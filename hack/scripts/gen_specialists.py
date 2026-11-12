#!/usr/bin/env python3
"""Place the species specialists ("mirror match") on the dumped maps.

Usage: .venv/bin/python hack/scripts/gen_specialists.py [--dry-run] [--fix-positions]

--fix-positions checks every object the hack added to the maps (specialists, static Pokémon, grunts...)
and moves the ones that do not stand on a valid spot; nothing else changes.

There is one specialist for every fully evolved or single stage Pokémon whose family is found in the
wild (data/Encounters.c, so run gen_encounters.py first).  Each one stands in a zone where the family
appears, at a level relative to that zone, and only battles a player that brings the same species,
one on one (src/hack_mirror.c and common script 2077).  Beating one gives an item for the species.

For every specialist the script adds to the dumped files of the map:
  data/eventdata/zone_event/NNN_<MAP>.json   the NPC
  data/scr_seq/include/event_<MAP>.inc       script and object labels
  data/scr_seq/scr_seq_NNNN_<MAP>.s          a short script that calls the common script

It is idempotent: specialists that are already on a map are kept where they are, with their flag.
Positions come from the collision data of rom.nds: the centre of a 3x3 block of plain walkable
ground that is connected to a warp or to an original event of the map (so never in the empty
space around indoor rooms nor behind a fence), at least 3 tiles away from every other event of the map (2 tiles, and tall grass too, when a zone has no room otherwise).
"""
import collections
import glob
import json
import re
import struct
import sys
from pathlib import Path

import ndspy.codeCompression
import ndspy.narc
import ndspy.rom

ROOT = Path(__file__).resolve().parents[2]

MAP_HEADERS_OFFSET = 0xF6BE0  # table of 24 byte map headers in the decompressed arm9 of HeartGold (U)
MAX_SPECIES = 1025            # forms and megas have higher ids and no specialist of their own
MAX_PER_MAP = 6               # raised automatically if the specialists do not fit
MAX_OBJECTS = 40              # do not crowd a map beyond this many objects
LEVEL_BONUS = 3               # levels above the strongest wild member of the family in the zone
MAX_LEVEL = 80

# unused script flags (hack/README.md): one per specialist, set when it is beaten
# 2098 to 2199 are kept for the defeated flags of new trainers (TRAINER_FLAG_BASE 1360 + trainer id),
# 2595 to 2599 for story NPCs of the hack
FLAG_POOL = [*range(2200, 2400), *range(2603, 2720), *range(2522, 2595)]

# where a specialist must stand close to a known spot: Cherrygrove City, for the in-game test
NEAR = {"T21": (566, 402)}

SPRITES = ["SPRITE_GSMAN1", "SPRITE_GSBOY3", "SPRITE_WOMAN3", "SPRITE_GSBIGMAN", "SPRITE_GSGENTLEMAN"]

# reward when the species has no Mega Stone, in rotation
ITEMS = """LEFTOVERS LIFE_ORB CHOICE_BAND CHOICE_SPECS CHOICE_SCARF FOCUS_SASH EXPERT_BELT ROCKY_HELMET
    ASSAULT_VEST WEAKNESS_POLICY EVIOLITE SHELL_BELL MUSCLE_BAND WISE_GLASSES SCOPE_LENS BRIGHT_POWDER
    QUICK_CLAW KINGS_ROCK AIR_BALLOON RED_CARD EJECT_BUTTON HEAVY_DUTY_BOOTS PP_UP RARE_CANDY BOTTLE_CAP
    ABILITY_CAPSULE LUM_BERRY SITRUS_BERRY""".split()

SCRIPT = """
// hack: {species} specialist (hack/scripts/gen_specialists.py)
{label}:
	setvar VAR_SPECIAL_x8004, SPECIES_{species}
	setvar VAR_SPECIAL_x8005, {level}
	setvar VAR_SPECIAL_x8006, ITEM_{item}
	setvar VAR_SPECIAL_x8007, {flag}
	callstd 2077
	end
"""


class Maps:
    """map headers, matrices and collision data of the base ROM"""

    def __init__(self):
        rom = ndspy.rom.NintendoDSRom.fromFile(str(ROOT / "rom.nds"))
        arm9 = rom.arm9
        try:
            arm9 = ndspy.codeCompression.decompress(arm9)
        except Exception:
            pass
        self.matrices = ndspy.narc.NARC(rom.getFileByName("a/0/4/1")).files
        self.land = ndspy.narc.NARC(rom.getFileByName("a/0/6/5")).files
        self.names = {int(value): name for name, value in
                      re.findall(r"\.equ MAP_(\w+), (\d+)", (ROOT / "asm/include/maps.inc").read_text())}
        self.headers = {}
        for header, name in self.names.items():
            wild, _, _, matrix = struct.unpack_from("<BBHH", arm9, MAP_HEADERS_OFFSET + header * 24)
            self.headers[name] = {"id": header, "wild": wild, "matrix": matrix}
        self.matrix_cache = {}
        self.permission_cache = {}
        self.reach_cache = {}

    def matrix(self, index):
        if index not in self.matrix_cache:
            data = self.matrices[index]
            width, height, has_headers, has_altitudes, name_length = data[:5]
            offset = 5 + name_length
            cells = width * height
            headers = struct.unpack_from(f"<{cells}H", data, offset) if has_headers else None
            offset += (2 * cells if has_headers else 0) + (cells if has_altitudes else 0)
            self.matrix_cache[index] = (width, height, headers, struct.unpack_from(f"<{cells}H", data, offset))
        return self.matrix_cache[index]

    def permissions(self, land_id):
        if land_id not in self.permission_cache:
            data = self.land[land_id]
            background_size = struct.unpack_from("<H", data, 18)[0]
            self.permission_cache[land_id] = struct.unpack_from("<1024H", data, 20 + background_size)
        return self.permission_cache[land_id]

    def tile(self, matrix_index, x, z):
        width, height, _, land_ids = self.matrix(matrix_index)
        if not (0 <= x < width * 32 and 0 <= z < height * 32):
            return 0xFFFF
        land_id = land_ids[(z // 32) * width + x // 32]
        if land_id == 0xFFFF or land_id >= len(self.land):
            return 0xFFFF
        return self.permissions(land_id)[(z % 32) * 32 + x % 32]

    def cells(self, map_name):
        header = self.headers[map_name]
        width, height, headers, _ = self.matrix(header["matrix"])
        return [(i % width, i // width) for i in range(width * height) if headers is None or headers[i] == header["id"]]

    # behaviours (low byte of a tile) the player can simply walk on: plain ground, tall grass, cave
    # floor and the two Cycling Road surfaces.  everything else is water, ice, ledges, doors, stairs...
    WALKABLE = (0x00, 0x02, 0x08, 0x70, 0x71)
    STANDABLE = (0x00, 0x08, 0x71)  # where an NPC may stand; tall grass only as a last resort

    @classmethod
    def passable(cls, tile):
        """a tile the player can walk on: no collision flag (high bit) and a walkable behaviour"""
        return tile != 0xFFFF and not tile & 0x8000 and tile & 0xFF in cls.WALKABLE

    def reachable(self, map_name, events):
        """tiles of the map connected by passable ground to a warp or to an existing event.
        this is what tells real floor from the empty space around indoor rooms (which is also 0)
        and from pockets behind fences"""
        key = (map_name, len(events.get("object_events", [])))
        if key in self.reach_cache:
            return self.reach_cache[key]
        matrix = self.headers[map_name]["matrix"]
        cells = set(self.cells(map_name))
        seeds = [(e["x"], e["z"]) for kind in ("warp_events", "object_events", "bg_events") for e in events.get(kind, [])
                 if not str(e.get("id", "")).count("_hack_")]
        seen, stack = set(), []
        for x, z in seeds:
            for dx, dz in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
                stack.append((x + dx, z + dz))
        while stack:
            x, z = stack.pop()
            if (x, z) in seen or (x // 32, z // 32) not in cells or not self.passable(self.tile(matrix, x, z)):
                continue
            seen.add((x, z))
            stack += [(x + 1, z), (x - 1, z), (x, z + 1), (x, z - 1)]
        self.reach_cache[key] = seen
        return seen

    def spot_ok(self, map_name, events, x, z, spacing=3, grass=False, ignore=None):
        """the centre of a 3x3 block of reachable ground, away from the other events"""
        matrix = self.headers[map_name]["matrix"]
        reached = self.reachable(map_name, events)
        allowed = self.STANDABLE + ((0x02,) if grass else ())
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                if (x + dx, z + dz) not in reached or self.tile(matrix, x + dx, z + dz) & 0xFF not in allowed:
                    return False
        occupied = [(e["x"], e["z"]) for kind in ("object_events", "bg_events", "warp_events") for e in events.get(kind, [])
                    if e is not ignore]
        for e in events.get("coord_events", []):
            occupied += [(e["x"] + i, e["z"] + j) for i in range(e.get("width", 1)) for j in range(e.get("length", 1))]
        return not any(abs(x - ox) < spacing and abs(z - oz) < spacing for ox, oz in occupied)

    def find_spot(self, map_name, events, near=None, spacing=3, grass=False, ignore=None):
        anchors = [(e["x"], e["z"]) for e in events.get("object_events", []) if e is not ignore]
        anchors = anchors or [(e["x"], e["z"]) for e in events.get("warp_events", [])] or [(16, 16)]
        centre = near or (sorted(x for x, _ in anchors)[len(anchors) // 2], sorted(z for _, z in anchors)[len(anchors) // 2])
        best = None
        for x, z in self.reachable(map_name, events):
            distance = abs(x - centre[0]) + abs(z - centre[1])
            if (best is None or distance < best[0]) and self.spot_ok(map_name, events, x, z, spacing, grass, ignore):
                best = (distance, x, z)
        return best


class MapFiles:
    """the three dumped files of a map"""

    def __init__(self, name):
        self.name = name
        json_paths = glob.glob(str(ROOT / f"data/eventdata/zone_event/[0-9][0-9][0-9]_{name}.json"))
        script_paths = glob.glob(str(ROOT / f"data/scr_seq/scr_seq_[0-9][0-9][0-9][0-9]_{name}.s"))
        self.inc_path = ROOT / f"data/scr_seq/include/event_{name}.inc"
        self.valid = bool(json_paths and script_paths and self.inc_path.exists())
        if self.valid:
            self.json_path, self.script_path = Path(json_paths[0]), Path(script_paths[0])
            self.events = json.loads(self.json_path.read_text())
            self.script = self.script_path.read_text()
            self.inc = self.inc_path.read_text()
            self.valid = "scrdef_end" in self.script and "\t.balign 4" in self.script and "_EV_scr_seq_" in self.inc
            self.dirty = False

    def add(self, obj, sprite, x, z, code_template, hidden_flag="FLAG_NOTHING", **values):
        number = len(re.findall(r"^scrdef scr_seq_", self.script, re.M))
        label = f"scr_seq_{self.name}_{number:03d}"
        self.events.setdefault("object_events", []).append({
            "id": obj, "graphics_id": sprite, "movement_type": 0, "trainer_type": 0, "hidden_flag": hidden_flag,
            "script": f"_EV_{label} + 1", "initial_dir": 1, "param0": 0, "param1": 0, "param2": 0,
            "movement_range_x": 0, "movement_range_z": 0, "x": x, "z": z, "y": 0,
        })
        last_script = re.findall(r"^\.equ _EV_scr_seq_\w+, \d+\n", self.inc, re.M)[-1]
        self.inc = self.inc.replace(last_script, last_script + f".equ _EV_{label}, {number}\n", 1)
        object_lines = re.findall(r"^\.equ obj_\w+, \d+\n", self.inc, re.M)
        if object_lines:
            self.inc = self.inc.replace(object_lines[-1], object_lines[-1] + f".equ {obj}, {len(object_lines)}\n", 1)
        else:
            self.inc = self.inc.replace(last_script + f".equ _EV_{label}, {number}\n",
                                        last_script + f".equ _EV_{label}, {number}\n\n.equ {obj}, 0\n", 1)
        self.script = self.script.replace("scrdef_end", f"scrdef {label}\nscrdef_end", 1)
        head, separator, tail = self.script.rpartition("\t.balign 4")
        self.script = head + code_template.format(label=label, obj=obj, **values).lstrip("\n") + separator + tail
        self.dirty = True
        return label

    def save(self):
        if self.dirty:
            self.json_path.write_text(json.dumps(self.events, indent=2))
            self.inc_path.write_text(self.inc)
            self.script_path.write_text(self.script)


def load_evolutions():
    evolutions = collections.defaultdict(list)
    level_needed = {}
    for block in re.split(r"\n(?=    \[SPECIES_)", (ROOT / "data/Evolutions.c").read_text())[1:]:
        base = re.match(r"    \[SPECIES_(\w+)\]", block).group(1)
        for method, parameter, target in re.findall(r"\{ (EVO_\w+), ([^,]+), SPECIES_(\w+) \}", block):
            if method != "EVO_NONE" and target != "NONE" and target not in evolutions[base]:
                evolutions[base].append(target)
                level_needed.setdefault(target, int(parameter) if method.startswith("EVO_LEVEL") and parameter.strip().isdigit() else 0)
    return evolutions, level_needed


def fix_positions(dry_run):
    """move every object of the hack (specialists, static Pokémon, grunts...) that does not stand on a
    valid spot to the nearest valid one of its map.  only the coordinates change"""
    maps = Maps()
    moved, stuck = 0, []
    for path in sorted(glob.glob(str(ROOT / "data/eventdata/zone_event/*.json"))):
        events = json.loads(Path(path).read_text())
        hack_objects = [e for e in events.get("object_events", []) if "_hack_" in str(e.get("id", ""))]
        if not hack_objects:
            continue
        name = Path(path).stem.split("_", 1)[1]
        changed = False
        for obj in hack_objects:
            if maps.spot_ok(name, events, obj["x"], obj["z"], spacing=2, grass=True, ignore=obj):
                continue
            spot = None
            for spacing, grass in ((3, False), (2, False), (2, True)):
                spot = maps.find_spot(name, events, near=(obj["x"], obj["z"]), spacing=spacing, grass=grass, ignore=obj)
                if spot:
                    break
            if spot is None:
                stuck.append(f"{obj['id']} ({obj['x']}, {obj['z']})")
                continue
            print(f"{obj['id']}: ({obj['x']}, {obj['z']}) -> ({spot[1]}, {spot[2]})")
            obj["x"], obj["z"] = spot[1], spot[2]
            maps.reach_cache.clear()
            moved += 1
            changed = True
        if changed and not dry_run:
            Path(path).write_text(json.dumps(events, indent=2))
    print(f"moved: {moved}; no valid spot in their map ({len(stuck)}): {' '.join(stuck)}")


def main():
    dry_run = "--dry-run" in sys.argv
    if "--fix-positions" in sys.argv:
        fix_positions(dry_run)
        return
    species_ids = {name: int(value) for name, value in
                   re.findall(r"#define SPECIES_(\w+)\s+(\d+)\b", (ROOT / "include/constants/species.h").read_text())}
    item_names = set(re.findall(r"#define ITEM_(\w+)\s+\d+", (ROOT / "include/constants/item.h").read_text()))
    evolutions, level_needed = load_evolutions()
    parent = {}
    for base, targets in evolutions.items():
        for target in targets:
            parent.setdefault(target, base)

    def root(species):
        while species in parent:
            species = parent[species]
        return species

    def finals(species):
        if not evolutions.get(species):
            return [species]
        return [final for target in evolutions[species] for final in finals(target)]

    def minimum_level(species):
        level = 0
        while species in parent:
            level = max(level, level_needed.get(species, 0))
            species = parent[species]
        return level

    def mega_stone(species):
        for name in (f"{species}ITE", f"{species[:-1]}ITE", f"{species}NITE", f"{species}ITE_X", f"{species}TITE",
                     f"{species[:-1]}ITE_X", f"{species}ANITE", f"{species[:-2]}ITE", f"{species}ZITE", f"{species}ITITE"):
            if name in item_names and len(name) > 6:
                return name
        return None

    # zones of every family, from the generated encounter tables
    blocks = re.split(r"\n(?=    \[ENCDATA_)", (ROOT / "data/Encounters.c").read_text())[1:]
    zone_families, zone_level = {}, {}
    for index, block in enumerate(blocks):
        name = re.match(r"    \[ENCDATA_(\w+)\]", block).group(1)
        if re.search(r"UNUSED|SAFARI|BUG_CATCHING", name):
            continue
        # level of a family in a zone: the strongest slot where one of its members appears
        levels = [int(x) for x in re.search(r"\.levels = \{\s*([^}]*)\}", block).group(1).split(",") if x.strip()]
        slots = []
        for field in ("speciesMorning", "speciesDay", "speciesNight"):
            names = re.findall(r"SPECIES_(\w+)", re.search(rf"\.{field} = \{{([^}}]*)\}}", block).group(1))
            slots += list(zip(names, levels))
        slots += [(name, int(high)) for _, high, name in re.findall(r"\{ (\d+), (\d+), SPECIES_(\w+) \}", block)]
        zone_families[index] = set()
        for name, level in slots:
            if name != "NONE" and level > 0:
                family = root(name)
                zone_families[index].add(family)
                zone_level[(index, family)] = max(zone_level.get((index, family), 0), level)

    maps = Maps()
    zone_maps = collections.defaultdict(list)
    files = {}
    for name, header in maps.headers.items():
        if header["wild"] in zone_families:
            files[name] = MapFiles(name)
            if files[name].valid and header["matrix"] < len(maps.matrices):
                zone_maps[header["wild"]].append(name)

    family_zones = collections.defaultdict(list)
    for zone, families in zone_families.items():
        if zone_maps[zone]:
            for family in families:
                family_zones[family].append(zone)
    wanted = sorted({final for family in family_zones for final in finals(family) if species_ids.get(final, 99999) <= MAX_SPECIES},
                    key=lambda s: species_ids[s])

    # specialists that are already placed keep their map and flag
    placed, used_flags, per_map = {}, set(), collections.Counter()
    for name, map_files in files.items():
        if not map_files.valid:
            continue
        for species, flag in re.findall(r"// hack: (\w+) specialist.*?setvar VAR_SPECIAL_x8007, (\d+)", map_files.script, re.S):
            placed[species] = name
            used_flags.add(int(flag))
            per_map[name] += 1
    free_flags = [flag for flag in FLAG_POOL if flag not in used_flags]
    todo = [species for species in wanted if species not in placed]
    print(f"specialists wanted: {len(wanted)}, already placed: {len(placed)}, to place: {len(todo)}, free flags: {len(free_flags)}")
    if len(todo) > len(free_flags):
        print(f"only {len(free_flags)} free flags: {len(todo) - len(free_flags)} specialists stay out until more flags are reserved")

    # species with few possible zones choose first; every species goes to its least crowded map
    todo.sort(key=lambda s: (len(family_zones[root(s)]), species_ids[s]))
    failed, new = [], 0
    for species in todo:
        candidates = [(zone, name) for zone in family_zones[root(species)] for name in zone_maps[zone]]
        done = False
        # first with the normal rules, then with more specialists per map, then closer to other events
        for limit, spacing, grass in ((MAX_PER_MAP, 3, False), (MAX_PER_MAP * 2, 3, False), (MAX_PER_MAP * 4, 3, False),
                                      (MAX_PER_MAP * 4, 2, False), (MAX_PER_MAP * 4, 2, True)):
            for zone, name in sorted(candidates, key=lambda c: (per_map[c[1]], c[1])):
                map_files = files[name]
                if per_map[name] >= limit or len(map_files.events.get("object_events", [])) >= MAX_OBJECTS:
                    continue
                spot = maps.find_spot(name, map_files.events, NEAR.get(name) if per_map[name] == 0 else None, spacing, grass)
                if spot is None:
                    continue
                level = min(MAX_LEVEL, max(zone_level[(zone, root(species))] + LEVEL_BONUS, minimum_level(species)))
                index = species_ids[species]
                item = mega_stone(species) or ITEMS[index % len(ITEMS)]
                if item not in item_names:
                    item = "RARE_CANDY"
                if not free_flags:
                    break
                flag = free_flags.pop(0)
                map_files.add(f"obj_{name}_hack_spec_{species.lower()}", SPRITES[index % len(SPRITES)], spot[1], spot[2],
                              SCRIPT, species=species, level=level, item=item, flag=flag)
                per_map[name] += 1
                placed[species] = name
                new += 1
                done = True
                break
            if done:
                break
        if not done:
            failed.append(species)

    counts = collections.Counter(per_map.values())
    print(f"placed now: {new}; maps used: {len([m for m in per_map if per_map[m]])}; specialists per map: {dict(sorted(counts.items()))}")
    print(f"no free spot in any of their zones ({len(failed)}): {' '.join(failed)}")
    if "--list" in sys.argv:
        for species in wanted:
            print(f"  {species}: {placed.get(species, '-')}")
    if not dry_run:
        for map_files in files.values():
            if map_files.valid:
                map_files.save()


if __name__ == "__main__":
    main()
