#!/usr/bin/env python3
"""Add Korrina to the top of the Olivine Lighthouse (Kalos / Mega Evolution arc of the hack).

Usage: .venv/bin/python hack/scripts/gen_korrina.py [--dry-run]

After Amphy is cured (Jasmine has left for her gym), Korrina stands in the light room.  She battles
the player (trainer 744, see hack/scripts/gen_trainer_teams.py), switches Mega Evolution on (flag
2518) and gives the Key Stone and the Ampharosite.  The script edits the dumped files of map D27R0107
and its text archive (data/text/custom/094.txt) once; running it again changes nothing.
"""
import sys
from pathlib import Path

from gen_specialists import ROOT, MapFiles, Maps

MAP = "D27R0107"
OBJECT = f"obj_{MAP}_hack_korrina"
DONE_FLAG = 2594             # set once the player has the Key Stone (hack/README.md)
JASMINE_GONE = "FLAG_UNK_1D7"  # hides Jasmine in this room: set when she goes back to the gym
TEXT = ROOT / "data/text/custom/094.txt"
FIRST_LINE = 13              # first new message index in the text archive

LINES = [
    "Oh! You’re the one who brought\\nthe medicine for Amphy?\\rI’m Korrina. I came all the way\\nfrom Kalos to see this Ampharos.\\rIn Kalos, some Pokémon can go beyond\\nevolution when the bond with their\\fTrainer is strong enough.\\rLet me see your bond. Battle me!",
    "That was amazing!\\rYou saw what my Lucario did?\\nThat was Mega Evolution.\\rYou’ll need two stones for it.\\nThis one is for you, the Trainer.",
    "You received the Key Stone!",
    "And this one is for the Pokémon.\\nAmphy wanted you to have it.",
    "You received the Ampharosite!",
    "Let an Ampharos hold it and\\nyou’ll see for yourself in battle.\\rThere are more Mega Stones hidden\\nall over Johto and Kanto.\\rGo find them!",
    "Mega Evolution is all about the bond\\nbetween a Trainer and a Pokémon.\\rI’ll watch the sea with Amphy\\na little longer.",
]

SCRIPT = """
// hack: Korrina, Kalos arc (hack/scripts/gen_korrina.py)
{label}:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	goto_if_set {done}, {label}_done
	npc_msg {m0}
	closemsg
	setflag FLAG_MEGA_EVOLUTION_ENABLED
	trainer_battle TRAINER_HACK_744, 0, 0, 0
	check_battle_won VAR_SPECIAL_RESULT
	compare VAR_SPECIAL_RESULT, 0
	goto_if_eq {label}_lost
	npc_msg {m1}
	giveitem ITEM_KEY_STONE, 1, VAR_SPECIAL_RESULT
	play_fanfare SEQ_ME_KEYITEM
	npc_msg {m2}
	wait_fanfare
	npc_msg {m3}
	giveitem ITEM_AMPHAROSITE, 1, VAR_SPECIAL_RESULT
	play_fanfare SEQ_ME_ITEM
	npc_msg {m4}
	wait_fanfare
	setflag {done}
	npc_msg {m5}
	wait_button_or_walk_away
	closemsg
	releaseall
	end

{label}_done:
	npc_msg {m6}
	wait_button_or_walk_away
	closemsg
	releaseall
	end

{label}_lost:
	clearflag FLAG_MEGA_EVOLUTION_ENABLED
	white_out
	releaseall
	end
"""

# the map's load script shows its objects; Korrina is hidden there until Jasmine has left
LOAD_SCRIPT_OLD = "scr_seq_D27R0107_004:\n"
LOAD_SCRIPT_NEW = """scr_seq_D27R0107_004:
	goto_if_set {gone}, scr_seq_D27R0107_004_original // hack: Korrina only appears after Amphy is cured
	hide_person {obj}
scr_seq_D27R0107_004_original:
"""


def main():
    dry_run = "--dry-run" in sys.argv
    map_files = MapFiles(MAP)
    if any(e["id"] == OBJECT for e in map_files.events["object_events"]):
        print("Korrina is already in the lighthouse, nothing to do")
        return
    spot = Maps().find_spot(MAP, map_files.events, near=(10, 10))  # close to Amphy and the stairs
    if spot is None:
        sys.exit("no free spot in the light room")
    messages = {f"m{i}": FIRST_LINE + i for i in range(len(LINES))}
    label = map_files.add(OBJECT, "SPRITE_GSGIRL3", spot[1], spot[2], SCRIPT, done=DONE_FLAG, **messages)
    assert LOAD_SCRIPT_OLD in map_files.script
    map_files.script = map_files.script.replace(LOAD_SCRIPT_OLD, LOAD_SCRIPT_NEW.format(gone=JASMINE_GONE, obj=OBJECT), 1)
    text = TEXT.read_bytes()
    assert text.count(b"\r\n") == FIRST_LINE, "the text archive changed: check FIRST_LINE"
    print(f"Korrina at ({spot[1]}, {spot[2]}), script {label}, messages {FIRST_LINE} to {FIRST_LINE + len(LINES) - 1}")
    if not dry_run:
        map_files.save()
        TEXT.write_bytes(text + ("\r\n".join(LINES) + "\r\n").encode())


if __name__ == "__main__":
    main()
