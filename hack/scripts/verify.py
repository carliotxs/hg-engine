#!/usr/bin/env python3
"""Smoke test: boot the built ROM headless in DeSmuME and save screenshots.

Usage: .venv/bin/python hack/scripts/verify.py [test.nds] [out_dir]
Fails (exit 1) if the screen is still blank after boot, which catches most broken builds.
Needs py-desmume (installed in .venv by the hg-engine Makefile). On a machine without a display,
run with SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy.
"""
import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

from desmume.controls import Keys, keymask  # noqa: E402
from desmume.emulator import DeSmuME  # noqa: E402

rom = sys.argv[1] if len(sys.argv) > 1 else "test.nds"
out = sys.argv[2] if len(sys.argv) > 2 else "hack/out/verify"
os.makedirs(out, exist_ok=True)

emu = DeSmuME()
emu.open(rom)


def run(frames):
    for _ in range(frames):
        emu.cycle(with_joystick=False)


def press(key, hold=6):
    emu.input.keypad_add_key(keymask(key))
    run(hold)
    emu.input.keypad_rm_key(keymask(key))
    run(20)


run(900)
title = emu.screenshot()
title.save(os.path.join(out, "01_title.png"))
for _ in range(6):
    press(Keys.KEY_A)
    run(60)
run(300)
intro = emu.screenshot()
intro.save(os.path.join(out, "02_intro.png"))

colours = len(intro.convert("RGB").getcolors(maxcolors=1 << 24))
print(f"screenshots in {out}; distinct colours on intro screen: {colours}")
if colours < 4:
    print("FAIL: screen looks blank, the ROM probably does not boot")
    sys.exit(1)
print("OK: ROM boots")
