#!/usr/bin/env python3
"""Automated in-game tests of the hack features, run headless in DeSmuME.

Needs a ROM built with `make HACK_TEST=Y` (hack/scripts/test.sh does everything) and a save file
that continues in the overworld (the hg-engine test save works).

Usage: .venv/bin/python hack/scripts/ingame_tests.py [--rom test.nds] [--sav test.sav]
                                                     [--out hack/out/tests] [--window [--speed 2]]
                                                     [scenario ...]

--window opens the DeSmuME window so that the run can be watched (--speed 1 is real time).

Every scenario runs in its own process: src/hack_test.c builds a known party/bag state, common
script 2073 starts a battle or a shop, this script presses the buttons and then checks the report
that the game keeps in memory.  Screenshots of every step go to the output folder.
"""
import argparse
import ctypes
import math
import os
import struct
import subprocess
import sys
import time

# headless unless --window is given: then DeSmuME opens a window and the run can be watched
WINDOW = "--window" in sys.argv
if not WINDOW:
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

SPEED = 2.0  # --speed: emulation speed of the window mode, 0 = as fast as possible
for index, argument in enumerate(sys.argv):
    if argument == "--speed" and index + 1 < len(sys.argv):
        SPEED = float(sys.argv[index + 1])

HOLE = 0x02FFF81C
REQUEST_MAGIC = 0xC0DE0000
REPORT_MAGIC = 0x53544B48
REPORT_SIZE = 28 + 6 * 16 + 24 + 24 + 4
EGG_ROLLS = 1000
SHINY_SAMPLES = 1500
SHINY_TEST_ODDS = 2049 / 65536  # HACK_TEST builds use SHINY_ODDS 2048, see include/config.h

SCENARIOS = {
    "exp_share_on": 1,
    "exp_share_off": 2,
    "no_level_cap": 3,
    "shop": 4,
    "bottle_caps": 5,
    "exp_share_toggle": 6,
    "exp_share_switch": 7,
    "switch_no_share": 8,
    "shiny_charm": 9,
    "day_care": 10,
    "bike": 11,
    "static_mon": 12,
    "capture_prompt": 13,
    "capture_prompt_no": 14,
    "capture_prompt_cancel": 14,
    "capture_prompt_mail": 15,
    "mirror": 16,
    "mirror_no_mon": 17,
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
        self.window = None
        self.pump_events = None
        if WINDOW:
            self.window = self.emu.create_sdl_window(auto_pause=False)
            # macOS only shows an SDL window once its events are pumped.  the window's own input
            # handling is not used: it would overwrite the buttons and touches of the test
            try:
                self.pump_events = ctypes.CDLL(None).SDL_PumpEvents
            except (AttributeError, OSError):
                self.pump_events = None
        self.frame_time = 1 / (60 * SPEED) if SPEED > 0 else 0
        self.next_frame = time.monotonic()
        self.out = out
        self.shot_index = 0
        self.report_addr = None
        os.makedirs(out, exist_ok=True)

    # emulator helpers -----------------------------------------------------------------------
    def run(self, frames=1):
        for _ in range(frames):
            self.emu.cycle(False)
            if self.window is not None:
                if self.pump_events is not None:
                    self.pump_events()
                self.window.draw()
                # keep the chosen speed (1 = real time) so that the run can be followed
                self.next_frame += self.frame_time
                delay = self.next_frame - time.monotonic()
                if delay > 0:
                    time.sleep(delay)
                else:
                    self.next_frame = time.monotonic()

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
        magic, ticks, scenario, party_count, level_cap, money, badges, owned, disabled, static_flag, caps, gold_caps, mints, compat = struct.unpack_from(
            "<IIHBBIBBBBHHHH", raw, 0
        )
        mons = []
        for i in range(party_count):
            species, level, is_egg, exp, hp = struct.unpack_from("<HBBIH", raw, 28 + i * 16)
            ivs = list(raw[28 + i * 16 + 10:28 + i * 16 + 16])
            mons.append({"species": species, "level": level, "egg": is_egg, "exp": exp, "hp": hp, "ivs": ivs})
        shiny = struct.unpack_from("<6I", raw, 28 + 6 * 16)
        eggs = struct.unpack_from("<6I", raw, 28 + 6 * 16 + 24)
        x, z = struct.unpack_from("<hh", raw, 28 + 6 * 16 + 48)
        return {
            "x": x, "z": z, "static_flag": static_flag,
            "compatibility": compat, "egg_rolls": eggs[0:2], "eggs": eggs[2:4], "shiny_eggs": eggs[4:6],
            "shiny_total": shiny[:3], "shiny_hits": shiny[3:],
            "ticks": ticks, "scenario": scenario, "level_cap": level_cap, "money": money, "badges": badges,
            "exp_share_owned": owned, "exp_share_disabled": disabled, "bottle_caps": caps,
            "gold_bottle_caps": gold_caps, "mints": mints, "mons": mons,
        }

    def field_is_running(self, frames=40):
        """the report tick counter only advances while the player can move in the overworld"""
        before = self.report()["ticks"]
        self.run(frames)
        # the counter stands still in battles and full screen menus; in the overworld it can advance
        # slower than once per frame, so any clear progress counts
        return self.report()["ticks"] - before > frames // 8

    def wait_field(self, timeout=1800):
        for _ in range(timeout // 40):
            if self.field_is_running():
                return True
        return False

    def back_to_field(self, timeout=1500):
        """press B until the menus are closed and the player can move again"""
        for _ in range(timeout // 60):
            if self.field_is_running(30):
                return True
            self.press(self.Keys.KEY_B, wait=26)
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
            if moved < 4:
                left_field = True
            elif left_field and self.field_is_running(60):
                return True
            if frames in shots:
                self.shot(f"frame{frames}")
            if os.environ.get("HACK_TEST_DEBUG") and frames % 300 == 0:
                print(f"  debug: frame {frames} ticks moved {moved} left_field {left_field}")
                self.shot(f"debug{frames}")
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


def test_no_level_cap(game, c):
    """the hack has no level cap: with 0 badges a level 13 lead and its bench still gain experience"""
    before = game.report()
    c.check("no badges", before["badges"] == 0, f"{before['badges']}")
    c.check("no level cap", before["level_cap"] == 100, f"cap {before['level_cap']}")
    c.check("battle finished", battle(game))
    after = game.report()
    gain = gains(before, after)
    levels = [m["level"] for m in before["mons"]]
    expected = [scaled_exp(RATTATA_BASE_EXP, WILD_LEVEL, level) for level in levels]
    print(f"  before {[(m['level'], m['exp']) for m in before['mons']]}")
    print(f"  after  {[(m['level'], m['exp']) for m in after['mons']]}")
    c.check("fighter gains the full experience", gain[0] == expected[0], f"{gain[0]} vs {expected[0]}")
    c.check("benched mon gains 50% and levels up", gain[1] == expected[1] // 2 and after["mons"][1]["level"] == 13,
            f"gain {gain[1]} vs {expected[1] // 2}, level {after['mons'][1]['level']}")
    c.check("low level mon gains 50%", gain[2] == expected[2] // 2, f"{gain[2]} vs {expected[2] // 2}")


def test_shop(game, c):
    """Goldenrod Dept. Store 4F: buy a Bottle Cap and an Adamant Mint from the second page"""
    before = game.report()
    game.run(300)
    game.shot("page1")
    game.touch(60, 176, wait=60)  # next page arrow
    game.shot("page2")
    for _ in range(6):  # Bottle Cap is the first item of page 2: select, quantity 1, confirm
        game.press(game.Keys.KEY_A, wait=150)
    game.shot("bought_bottle_cap")
    game.press(game.Keys.KEY_DOWN, wait=30)
    game.press(game.Keys.KEY_RIGHT, wait=30)  # Adamant Mint
    game.shot("adamant_mint")
    for _ in range(6):
        game.press(game.Keys.KEY_A, wait=150)
    game.shot("bought_mint")
    c.check("back in the overworld", game.back_to_field())
    after = game.report()
    c.check("one Bottle Cap bought", after["bottle_caps"] == 1, f"{after['bottle_caps']}")
    c.check("one Adamant Mint bought", after["mints"] == 1, f"{after['mints']}")
    c.check("20 000 each were paid", before["money"] - after["money"] == 40000, f"paid {before['money'] - after['money']}")


def open_bag(game):
    game.press(game.Keys.KEY_X, wait=40)
    game.touch(43, 118, wait=150)  # BAG icon of the touch menu


def use_selected_item_on(game, slot_moves):
    """bag cursor is on the item: USE, move to the party slot, confirm and wait for the message"""
    game.press(game.Keys.KEY_A, wait=60)
    game.press(game.Keys.KEY_A, wait=150)
    for key in slot_moves:
        game.press(key, wait=30)
    game.press(game.Keys.KEY_A, wait=90)
    path = game.shot("item_used")
    game.run(240)
    return path


def test_bottle_caps(game, c):
    keys = game.Keys
    before = game.report()
    c.check("setup IVs", before["mons"][0]["ivs"] == [5, 10, 31, 20, 31, 31], f"{before['mons'][0]['ivs']}")
    open_bag(game)
    game.shot("bag")
    use_selected_item_on(game, [])  # Bottle Cap on the level 50 Garchomp
    game.shot("after_bottle_cap")
    game.press(keys.KEY_RIGHT, wait=30)  # Gold Bottle Cap
    use_selected_item_on(game, [keys.KEY_RIGHT])  # on the level 50 Pidgeot
    game.shot("after_gold_bottle_cap")
    game.press(keys.KEY_LEFT, wait=30)  # Bottle Cap again
    use_selected_item_on(game, [keys.KEY_DOWN])  # on the level 49 Raticate: no effect
    c.check("back in the overworld", game.back_to_field())
    after = game.report()
    print(f"  IVs after: {[m['ivs'] for m in after['mons']]}, caps {after['bottle_caps']}, gold {after['gold_bottle_caps']}")
    c.check("Bottle Cap maxes only the lowest IV", after["mons"][0]["ivs"] == [31, 10, 31, 20, 31, 31])
    c.check("Gold Bottle Cap maxes every IV", after["mons"][1]["ivs"] == [31] * 6)
    c.check("no effect below level 50", after["mons"][2]["ivs"] == [0] * 6)
    c.check("one Bottle Cap used", after["bottle_caps"] == 2, f"{after['bottle_caps']} left")
    c.check("one Gold Bottle Cap used", after["gold_bottle_caps"] == 2, f"{after['gold_bottle_caps']} left")


def toggle_exp_share(game):
    open_bag(game)
    game.touch(240, 16, wait=60)  # key items pocket
    game.shot("key_items")
    game.press(game.Keys.KEY_A, wait=60)
    game.press(game.Keys.KEY_A, wait=300)  # USE: the bag closes and the common script runs
    game.shot("message1")
    game.press(game.Keys.KEY_A, wait=150)
    game.shot("message2")
    game.press(game.Keys.KEY_A, wait=150)
    game.press(game.Keys.KEY_B, wait=90)
    return game.back_to_field()


def test_exp_share_toggle(game, c):
    c.check("starts switched on", game.report()["exp_share_disabled"] == 0)
    c.check("first use returns to the overworld", toggle_exp_share(game))
    c.check("first use switches it off", game.report()["exp_share_disabled"] == 1)
    c.check("second use returns to the overworld", toggle_exp_share(game))
    c.check("second use switches it on again", game.report()["exp_share_disabled"] == 0)
    c.check("still owned", game.report()["exp_share_owned"] == 1)


def baton_pass_battle(game, c):
    """the lead uses Baton Pass into the second mon, which then wins the battle"""
    before = game.report()
    game.run(900)  # battle intro, until the FIGHT menu is up
    for _ in range(3):  # cursor, FIGHT, Baton Pass
        game.press(game.Keys.KEY_A, wait=60)
    game.run(600)  # Baton Pass animation, until the party screen is up
    game.shot("choose_mon")
    game.touch(192, 24, wait=90)  # second party slot
    game.shot("shift_menu")
    game.touch(128, 70, wait=90)  # SHIFT
    game.shot("shifted")
    c.check("battle finished", game.mash_until_field(game.Keys.KEY_A))
    game.shot("battle_end")
    gain = gains(before, game.report())
    full = scaled_exp(RATTATA_BASE_EXP, WILD_LEVEL, 40)
    bench = scaled_exp(RATTATA_BASE_EXP, WILD_LEVEL, 10)
    print(f"  gains {gain}, full value for level 40: {full}, for level 10: {bench}")
    c.check("first fighter gets half", gain[0] == full // 2, f"{gain[0]} vs {full // 2}")
    c.check("second fighter gets half", gain[1] == full // 2, f"{gain[1]} vs {full // 2}")
    return gain, bench


def test_exp_share_switch(game, c):
    gain, bench = baton_pass_battle(game, c)
    c.check("benched mon gets 50% of its own value", gain[2] == bench // 2, f"{gain[2]} vs {bench // 2}")


def test_switch_no_share(game, c):
    gain, _ = baton_pass_battle(game, c)
    c.check("benched mon gets nothing", gain[2] == 0, f"{gain[2]}")


def test_shiny_charm(game, c):
    """statistical: 1500 mons per phase with the raised odds of the test build, 3 rolls with the charm"""
    for _ in range(4000):
        report = game.report()
        if min(report["shiny_total"]) >= SHINY_SAMPLES:
            break
        game.run(30)
    total, hits = report["shiny_total"], report["shiny_hits"]
    base = SHINY_SAMPLES * SHINY_TEST_ODDS
    charm = SHINY_SAMPLES * (1 - (1 - SHINY_TEST_ODDS) ** 3)
    print(f"  generated {total}, shiny {hits}; expected about {base:.0f} without the charm and {charm:.0f} with it")
    c.check("all mons were generated", min(total) >= SHINY_SAMPLES, f"{total}")
    c.check("wild mons without the charm: base odds", 25 <= hits[0] <= 72, f"{hits[0]}")
    c.check("wild mons with the charm: 3 rolls", 100 <= hits[1] <= 175, f"{hits[1]}")
    c.check("gift mons with the charm: 3 rolls", 100 <= hits[2] <= 175, f"{hits[2]}")


def test_day_care(game, c):
    """statistical: 1000 egg rolls with compatibility 50, then 1000 with the Oval and Shiny Charms"""
    for _ in range(2000):
        report = game.report()
        if min(report["egg_rolls"]) >= EGG_ROLLS:
            break
        game.run(30)
    rolls, eggs, shiny = report["egg_rolls"], report["eggs"], report["shiny_eggs"]
    rates = [s / e if e else 0 for s, e in zip(shiny, eggs)]
    charm_rate = 1 - (1 - SHINY_TEST_ODDS) ** 3
    print(f"  compatibility {report['compatibility']}, rolls {rolls}, eggs {eggs}, shiny eggs {shiny}")
    print(f"  shiny rates {rates[0]:.3f} / {rates[1]:.3f}; expected about {SHINY_TEST_ODDS:.3f} / {charm_rate:.3f}")
    c.check("all rolls done", min(rolls) >= EGG_ROLLS, f"{rolls}")
    c.check("no charm: about 50% eggs", 430 <= eggs[0] <= 570, f"{eggs[0]}")
    c.check("Oval Charm: about 80% eggs", 740 <= eggs[1] <= 860, f"{eggs[1]}")
    c.check("no charm: base shiny odds on eggs", rates[0] <= 0.065, f"{rates[0]:.3f}")
    c.check("Shiny Charm: 3 rolls on eggs", 0.06 <= rates[1] <= 0.13, f"{rates[1]:.3f}")


def ride(game, key, frames):
    """hold a direction and return the player position after every frame"""
    positions = []
    game.emu.input.keypad_add_key(game.keymask(key))
    for _ in range(frames):
        game.run(1)
        report = game.report()
        positions.append((report["x"], report["z"]))
    game.emu.input.keypad_rm_key(game.keymask(key))
    game.run(40)
    return positions


def walk_to(game, x=None, z=None, tries=40):
    """walk along one axis until the player stands on the given coordinate"""
    keys = game.Keys
    for _ in range(tries):
        report = game.report()
        if x is not None and report["x"] != x:
            key = keys.KEY_LEFT if report["x"] > x else keys.KEY_RIGHT
        elif z is not None and report["z"] != z:
            key = keys.KEY_UP if report["z"] > z else keys.KEY_DOWN
        else:
            return True
        ride(game, key, 8)
    return False


def reload_cherrygrove(game):
    """map objects come from the save file until the map is loaded again: go in and out of the
    Pokémon Center of Cherrygrove City, whose door is at (564, 391)"""
    keys = game.Keys
    walk_to(game, x=565)
    walk_to(game, z=392)
    walk_to(game, x=564)
    ride(game, keys.KEY_UP, 30)
    game.run(200)
    game.shot("pokemon_center")
    ride(game, keys.KEY_DOWN, 40)
    game.run(200)


def fastest_tile_time(positions):
    """smallest number of frames between two consecutive tile changes"""
    changes = [i for i in range(1, len(positions)) if positions[i] != positions[i - 1]]
    gaps = [b - a for a, b in zip(changes, changes[1:])]
    return (min(gaps) if gaps else None), len(changes)


def test_bike(game, c):
    """the test save stands in Cherrygrove City with 7 free tiles to the west (east is a story trigger)"""
    keys = game.Keys
    open_bag(game)
    game.touch(240, 16, wait=60)  # key items pocket
    game.press(keys.KEY_RIGHT, wait=30)  # Bicycle is the second key item
    game.shot("bicycle_selected")
    game.press(keys.KEY_A, wait=60)
    game.press(keys.KEY_A, wait=200)  # USE
    c.check("back in the overworld", game.back_to_field())
    game.shot("on_bike")
    positions = ride(game, keys.KEY_LEFT, 50)
    changes = [i for i in range(1, len(positions)) if positions[i] != positions[i - 1]]
    gaps = [b - a for a, b in zip(changes, changes[1:])]
    game.shot("after_ride")
    print(f"  bike: {len(changes)} tiles, frames between tiles while accelerating: {gaps}")
    c.check("the bike accelerates over the first tiles", len(gaps) >= 5 and gaps[0] > gaps[-1], f"{gaps}")
    c.check("top speed is 2 frames per tile (vanilla: 4)", gaps[-2:] == [2, 2], f"{gaps[-2:]}")


def test_static_mon(game, c):
    """Cherrygrove City: a visible Yamper stands 5 tiles west of where the test save was made.
    map objects come from the save file until the map is loaded again, so the test first goes in
    and out of the Pokémon Center"""
    keys = game.Keys
    before = game.report()
    c.check("daily flag starts clear", before["static_flag"] == 0)
    reload_cherrygrove(game)
    # back down the same column to the row of the Pokémon, one tile to its right
    walk_to(game, x=565)
    walk_to(game, z=398)
    walk_to(game, x=564)
    positions = ride(game, keys.KEY_LEFT, 40)
    game.shot("in_front_of_the_mon")
    c.check("the Pokémon blocks the tile it stands on", positions[-1] == (564, 398), f"player at {positions[-1]}")
    game.press(keys.KEY_A, wait=200)
    game.shot("talked")
    c.check("battle finished", game.mash_until_field(keys.KEY_A, shots=(600,)))
    game.run(60)
    game.shot("after_battle")
    after = game.report()
    c.check("daily flag set after the battle", after["static_flag"] == 1)
    c.check("experience gained from the battle", after["mons"][0]["exp"] > before["mons"][0]["exp"],
            f"{after['mons'][0]['exp'] - before['mons'][0]['exp']}")
    positions = ride(game, keys.KEY_LEFT, 40)
    c.check("the Pokémon is gone: the tile is free", positions[-1][0] < 563, f"player x {positions[-1][0]}")
    game.shot("walked_through")


def catch_with_full_party(game, c):
    """catch the wild Rattata with a Master Ball and get back to the overworld, where the prompt starts"""
    before = game.report()
    c.check("party is full", len(before["mons"]) == 6)
    game.run(900)
    game.touch(40, 170, wait=100)   # BAG
    game.touch(192, 35, wait=100)   # POKé BALLS
    game.touch(64, 28, wait=100)    # Master Ball
    game.touch(104, 170, wait=300)  # USE
    game.shot("ball_thrown")
    # B skips the texts and the Pokédex page; the nickname question only takes a touch on "No"
    finished = False
    for _ in range(150):
        ticks = game.report()["ticks"]
        game.press(game.Keys.KEY_B, wait=26)
        game.touch(128, 138, wait=26)
        if game.report()["ticks"] - ticks > 10:
            finished = True
            break
    c.check("capture sequence finished", finished)
    game.run(120)
    game.press(game.Keys.KEY_A, wait=120)  # first page of the question
    game.run(120)
    game.shot("prompt")
    return before


RATTATA, GARCHOMP = 19, 445


def test_capture_prompt(game, c):
    """full party: the caught Rattata goes to the PC, the prompt swaps it with the chosen party member"""
    before = catch_with_full_party(game, c)
    c.check("the caught Pokémon went to the PC", game.report()["compatibility"] == RATTATA, f"{game.report()['compatibility']}")
    answer_yes_and_pick_first(game, lambda report: report["mons"][0]["species"] == RATTATA)
    game.shot("switched")
    game.press(game.Keys.KEY_A, wait=150)
    c.check("back in the overworld", game.back_to_field())
    after = game.report()
    species = [m["species"] for m in after["mons"]]
    print(f"  party before {[m['species'] for m in before['mons']]}, after {species}, in the PC slot: {after['compatibility']}")
    c.check("the caught Rattata is in the chosen party slot", species[0] == RATTATA and len(species) == 6)
    c.check("it has its level and HP", after["mons"][0]["level"] == 20 and after["mons"][0]["hp"] > 0,
            f"level {after['mons'][0]['level']}, hp {after['mons'][0]['hp']}")
    c.check("the rest of the party is unchanged", species[1:] == [m["species"] for m in before["mons"]][1:])
    c.check("the party member is in the PC slot now", after["compatibility"] == GARCHOMP, f"{after['compatibility']}")
    ride(game, game.Keys.KEY_LEFT, 30)
    game.shot("follower")  # the Pokémon behind the player should be the Rattata now


def answer_yes_and_pick_first(game, done):
    """A: rest of the question, YES, first party member, final message.  stops when done(report) is true"""
    for step in range(12):
        game.press(game.Keys.KEY_A, wait=150)
        if step in (1, 2, 3, 4, 5):
            game.shot(f"answer{step}")
        if done(game.report()):
            break


def test_capture_prompt_cancel(game, c):
    """answering yes and then cancelling on the party screen changes nothing"""
    before = catch_with_full_party(game, c)
    game.press(game.Keys.KEY_A, wait=150)
    game.press(game.Keys.KEY_A, wait=300)  # YES: the party screen opens
    game.shot("party_screen")
    game.press(game.Keys.KEY_B, wait=300)  # cancel
    game.shot("cancelled")
    c.check("back in the overworld", game.back_to_field())
    after = game.report()
    c.check("party unchanged", [m["species"] for m in after["mons"]] == [m["species"] for m in before["mons"]])
    c.check("the caught Pokémon stays in the PC", after["compatibility"] == RATTATA, f"{after['compatibility']}")


def test_capture_prompt_mail(game, c):
    """the chosen party member holds Mail: like the PC, the swap is refused with a message"""
    before = catch_with_full_party(game, c)
    answer_yes_and_pick_first(game, lambda report: False)
    game.shot("refused")
    c.check("back in the overworld", game.back_to_field())
    after = game.report()
    c.check("party unchanged", [m["species"] for m in after["mons"]] == [m["species"] for m in before["mons"]])
    c.check("the caught Pokémon stays in the PC", after["compatibility"] == RATTATA, f"{after['compatibility']}")


def test_capture_prompt_no(game, c):
    """answering no leaves the party alone and the caught Pokémon in the PC"""
    before = catch_with_full_party(game, c)
    game.press(game.Keys.KEY_B, wait=200)  # NO
    game.shot("answered_no")
    c.check("back in the overworld", game.back_to_field())
    after = game.report()
    c.check("party unchanged", [m["species"] for m in after["mons"]] == [m["species"] for m in before["mons"]])
    c.check("the caught Pokémon stays in the PC", after["compatibility"] == RATTATA, f"{after['compatibility']}")


MANTINE = 226


def go_to_mantine_specialist(game):
    """Cherrygrove City: reload the map through the Pokémon Center, then walk to the tile west of the
    specialist at (566, 408)"""
    keys = game.Keys
    reload_cherrygrove(game)
    # down the path west of the house, then east along the row of the specialist
    steps = [walk_to(game, x=564), walk_to(game, z=408), walk_to(game, x=565)]
    ride(game, keys.KEY_RIGHT, 6)  # face the specialist
    report = game.report()
    print(f"  player at ({report['x']}, {report['z']})")
    game.shot("at_specialist")
    return all(steps) and (report["x"], report["z"]) == (565, 408)


def test_mirror(game, c):
    """the Mantine specialist battles the Mantine of the party one on one and rewards the win"""
    before = game.report()
    c.check("reached the specialist", go_to_mantine_specialist(game))
    game.press(game.Keys.KEY_A, wait=200)
    game.shot("intro")
    game.press(game.Keys.KEY_A, wait=200)
    game.press(game.Keys.KEY_A, wait=600)
    game.shot("battle")
    c.check("battle finished", game.mash_until_field(game.Keys.KEY_A, shots=(300, 900)))
    for step in range(6):
        game.press(game.Keys.KEY_A, wait=150)
        if step < 3:
            game.shot(f"reward{step}")
    c.check("back in the overworld", game.back_to_field())
    after = game.report()
    species = [m["species"] for m in after["mons"]]
    print(f"  party {species}, Mantine exp {before['mons'][1]['exp']} -> {after['mons'][1]['exp']}, reward {after['mints']}, wins {after['compatibility']}")
    c.check("the party is back, in the same order", species == [m["species"] for m in before["mons"]])
    c.check("only the Mantine battled", after["mons"][1]["exp"] > before["mons"][1]["exp"] and after["mons"][0]["exp"] == before["mons"][0]["exp"])
    c.check("reward received", after["mints"] == 1, f"{after['mints']}")
    c.check("win counted", after["compatibility"] == 1, f"{after['compatibility']}")
    game.press(game.Keys.KEY_A, wait=250)  # talk again: no second battle
    game.shot("talk_again")
    for _ in range(3):
        game.press(game.Keys.KEY_A, wait=150)
    c.check("back in the overworld", game.back_to_field())
    again = game.report()
    c.check("no second battle or reward", again["mints"] == 1 and again["compatibility"] == 1 and again["mons"][1]["exp"] == after["mons"][1]["exp"])


def test_mirror_no_mon(game, c):
    """without a Mantine the specialist only explains the rule"""
    before = game.report()
    c.check("reached the specialist", go_to_mantine_specialist(game))
    game.press(game.Keys.KEY_A, wait=250)
    game.shot("refusal")
    for _ in range(4):
        game.press(game.Keys.KEY_A, wait=150)
    c.check("back in the overworld", game.back_to_field())
    after = game.report()
    c.check("nothing happened", after["mints"] == 0 and after["compatibility"] == 0
            and [m["exp"] for m in after["mons"]] == [m["exp"] for m in before["mons"]])


TESTS = {
    "exp_share_on": test_exp_share_on,
    "exp_share_off": test_exp_share_off,
    "no_level_cap": test_no_level_cap,
    "shop": test_shop,
    "bottle_caps": test_bottle_caps,
    "exp_share_toggle": test_exp_share_toggle,
    "exp_share_switch": test_exp_share_switch,
    "switch_no_share": test_switch_no_share,
    "shiny_charm": test_shiny_charm,
    "day_care": test_day_care,
    "bike": test_bike,
    "static_mon": test_static_mon,
    "capture_prompt": test_capture_prompt,
    "capture_prompt_no": test_capture_prompt_no,
    "capture_prompt_cancel": test_capture_prompt_cancel,
    "capture_prompt_mail": test_capture_prompt_mail,
    "mirror": test_mirror,
    "mirror_no_mon": test_mirror_no_mon,
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
    parser.add_argument("--window", action="store_true", help="open the emulator window to watch the run")
    parser.add_argument("--speed", type=float, default=2.0, help="speed of the window mode (1 = real time, 0 = unlimited)")
    parser.add_argument("scenarios", nargs="*", default=[])
    args = parser.parse_args()
    names = args.scenarios or list(TESTS)

    if args.single:
        sys.exit(1 if run_one(args, names[0]) else 0)

    failed = []
    for name in names:
        command = [sys.executable, __file__, "--rom", args.rom, "--sav", args.sav, "--out", args.out, "--single", name]
        if args.window:
            command += ["--window", "--speed", str(args.speed)]
        result = subprocess.run(command)
        if result.returncode != 0:
            failed.append(name)
    print(f"\n{len(names) - len(failed)}/{len(names)} scenarios passed" + (f"; FAILED: {', '.join(failed)}" if failed else ""))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
