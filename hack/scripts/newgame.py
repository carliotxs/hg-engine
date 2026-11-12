#!/usr/bin/env python3
"""Smoke test of a new game on the normal ROM: intro, New Bark Town, Elm's lab and the starter choice.

Usage: .venv/bin/python hack/scripts/newgame.py [test.nds] [out_dir] [starter 0-2]

The inputs are a fixed recording (button mashing through the dialogue, a few walks), so this breaks
if the opening scripts or maps change; re-record the steps then.  It fails when the game hangs before
the starter is received.  Look at the screenshots in the output folder to check sprites and text:
they show the three starters, the confirmation and the "received" message.
"""
import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

from desmume.controls import Keys, keymask  # noqa: E402
from desmume.emulator import DeSmuME  # noqa: E402

rom = sys.argv[1] if len(sys.argv) > 1 else "test.nds"
out = sys.argv[2] if len(sys.argv) > 2 else "hack/out/newgame"
starter = int(sys.argv[3]) if len(sys.argv) > 3 else 1
os.makedirs(out, exist_ok=True)

KEYS = {"A": Keys.KEY_A, "U": Keys.KEY_UP, "D": Keys.KEY_DOWN, "L": Keys.KEY_LEFT, "R": Keys.KEY_RIGHT}

# W<n>: wait n frames; A<n>: press A n times; H<dir><n>: hold a direction n frames; T<x>,<y>: touch;
# R: press right; S<name>: screenshot
STEPS = (
    "W900 A6 W300 Stitle_menu T128,152 W200 "  # title screen, "NO INFO NEEDED"
    "A102 A24 W300 A8 W300 A4 W200 Sbedroom "  # Oak's speech, boy, default name "AAAAAAA"
    "HU18 HL70 W150 A6 W100 HL40 HU20 HL40 W120 HD20 HL40 W200 "  # to the stairs
    "A40 W100 HD140 W200 A30 W100 HD140 W200 Snew_bark "  # mom, out of the house
    "W200 A6 HL64 HL64 HL64 HL64 W300 A6 W200 "  # Marill and the friend
    "HL96 HL96 HU64 HL96 HR17 HU40 HR17 HU40 HR17 HU40 HR17 HU40 Slab "  # to the lab door
    "W100 HU120 A60 W200 A10 W200 A40 W200 HR70 HU40 A1 W200 W200 "  # Elm, to the machine
    "A1 W200 Sstarter_0 R W80 Sstarter_2 R W80 Sstarter_1"  # the three balls: 0, 2, 1
).split()
CHOOSE = {0: "R W80", 1: "", 2: "R W80 R W80"}[starter].split() + "A1 W120 Sconfirm A1 W150 A1 W150 Sreceived A1 W200".split()

emu = DeSmuME()
emu.open(rom)


def run(frames):
    for _ in range(frames):
        emu.cycle(False)


def press(key, wait=40):
    emu.input.keypad_add_key(keymask(key))
    run(4)
    emu.input.keypad_rm_key(keymask(key))
    run(wait)


shots = {}
for step in list(STEPS) + CHOOSE:
    kind, arg = step[0], step[1:]
    if kind == "W":
        run(int(arg))
    elif kind == "A":
        for _ in range(int(arg)):
            press(Keys.KEY_A)
    elif kind == "R":
        press(Keys.KEY_RIGHT)
    elif kind == "H":
        emu.input.keypad_add_key(keymask(KEYS[arg[0]]))
        run(int(arg[1:]))
        emu.input.keypad_rm_key(keymask(KEYS[arg[0]]))
        run(20)
    elif kind == "T":
        x, y = arg.split(",")
        emu.input.touch_set_pos(int(x), int(y))
        run(4)
        emu.input.touch_release()
        run(60)
    elif kind == "S":
        image = emu.screenshot()
        image.save(os.path.join(out, f"{len(shots) + 1:02d}_{arg}.png"))
        shots[arg] = image

# the selection screen has a grey 3D top screen; after receiving the starter the lab is back and
# the POKéMON entry of the touch menu exists.  a hang leaves the selection screen (or a blank one) up
selection = shots["starter_1"].crop((0, 0, 256, 140)).convert("RGB")
received = shots["received"].crop((0, 0, 256, 140)).convert("RGB")
colours = len(received.getcolors(maxcolors=1 << 24))
different = sum(1 for a, b in zip(selection.getdata(), received.getdata()) if a != b)
print(f"screenshots in {out}; lab screen colours: {colours}, pixels changed since the selection screen: {different}")
if colours < 16 or different < 5000:
    print("FAIL: the game did not get back to the lab after choosing the starter")
    sys.exit(1)
print("OK: new game reaches the starter choice and the starter is received")
