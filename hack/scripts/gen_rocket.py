#!/usr/bin/env python3
"""Place the extra Team Rocket grunts of the hack on the dumped maps.

Usage: .venv/bin/python hack/scripts/gen_rocket.py [--dry-run]

Every entry of GRUNTS is a grunt that battles when talked to (trainers 739 and up, whose teams are in
hack/scripts/gen_trainer_teams.py).  They are only on the map while Team Rocket is active there: the
object is hidden by the same story flag as the vanilla Rocket members of that part of the story.
Positions are chosen like the static Pokémon (hack/scripts/gen_specialists.py has the shared code).
The script is idempotent: a grunt that is already on its map is skipped.
"""
import sys

from gen_specialists import MapFiles, Maps

# (map, trainer, defeated flag, flag that hides the object, where)
GRUNTS = [
    ("R43", 739, 2595, "FLAG_HIDE_ROUTE_43_GATE_ROCKETS", "Route 43, until the Mahogany hideout is cleared"),
    ("T29", 740, 2596, "FLAG_HIDE_ROUTE_43_GATE_ROCKETS", "Lake of Rage, until the Mahogany hideout is cleared"),
    ("T28", 741, 2597, "FLAG_HIDE_ROUTE_43_GATE_ROCKETS", "Mahogany Town, until the Mahogany hideout is cleared"),
    ("T25", 742, 2598, "FLAG_HIDE_ROCKET_TAKEOVER_1", "Goldenrod City, during the Radio Tower takeover"),
    ("T25", 743, 2599, "FLAG_HIDE_ROCKET_TAKEOVER_1", "Goldenrod City, during the Radio Tower takeover"),
]

# common script 2078 talks (and tells in VAR_SPECIAL_RESULT whether to battle), 2079 is the line after a win
SCRIPT = """
// hack: extra Team Rocket grunt, {where} (hack/scripts/gen_rocket.py)
{label}:
	setvar VAR_SPECIAL_x8007, {flag}
	callstd 2078
	compare VAR_SPECIAL_RESULT, 0
	goto_if_eq {label}_end
	trainer_battle TRAINER_HACK_{trainer}, 0, 0, 0
	check_battle_won VAR_SPECIAL_RESULT
	compare VAR_SPECIAL_RESULT, 0
	goto_if_eq {label}_lost
	setflag {flag}
	callstd 2079
{label}_end:
	releaseall
	end

{label}_lost:
	white_out
	releaseall
	end
"""


def main():
    dry_run = "--dry-run" in sys.argv
    maps = Maps()
    files = {}
    for map_name, trainer, flag, hidden_flag, where in GRUNTS:
        map_files = files.setdefault(map_name, MapFiles(map_name))
        obj = f"obj_{map_name}_hack_rocket_{trainer}"
        if any(e["id"] == obj for e in map_files.events.get("object_events", [])):
            print(f"{map_name}: grunt {trainer} already placed, skipped")
            continue
        spot = maps.find_spot(map_name, map_files.events)
        if spot is None:
            sys.exit(f"{map_name}: no free spot for grunt {trainer}")
        label = map_files.add(obj, "SPRITE_ROCKETM", spot[1], spot[2], SCRIPT, hidden_flag=hidden_flag,
                              trainer=trainer, flag=flag, where=where)
        print(f"{map_name}: grunt {trainer} at ({spot[1]}, {spot[2]}), script {label}, defeated flag {flag}, hidden by {hidden_flag}")
    if not dry_run:
        for map_files in files.values():
            map_files.save()


if __name__ == "__main__":
    main()
