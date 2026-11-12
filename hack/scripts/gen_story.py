#!/usr/bin/env python3
"""Place the story objects of the hack that come and go by rule (src/hack_story.c).

Usage: .venv/bin/python hack/scripts/gen_story.py [--dry-run]

  * Giovanni in the hidden cave of Tohjo Falls (map D45R0102) after the Radio Tower is freed.  The
    cave is reached with Surf and Waterfall; the invisible obstacle in front of its door gets a hide
    flag of its own, which the rules set once the Radio Tower is done.  He uses his vanilla trainer
    entry (700), whose team is in hack/scripts/gen_trainer_teams.py
  * famous visitors: Crasher Wake at the Lake of Rage on Saturdays, one battle a day, for a Mystic Water
  * random events: a Team Rocket grunt robbing a Poké Mart, a different one depending on the day of
    the week, once a day.  Beating him gets an Elixir from the clerk

The visibility rules themselves are in src/hack_story.c; here only the hide flag of each object is
set.  The script is idempotent.
"""
import json
import sys

from gen_specialists import ROOT, MapFiles, Maps

GIOVANNI_MAP = "D45R0102"
GIOVANNI_TEXT = ROOT / "data/text/custom/131.txt"
GIOVANNI_FIRST_LINE = 28
GIOVANNI_LINES = [
    "...\\r...I heard it on the radio.\\nMy men called for me, and I did not come.\\rI was on my way. Then I heard how\\nit ended. A child, again.\\rThree years of training, alone,\\nto become strong enough to return...\\rLet me see what stopped them.",
    "...I see.\\nSo this is how it ends, a second time.\\rTeam Rocket is finished. This time\\nI will not ask them to wait for me.",
    "You received the Kangaskhanite!",
    "It reacts to the bond between\\na parent and a child.\\rI have no use for it anymore.",
]
GIOVANNI_SCRIPT = """
// hack: Giovanni after the Radio Tower (hack/scripts/gen_story.py)
{label}:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	npc_msg {m0}
	closemsg
	trainer_battle TRAINER_ROCKET_BOSS_GIOVANNI, 0, 0, 0
	check_battle_won VAR_SPECIAL_RESULT
	compare VAR_SPECIAL_RESULT, 0
	goto_if_eq {label}_lost
	npc_msg {m1}
	giveitem ITEM_KANGASKHANITE, 1, VAR_SPECIAL_RESULT
	play_fanfare SEQ_ME_ITEM
	npc_msg {m2}
	wait_fanfare
	npc_msg {m3}
	closemsg
	fade_screen 6, 1, 0, RGB_BLACK
	wait_fade
	setflag 1342 // HACK_FLAG_GIOVANNI_DONE
	setflag 1341 // HACK_FLAG_HIDE_GIOVANNI
	hide_person {obj}
	fade_screen 6, 1, 1, RGB_BLACK
	wait_fade
	releaseall
	end

{label}_lost:
	white_out
	releaseall
	end
"""

# (map, trainer, hide flag): which days each one is active is in src/hack_story.c
MART_ROBBERS = [("T21FS0101", 745, 1343), ("T22FS0101", 746, 1344), ("T23FS0101", 747, 1345)]
MART_SCRIPT = """
// hack: random event, a grunt robbing this Poké Mart (hack/scripts/gen_story.py)
{label}:
	callstd 2080
	trainer_battle TRAINER_HACK_{trainer}, 0, 0, 0
	check_battle_won VAR_SPECIAL_RESULT
	compare VAR_SPECIAL_RESULT, 0
	goto_if_eq {label}_lost
	setflag 2880 // HACK_DAILY_FLAG_MART_ROBBER: no more robberies today
	setflag {hide}
	setvar VAR_SPECIAL_x8006, ITEM_ELIXIR
	callstd 2081
	hide_person {obj}
	releaseall
	end

{label}_lost:
	white_out
	releaseall
	end
"""


# famous visitors: (map, object suffix, sprite, trainer, hide flag, daily done flag, reward item, lines).
# when each one shows up is in src/hack_story.c
VISITORS = [
    ("T29", "wake", "SPRITE_LEADER3", 748, 1346, 2881, "MYSTIC_WATER", [
        "Hahaha! A challenger at the lake!\\rI’m Crasher Wake, from Pastoria City\\nin Sinnoh! Every Saturday I train\\fagainst the waves of this lake.\\rYou look strong. Come at me!",
        "Hahaha! You washed me away!\\nTake this, you earned it!",
        "You received the Mystic Water!",
        "I’m here every Saturday while the\\nsun is up. Come back for a rematch!",
    ]),
]
VISITOR_SCRIPT = """
// hack: famous visitor, {name} (hack/scripts/gen_story.py)
{label}:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	npc_msg {m0}
	closemsg
	trainer_battle TRAINER_HACK_{trainer}, 0, 0, 0
	check_battle_won VAR_SPECIAL_RESULT
	compare VAR_SPECIAL_RESULT, 0
	goto_if_eq {label}_lost
	npc_msg {m1}
	giveitem ITEM_{item}, 1, VAR_SPECIAL_RESULT
	play_fanfare SEQ_ME_ITEM
	npc_msg {m2}
	wait_fanfare
	npc_msg {m3}
	closemsg
	fade_screen 6, 1, 0, RGB_BLACK
	wait_fade
	setflag {done} // battled today
	setflag {hide}
	hide_person {obj}
	fade_screen 6, 1, 1, RGB_BLACK
	wait_fade
	releaseall
	end

{label}_lost:
	white_out
	releaseall
	end
"""


def text_archive(map_files):
    """path of the text archive the map's script uses"""
    import re
    number = re.search(r"// text archive to grab from: (\d+)\.txt", map_files.script).group(1)
    return ROOT / f"data/text/custom/{number}.txt"


def main():
    dry_run = "--dry-run" in sys.argv
    maps = Maps()
    changed = []

    falls = MapFiles("D45R0101")
    stop = next(e for e in falls.events["object_events"] if e["id"] == "obj_D45R0101_stop")
    if stop["hidden_flag"] != "1340":
        stop["hidden_flag"] = "1340"  # HACK_FLAG_HIDE_TOHJO_CAVE_BLOCK
        falls.dirty = True
        changed.append(falls)
        print("Tohjo Falls: the obstacle of the hidden cave now has hide flag 1340")

    cave = MapFiles(GIOVANNI_MAP)
    obj = f"obj_{GIOVANNI_MAP}_hack_giovanni"
    if not any(e["id"] == obj for e in cave.events["object_events"]):
        spot = maps.find_spot(GIOVANNI_MAP, cave.events, near=(9, 6), spacing=2)
        if spot is None:
            sys.exit("no free spot for Giovanni")
        messages = {f"m{i}": GIOVANNI_FIRST_LINE + i for i in range(len(GIOVANNI_LINES))}
        label = cave.add(obj, "SPRITE_SAKAKI", spot[1], spot[2], GIOVANNI_SCRIPT, hidden_flag="1341", **messages)
        text = GIOVANNI_TEXT.read_bytes()
        assert text.count(b"\r\n") == GIOVANNI_FIRST_LINE, "text 131 changed: check GIOVANNI_FIRST_LINE"
        if not dry_run:
            GIOVANNI_TEXT.write_bytes(text + ("\r\n".join(GIOVANNI_LINES) + "\r\n").encode())
        changed.append(cave)
        print(f"Giovanni at ({spot[1]}, {spot[2]}) of {GIOVANNI_MAP}, script {label}")

    for map_name, trainer, hide in MART_ROBBERS:
        mart = MapFiles(map_name)
        obj = f"obj_{map_name}_hack_robber"
        if any(e["id"] == obj for e in mart.events.get("object_events", [])):
            continue
        spot = maps.find_spot(map_name, mart.events, spacing=2)
        if spot is None:
            sys.exit(f"{map_name}: no free spot for the robber")
        label = mart.add(obj, "SPRITE_ROCKETM", spot[1], spot[2], MART_SCRIPT, hidden_flag=str(hide), trainer=trainer, hide=hide)
        changed.append(mart)
        print(f"{map_name}: robber at ({spot[1]}, {spot[2]}), script {label}, hide flag {hide}")

    for map_name, suffix, sprite, trainer, hide, done, item, lines in VISITORS:
        visited = MapFiles(map_name)
        obj = f"obj_{map_name}_hack_visitor_{suffix}"
        if any(e["id"] == obj for e in visited.events.get("object_events", [])):
            continue
        spot = maps.find_spot(map_name, visited.events)
        if spot is None:
            sys.exit(f"{map_name}: no free spot for {suffix}")
        path = text_archive(visited)
        text = path.read_bytes()
        first = text.count(b"\r\n")
        messages = {f"m{i}": first + i for i in range(len(lines))}
        label = visited.add(obj, sprite, spot[1], spot[2], VISITOR_SCRIPT, hidden_flag=str(hide), name=suffix, trainer=trainer,
                            item=item, hide=hide, done=done, **messages)
        if not dry_run:
            path.write_bytes(text + ("\r\n".join(lines) + "\r\n").encode())
        changed.append(visited)
        print(f"{map_name}: visitor {suffix} at ({spot[1]}, {spot[2]}), script {label}, messages from {first} in {path.name}")

    if not dry_run:
        for map_files in changed:
            map_files.save()


if __name__ == "__main__":
    main()
