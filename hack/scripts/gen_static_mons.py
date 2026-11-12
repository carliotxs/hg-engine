#!/usr/bin/env python3
"""Add the visible static Pokémon of the hack to the dumped maps.

Usage: .venv/bin/python hack/scripts/gen_static_mons.py [--dry-run]

Every entry of STATIC_MONS becomes a map object with the overworld sprite of the species.  Talking to
it starts a wild battle; afterwards the object is hidden by a daily flag, so it is back the next day.

For every entry the script edits three dumped files of the map (it is idempotent: an entry that is
already there is skipped, so positions never move once they are committed):
  data/eventdata/zone_event/NNN_<MAP>.json   the object event
  data/scr_seq/include/event_<MAP>.inc       script and object labels
  data/scr_seq/scr_seq_NNNN_<MAP>.s          the script

The position is chosen from the collision data of rom.nds: the centre of a 3x3 block of plain
walkable ground (so the Pokémon can always be walked around and never blocks a path), at least 3
tiles away from every other event of the map and as close as possible to the middle of its objects.
"""
import glob
import json
import re
import struct
import sys
from pathlib import Path

import ndspy.narc
import ndspy.rom

ROOT = Path(__file__).resolve().parents[2]

# (map, species, level, daily flag[, (x, z) to stay close to]).  flags 2900-2911 are unused daily flags (reset at midnight),
# registered in hack/README.md.  no legendaries here: those come with the side quests
STATIC_MONS = [
    ("T21", "YAMPER", 4, 2910, (565, 398)),  # Cherrygrove City, next to where the in-game test save stands
    ("R31", "ROCKRUFF", 6, 2900),
    ("R32", "RIOLU", 8, 2901),
    ("R33", "ZORUA", 10, 2902),
    ("R34", "EEVEE", 12, 2903),
    ("R36", "ABSOL", 16, 2904),
    ("R38", "MIMIKYU", 18, 2905),
    ("R42", "GOOMY", 20, 2906),
    ("R44", "AXEW", 25, 2907),
    ("R45", "GIBLE", 27, 2908),
    ("R47", "DRAMPA", 32, 2909),
]

MON_OVERWORLD_TAG_START = 2500  # include/constants/pokemon.h: overworld tag of a species

SCRIPT = """
// hack: visible static Pokémon with daily respawn (hack/scripts/gen_static_mons.py)
{label}:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	play_cry SPECIES_{species}, 0
	wait_cry
	setflag FLAG_ENGAGING_STATIC_POKEMON
	wild_battle SPECIES_{species}, {level}, 0
	clearflag FLAG_ENGAGING_STATIC_POKEMON
	check_battle_won VAR_SPECIAL_RESULT
	compare VAR_SPECIAL_RESULT, 0
	goto_if_eq {label}_lost
	setflag {flag}
	hide_person {obj}
	releaseall
	end

{label}_lost:
	white_out
	releaseall
	end
"""


class Maps:
    """collision data of the overworld matrix of the base ROM"""

    def __init__(self):
        rom = ndspy.rom.NintendoDSRom.fromFile(str(ROOT / "rom.nds"))
        matrix = ndspy.narc.NARC(rom.getFileByName("a/0/4/1")).files[0]
        self.land = ndspy.narc.NARC(rom.getFileByName("a/0/6/5")).files
        self.width, self.height, has_headers, has_altitudes, name_length = matrix[:5]
        offset = 5 + name_length
        cells = self.width * self.height
        self.headers = struct.unpack_from(f"<{cells}H", matrix, offset)
        offset += 2 * cells + (cells if has_altitudes else 0)
        self.land_ids = struct.unpack_from(f"<{cells}H", matrix, offset)
        self.map_ids = {name: int(value) for name, value in
                        re.findall(r"\.equ MAP_(\w+), (\d+)", (ROOT / "asm/include/maps.inc").read_text())}
        self.cache = {}

    def permissions(self, cell):
        if cell not in self.cache:
            data = self.land[self.land_ids[cell]]
            background_size = struct.unpack_from("<H", data, 18)[0]
            self.cache[cell] = struct.unpack_from("<1024H", data, 20 + background_size)
        return self.cache[cell]

    def tile(self, x, z):
        """permission of a global tile: 0 is plain walkable ground"""
        if not (0 <= x < self.width * 32 and 0 <= z < self.height * 32):
            return 0xFFFF
        cell = (z // 32) * self.width + x // 32
        if self.land_ids[cell] == 0xFFFF:
            return 0xFFFF
        return self.permissions(cell)[(z % 32) * 32 + x % 32]

    def cells_of(self, map_name):
        header = self.map_ids[map_name]
        return [(i % self.width, i // self.width) for i, value in enumerate(self.headers) if value == header]


def find_spot(maps, map_name, events, near=None):
    occupied = [(e["x"], e["z"]) for kind in ("object_events", "bg_events", "warp_events") for e in events.get(kind, [])]
    for e in events.get("coord_events", []):
        occupied += [(e["x"] + dx, e["z"] + dz) for dx in range(e.get("width", 1)) for dz in range(e.get("length", 1))]
    objects = [(e["x"], e["z"]) for e in events.get("object_events", [])] or occupied
    centre_x = sorted(x for x, _ in objects)[len(objects) // 2]
    centre_z = sorted(z for _, z in objects)[len(objects) // 2]
    if near:
        centre_x, centre_z = near
    best = None
    for cell_x, cell_z in maps.cells_of(map_name):
        for x in range(cell_x * 32 + 1, cell_x * 32 + 31):
            for z in range(cell_z * 32 + 1, cell_z * 32 + 31):
                if any(maps.tile(x + dx, z + dz) != 0 for dx in (-1, 0, 1) for dz in (-1, 0, 1)):
                    continue
                if any(abs(x - ox) < 3 and abs(z - oz) < 3 for ox, oz in occupied):
                    continue
                distance = abs(x - centre_x) + abs(z - centre_z)
                if best is None or distance < best[0]:
                    best = (distance, x, z)
    return best


def main():
    dry_run = "--dry-run" in sys.argv
    maps = Maps()
    species_ids = {name: int(value) for name, value in
                   re.findall(r"#define SPECIES_(\w+)\s+(\d+)\b", (ROOT / "include/constants/species.h").read_text())}
    for map_name, species, level, flag, *near in STATIC_MONS:
        json_path = Path(glob.glob(str(ROOT / f"data/eventdata/zone_event/*_{map_name}.json"))[0])
        script_path = Path(glob.glob(str(ROOT / f"data/scr_seq/scr_seq_[0-9][0-9][0-9][0-9]_{map_name}.s"))[0])
        inc_path = ROOT / f"data/scr_seq/include/event_{map_name}.inc"
        events = json.loads(json_path.read_text())
        obj = f"obj_{map_name}_hack_static"
        if any(e["id"] == obj for e in events["object_events"]):
            print(f"{map_name}: {species} already placed, skipped")
            continue
        spot = find_spot(maps, map_name, events, near[0] if near else None)
        if spot is None:
            print(f"{map_name}: no free 3x3 spot found for {species}")
            sys.exit(1)
        _, x, z = spot

        script = script_path.read_text()
        number = len(re.findall(r"^scrdef scr_seq_", script, re.M))
        label = f"scr_seq_{map_name}_{number:03d}"
        flag_name = f"FLAG_UNK_{flag:03X}"
        print(f"{map_name}: {species} lv {level} at ({x}, {z}), script {label}, flag {flag} ({flag_name})")
        if dry_run:
            continue

        events.setdefault("object_events", []).append({
            "id": obj, "graphics_id": f"{MON_OVERWORLD_TAG_START} + {species_ids[species]}", "movement_type": 0, "trainer_type": 0,
            "hidden_flag": flag_name, "script": f"_EV_{label} + 1", "initial_dir": 1,
            "param0": 0, "param1": 0, "param2": 0, "movement_range_x": 0, "movement_range_z": 0,
            "x": x, "z": z, "y": 0,
        })
        json_path.write_text(json.dumps(events, indent=2))

        inc = inc_path.read_text()
        last_script = re.findall(r"^\.equ _EV_scr_seq_\w+, \d+\n", inc, re.M)[-1]
        inc = inc.replace(last_script, last_script + f".equ _EV_{label}, {number}\n", 1)
        object_lines = re.findall(r"^\.equ obj_\w+, \d+\n", inc, re.M)
        inc = inc.replace(object_lines[-1], object_lines[-1] + f".equ {obj}, {len(object_lines)}\n", 1)
        inc_path.write_text(inc)

        script = script.replace("scrdef_end", f"scrdef {label}\nscrdef_end", 1)
        code = SCRIPT.format(label=label, species=species, level=level, flag=flag_name, obj=obj)
        head, separator, tail = script.rpartition("\t.balign 4")
        script_path.write_text(head + code.lstrip("\n") + separator + tail)


if __name__ == "__main__":
    main()
