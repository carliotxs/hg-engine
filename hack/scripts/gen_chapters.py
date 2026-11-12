#!/usr/bin/env python3
"""Chapters of the debug ROM: start the game at a chosen point of the story.

Usage: .venv/bin/python hack/scripts/gen_chapters.py

A chapter is a map position plus the story state that makes that part of the game testable: badges,
flags and a party.  The debug ROM (make HACK_TEST=Y) applies the state and warps the player there;
hack/scripts/ingame_tests.py and hack/scripts/play.sh ask for a chapter by name.

CHAPTERS is the source of truth.  This script writes the two generated files that the build uses:
  include/hack_chapters.h                  the state of every chapter, for src/hack_test.c
  data/scr_seq/include/hack_chapters.inc   the warps, for common script 2073 of the debug ROM
Run it after changing the table or after moving the objects that chapters stand next to.

"next_to" puts the player on a walkable tile beside that object, facing it, so that pressing A talks
to it.  Flags can be names from asm/include/flags.inc or numbers; "vars" are (name or number, value)
pairs for story variables, which many maps read when they load to decide who is there.
"""
import glob
import json
import re
from pathlib import Path

from gen_specialists import ROOT, Maps

GARCHOMP = ("GARCHOMP", 60, "FLAMETHROWER")  # a move nothing in these chapters is immune to

CHAPTERS = [
    dict(name="lighthouse_korrina", map="D27R0107", next_to="obj_D27R0107_hack_korrina", badges=6,
         set=["FLAG_UNK_1D7", "FLAG_UNK_1D8"], clear=[2594, "FLAG_MEGA_EVOLUTION_ENABLED"], party=[GARCHOMP],
         about="topo do Farol de Olivine depois de a Amphy estar curada: Korrina"),
    dict(name="mahogany_rocket", map="T28", next_to="obj_T28_hack_rocket_741", badges=6,
         clear=["FLAG_HIDE_ROUTE_43_GATE_ROCKETS", 2597], party=[GARCHOMP],
         about="Mahogany Town com a Equipa Rocket ativa: recruta novo"),
    dict(name="lake_rocket", map="T29", next_to="obj_T29_hack_rocket_740", badges=6,
         clear=["FLAG_HIDE_ROUTE_43_GATE_ROCKETS", 2596], party=[GARCHOMP],
         about="Lago da Fúria com a Equipa Rocket ativa: recruta novo"),
    dict(name="route43_rocket", map="R43", next_to="obj_R43_hack_rocket_739", badges=6,
         clear=["FLAG_HIDE_ROUTE_43_GATE_ROCKETS", 2595], party=[GARCHOMP],
         about="Route 43 com a Equipa Rocket ativa: recruta novo"),
    dict(name="goldenrod_takeover", map="T25", next_to="obj_T25_hack_rocket_742", badges=7,
         clear=[2598, 2599], vars=[("VAR_SCENE_ROCKET_TAKEOVER", 3)], party=[GARCHOMP],
         about="Goldenrod City durante a tomada da Radio Tower: recrutas novos"),
    dict(name="union_cave_specialist", map="D25R0101", next_to="obj_D25R0101_hack_spec_golem", badges=1,
         party=[("GOLEM", 30, "EARTHQUAKE"), ("PIDGEY", 10, "TACKLE")],
         about="Union Cave: um especialista colocado numa gruta (Golem)"),
    dict(name="route31_static", map="R31", next_to="obj_R31_hack_static", badges=0, clear=[2900],
         party=[("PIDGEOTTO", 20, "GUST")], about="Route 31: o Rockruff estático"),
]

# offset from the object -> facing.  beside the object first: seen from the south the player's sprite
# covers whatever stands on the tile above
DIRECTIONS = {(1, 0): "DIR_WEST", (-1, 0): "DIR_EAST", (0, -1): "DIR_SOUTH", (0, 1): "DIR_NORTH"}
MAX_VARS = 3
MAX_FLAGS = 6
MAX_PARTY = 6


def main():
    maps = Maps()
    flags = {name: int(value) for name, value in re.findall(r"\.equ (FLAG_\w+), (\d+)", (ROOT / "asm/include/flags.inc").read_text())}
    variables = {name: int(value, 0) for name, value in re.findall(r"\.equ (VAR_\w+), (\w+)", (ROOT / "asm/include/vars.inc").read_text())}
    rows, warps, summary = [], [], []
    for index, chapter in enumerate(CHAPTERS):
        path = glob.glob(str(ROOT / f"data/eventdata/zone_event/[0-9][0-9][0-9]_{chapter['map']}.json"))[0]
        events = json.loads(Path(path).read_text())
        if "next_to" in chapter:
            obj = next(e for e in events["object_events"] if e["id"] == chapter["next_to"])
            reached = maps.reachable(chapter["map"], events)
            occupied = {(e["x"], e["z"]) for e in events["object_events"]}
            spot = next(((obj["x"] + dx, obj["z"] + dz, facing) for (dx, dz), facing in DIRECTIONS.items()
                         if (obj["x"] + dx, obj["z"] + dz) in reached and (obj["x"] + dx, obj["z"] + dz) not in occupied), None)
            if spot is None:
                raise SystemExit(f"{chapter['name']}: no walkable tile next to {chapter['next_to']}")
            x, z, facing = spot
        else:
            x, z, facing = chapter["x"], chapter["z"], chapter.get("facing", "DIR_SOUTH")

        def numbers(names):
            values = [flags[name] if isinstance(name, str) else name for name in names]
            assert len(values) <= MAX_FLAGS, chapter["name"]
            return ", ".join(str(v) for v in values + [0] * (MAX_FLAGS - len(values)))

        var_list = [(variables[name] if isinstance(name, str) else name, value) for name, value in chapter.get("vars", [])]
        assert len(var_list) <= MAX_VARS, chapter["name"]
        var_text = ", ".join(f"{{ {var}, {value} }}" for var, value in var_list + [(0, 0)] * (MAX_VARS - len(var_list)))
        party = ", ".join(f"{{ SPECIES_{s}, {level}, MOVE_{move} }}" for s, level, move in chapter["party"])
        rows.append(f"    // {index}: {chapter['name']}\n    {{ {chapter.get('badges', 0)}, {{ {numbers(chapter.get('set', []))} }}, "
                    f"{{ {numbers(chapter.get('clear', []))} }}, {{ {var_text} }}, {{ {party} }} }},")
        warps.append(f"    compare VAR_SPECIAL_RESULT, {index} // {chapter['name']}\n    goto_if_ne _hack_chapter_skip_{index}\n"
                     f"    warp MAP_{chapter['map']}, 0, {x}, {z}, {facing}\n_hack_chapter_skip_{index}:")
        summary.append(f"{index}: {chapter['name']}: {chapter['map']} ({x}, {z}) {facing}")

    header = f"""#ifndef HACK_CHAPTERS_H
#define HACK_CHAPTERS_H

// generated by hack/scripts/gen_chapters.py, do not edit: chapters of the debug ROM (make HACK_TEST=Y)

#define HACK_CHAPTER_COUNT {len(CHAPTERS)}
#define HACK_CHAPTER_MAX_FLAGS {MAX_FLAGS}
#define HACK_CHAPTER_MAX_PARTY {MAX_PARTY}
#define HACK_CHAPTER_MAX_VARS {MAX_VARS}

struct HackChapterMon {{
    u16 species;
    u16 level;
    u16 move;
}};

struct HackChapter {{
    u8 badges;                                // number of Johto badges
    u16 flagsSet[HACK_CHAPTER_MAX_FLAGS];     // 0 ends the list
    u16 flagsClear[HACK_CHAPTER_MAX_FLAGS];
    u16 vars[HACK_CHAPTER_MAX_VARS][2];       // story variable and its value, variable 0 ends the list
    struct HackChapterMon party[HACK_CHAPTER_MAX_PARTY]; // species 0 ends the list
}};

#ifdef HACK_CHAPTER_TABLE
static const struct HackChapter sHackChapters[HACK_CHAPTER_COUNT] = {{
{chr(10).join(rows)}
}};
#endif // HACK_CHAPTER_TABLE

#endif // HACK_CHAPTERS_H
"""
    inc = ("// generated by hack/scripts/gen_chapters.py, do not edit: warps of the chapters of the debug ROM.\n"
           "// VAR_SPECIAL_RESULT holds the chapter number\n.macro hack_chapter_warps\n" + "\n".join(warps) + "\n.endm\n")
    (ROOT / "include/hack_chapters.h").write_text(header)
    (ROOT / "data/scr_seq/include/hack_chapters.inc").write_text(inc)
    print("\n".join(summary))


if __name__ == "__main__":
    main()
