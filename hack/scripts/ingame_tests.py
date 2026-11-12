#!/usr/bin/env python3
"""Automated in-game tests of the hack features, run headless in DeSmuME.

Needs a ROM built with `make HACK_TEST=Y` (hack/scripts/test.sh does everything) and a save file
that continues in the overworld (the hg-engine test save works).

Usage: .venv/bin/python hack/scripts/ingame_tests.py [--rom test.nds] [--sav test.sav]
                                                     [--out hack/out/tests] [scenario ...]

Every scenario runs in its own process: src/hack_test.c builds a known party/bag state, common
script 2073 starts a battle or a shop, this script presses the buttons and then checks the report
that the game keeps in memory.  Screenshots of every step go to the output folder.
"""
import argparse
import math
import os
import struct
import subprocess
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

HOLE = 0x02FFF81C
REQUEST_MAGIC = 0xC0DE0000
REPORT_MAGIC = 0x53544B48
REPORT_SIZE = 28 + 6 * 16

SCENARIOS = {
    "exp_share_on": 1,
    "exp_share_off": 2,
    "level_cap": 3,
    "shop": 4,
    "bottle_caps": 5,
    "exp_share_toggle": 6,
    "exp_share_switch": 7,
}

# base experience and growth data used by the expectations
RATTATA_BASE_EXP = 51
WILD_LEVEL = 20


class Game:
    def __init__(self, rom, sav, out):
        from desmume.controls import Keys, keymask
        from desmume.emulator import DeSmuME

        self.Keys = Keys
        self.keymask = keymask
        self.emu = DeSmuME()
        self.emu.open(rom)
        self.emu.backup.import_file(sav)
        self.out = out
        self.shot_index = 0
        self.report_addr = None
        os.makedirs(out, exist_ok=True)

    # emulator helpers -----------------------------------------------------------------------
    def run(self, frames=1):
        for _ in range(frames):
            self.emu.cycle(False)

    def press(self, key, hold=4, wait=20):
        self.emu.input.keypad_add_key(self.keymask(key))
        self.run(hold)
        self.emu.input.keypad_rm_key(self.keymask(key))
        self.run(wait)

    def touch(self, x, y, hold=4, wait=30):
        self.emu.input.touch_set_pos(x, y)
        self.run(hold)
        self.emu.input.touch_release()
        self.run(wait)

    def shot(self, name):
        self.shot_index += 1
        path = os.path.join(self.out, f"{self.shot_index:02d}_{name}.png")
        self.emu.screenshot().save(path)
        return path

    # report ---------------------------------------------------------------------------------
    def start_scenario(self, scenario, timeout=3000):
        """ask the game for a scenario and wait until it answers with the report address"""
        for _ in range(timeout):
            value = self.emu.memory.unsigned.read_long(HOLE)
            if 0x02000000 <= value < 0x02400000 and self.emu.memory.unsigned.read_long(value) == REPORT_MAGIC:
                self.report_addr = value
                return
            if value != (REQUEST_MAGIC | scenario):
                self.emu.memory.write_long(HOLE, REQUEST_MAGIC | scenario)
            self.run(1)
        self.shot("timeout")
        raise RuntimeError("the game never answered: is this a HACK_TEST=Y ROM and does the save continue in the overworld?")

    def report(self):
        raw = bytes(self.emu.memory.unsigned[self.report_addr:self.report_addr + REPORT_SIZE])
        magic, ticks, scenario, party_count, level_cap, money, badges, owned, disabled, _, caps, gold_caps, mints, _ = struct.unpack_from(
            "<IIHBBIBBBBHHHH", raw, 0
        )
        mons = []
        for i in range(party_count):
            species, level, is_egg, exp, hp = struct.unpack_from("<HBBIH", raw, 28 + i * 16)
            ivs = list(raw[28 + i * 16 + 10:28 + i * 16 + 16])
            mons.append({"species": species, "level": level, "egg": is_egg, "exp": exp, "hp": hp, "ivs": ivs})
        return {
            "ticks": ticks, "scenario": scenario, "level_cap": level_cap, "money": money, "badges": badges,
            "exp_share_owned": owned, "exp_share_disabled": disabled, "bottle_caps": caps,
            "gold_bottle_caps": gold_caps, "mints": mints, "mons": mons,
        }

    def field_is_running(self, frames=40):
        """the report tick counter only advances while the player can move in the overworld"""
        before = self.report()["ticks"]
        self.run(frames)
        return self.report()["ticks"] - before >= frames // 2

    def wait_field(self, timeout=1800):
        for _ in range(timeout // 40):
            if self.field_is_running():
                return True
        return False

    def mash_until_field(self, key, timeout=12000, shots=()):
        """press a button until control returns to the overworld (end of battle, closed menu...)"""
        frames = 0
        left_field = False
        while frames < timeout:
            before = self.report()["ticks"]
            self.press(key, hold=4, wait=26)
            frames += 30
            moved = self.report()["ticks"] - before
            if moved < 10:
                left_field = True
            elif left_field and self.field_is_running(60):
                return True
            if frames in shots:
                self.shot(f"frame{frames}")
        return False


# expectations -----------------------------------------------------------------------------------
def scaled_exp(base, enemy_level, own_level):
    """Gen 5 formula as implemented in Task_DistributeExp_Extend (integer maths, integer sqrt)"""
    total = base * enemy_level // 5
    top = (2 * enemy_level + 10) ** 2 * math.isqrt(2 * enemy_level + 10)
    bottom = (enemy_level + own_level + 10) ** 2 * math.isqrt(enemy_level + own_level + 10)
    return total * top // bottom


class Checker:
    def __init__(self):
        self.failures = 0

    def check(self, name, condition, detail=""):
        print(f"  [{'OK' if condition else 'FAIL'}] {name}{' (' + detail + ')' if detail else ''}")
        if not condition:
            self.failures += 1


def gains(before, after):
    return [a["exp"] - b["exp"] for b, a in zip(before["mons"], after["mons"])]


def battle(game):
    """fight the wild Rattata with the first move until the overworld comes back"""
    game.run(600)
    game.shot("battle_start")
    done = game.mash_until_field(game.Keys.KEY_A, shots=(900, 1800, 3000))
    game.shot("battle_end")
    return done


# scenarios --------------------------------------------------------------------------------------
def test_exp_share_on(game, c):
    before = game.report()
    c.check("battle finished", battle(game))
    after = game.report()
    gain = gains(before, after)
    levels = [m["level"] for m in before["mons"]]
    expected = [scaled_exp(RATTATA_BASE_EXP, WILD_LEVEL, level) for level in levels]
    print(f"  levels {levels} gains {gain} full formula values {expected}")
    c.check("level cap is 50 with 8 badges", before["level_cap"] == 50, f"cap {before['level_cap']}")
    c.check("fighter gets the full Gen 5 experience", gain[0] == expected[0], f"{gain[0]} vs {expected[0]}")
    c.check("benched level 20 gets 50%", gain[1] == max(1, expected[1] // 2), f"{gain[1]} vs {expected[1] // 2}")
    c.check("benched level 10 gets 50%", gain[2] == max(1, expected[2] // 2), f"{gain[2]} vs {expected[2] // 2}")
    c.check("fainted mon gets nothing", gain[3] == 0, f"{gain[3]}")


def test_exp_share_off(game, c):
    before = game.report()
    c.check("Exp. Share flag is off", before["exp_share_disabled"] == 1)
    c.check("battle finished", battle(game))
    gain = gains(before, game.report())
    expected = scaled_exp(RATTATA_BASE_EXP, WILD_LEVEL, before["mons"][0]["level"])
    print(f"  gains {gain}")
    c.check("fighter gets the full Gen 5 experience", gain[0] == expected, f"{gain[0]} vs {expected}")
    c.check("nobody else gets experience", gain[1:] == [0, 0, 0], f"{gain[1:]}")


def test_level_cap(game, c):
    before = game.report()
    c.check("level cap is 13 with 0 badges", before["level_cap"] == 13, f"cap {before['level_cap']}")
    c.check("battle finished", battle(game))
    after = game.report()
    gain = gains(before, after)
    print(f"  before {[(m['level'], m['exp']) for m in before['mons']]}")
    print(f"  after  {[(m['level'], m['exp']) for m in after['mons']]}")
    c.check("mon at the cap gains no experience", gain[0] == 0 and after["mons"][0]["level"] == 13, f"gain {gain[0]}")
    c.check("mon below the cap stops at the cap", after["mons"][1]["level"] == 13 and gain[1] == 1,
            f"level {after['mons'][1]['level']}, gain {gain[1]}")
    c.check("low level mon still gains experience", gain[2] > 0 and after["mons"][2]["level"] <= 13,
            f"gain {gain[2]}, level {after['mons'][2]['level']}")


def test_shop(game, c):
    game.run(300)
    game.shot("shop")
    c.check("not implemented yet", False)


def test_bottle_caps(game, c):
    game.run(120)
    game.shot("field")
    c.check("not implemented yet", False)


def test_exp_share_toggle(game, c):
    game.run(120)
    game.shot("field")
    c.check("not implemented yet", False)


def test_exp_share_switch(game, c):
    c.check("not implemented yet", False)


TESTS = {
    "exp_share_on": test_exp_share_on,
    "exp_share_off": test_exp_share_off,
    "level_cap": test_level_cap,
    "shop": test_shop,
    "bottle_caps": test_bottle_caps,
    "exp_share_toggle": test_exp_share_toggle,
    "exp_share_switch": test_exp_share_switch,
}


def run_one(args, name):
    game = Game(args.rom, args.sav, os.path.join(args.out, name))
    checker = Checker()
    print(f"{name}:")
    game.start_scenario(SCENARIOS[name])
    game.run(30)
    TESTS[name](game, checker)
    return checker.failures


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rom", default="test.nds")
    parser.add_argument("--sav", default="test.sav")
    parser.add_argument("--out", default="hack/out/tests")
    parser.add_argument("--single", action="store_true", help="internal: run one scenario in this process")
    parser.add_argument("scenarios", nargs="*", default=[])
    args = parser.parse_args()
    names = args.scenarios or list(TESTS)

    if args.single:
        sys.exit(1 if run_one(args, names[0]) else 0)

    failed = []
    for name in names:
        result = subprocess.run([sys.executable, __file__, "--rom", args.rom, "--sav", args.sav, "--out", args.out, "--single", name])
        if result.returncode != 0:
            failed.append(name)
    print(f"\n{len(names) - len(failed)}/{len(names)} scenarios passed" + (f"; FAILED: {', '.join(failed)}" if failed else ""))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
