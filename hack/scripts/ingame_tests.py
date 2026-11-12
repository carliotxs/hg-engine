#!/usr/bin/env python3
"""Automated in-game tests of the hack features, run headless in DeSmuME.

Needs a ROM built with `make HACK_TEST=Y` (hack/scripts/test.sh does everything) and a save file
that continues in the overworld (the hg-engine test save works).

Usage: .venv/bin/python hack/scripts/ingame_tests.py [--rom test.nds] [--sav test.sav]
                                                     [--out hack/out/tests] [--speed 6] [--headless]
                                                     [scenario ...]

The DeSmuME window is open by default so that the run can be watched, at 6 times real speed
(--speed 1 is real time, --speed 0 unlimited).  --headless runs without a window.

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

# the DeSmuME window is on by default so that the run can be watched; --headless switches it off.
# while somebody is playing a chapter (play.sh), tests run without a window: a window that opens on
# top of the game steals the keyboard focus and leaves keys stuck
WINDOW = "--headless" not in sys.argv
if WINDOW and "--play" not in sys.argv:
    playing = subprocess.run(["pgrep", "-f", "ingame_tests.py.*--play"], capture_output=True).stdout.split()
    if any(int(pid) != os.getpid() for pid in playing):
        WINDOW = False
if not WINDOW:
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

SPEED = 6.0  # --speed: emulation speed of the window mode, 0 = as fast as possible
for index, argument in enumerate(sys.argv):
    if argument == "--speed" and index + 1 < len(sys.argv):
        SPEED = float(sys.argv[index + 1])

HOLE = 0x02FFF81C
REQUEST_MAGIC = 0xC0DE0000
REPORT_MAGIC = 0x53544B48
REPORT_SIZE = 28 + 6 * 16 + 24 + 24 + 4 + 8 + 8
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
    "leader": 18,
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
        x, z, key_stone, ampharosite, mega_enabled = struct.unpack_from("<hhHHH", raw, 28 + 6 * 16 + 48)
        elixirs, kangaskhanite, giovanni_done = struct.unpack_from("<HHH", raw, 28 + 6 * 16 + 60)
        return {
            "elixirs": elixirs, "kangaskhanite": kangaskhanite, "giovanni_done": giovanni_done,
            "x": x, "z": z, "key_stone": key_stone, "ampharosite": ampharosite, "mega_enabled": mega_enabled, "static_flag": static_flag,
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
    # the position is sampled once per frame, so two tiles in four frames can read as 2+2 or 1+3
    c.check("top speed is 2 frames per tile (vanilla: 4)", sum(gaps[-2:]) == 4, f"{gaps[-2:]}")


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


def test_leader(game, c):
    """trainer battle against Falkner: the screenshots show his new team (Rookidee, Fletchling, Pidgeotto)"""
    before = game.report()
    game.run(700)
    game.shot("leader_intro")
    shots = tuple(range(300, 6000, 300))
    c.check("battle finished", game.mash_until_field(game.Keys.KEY_A, timeout=9000, shots=shots))
    game.shot("battle_end")
    after = game.report()
    gain = after["mons"][0]["exp"] - before["mons"][0]["exp"]
    expected = sum(scaled_exp(base, level, 40) * 3 // 2 for base, level in ((53, 11), (56, 12), (122, 15)))
    print(f"  experience gained {gain}; three Pokémon of levels 11, 12 and 15 give about {expected} (trainer bonus included)")
    c.check("three Pokémon were beaten", 0.6 * expected <= gain <= 1.5 * expected, f"{gain} vs {expected}")
    c.check("money received", after["money"] > before["money"], f"{after['money'] - before['money']}")


def test_chapter_view(game, c):
    """only opens the chapter: the screenshot shows where the player stands"""
    report = game.report()
    print(f"  player at ({report['x']}, {report['z']}), badges {report['badges']}, party {[m['species'] for m in report['mons']]}")
    c.check("the chapter loaded", len(report["mons"]) > 0)


def test_korrina(game, c):
    """top of the Olivine Lighthouse after Amphy is cured: Korrina battles and gives the Key Stone"""
    before = game.report()
    place = (before["x"], before["z"])
    c.check("no Key Stone and no Mega Evolution yet", before["key_stone"] == 0 and before["mega_enabled"] == 0)
    game.press(game.Keys.KEY_A, wait=150)
    game.shot("korrina_intro")
    for step in range(8):
        game.press(game.Keys.KEY_A, wait=120)
    game.run(400)
    game.shot("korrina_battle")
    c.check("battle finished", game.mash_until_field(game.Keys.KEY_A, timeout=15000, shots=(300, 1200, 2400, 3600, 4800)))
    for step in range(16):
        game.press(game.Keys.KEY_A, wait=150)
        if step in (0, 2, 4, 6, 8):
            game.shot(f"korrina_after{step}")
    c.check("back in the overworld", game.back_to_field())
    after = game.report()
    print(f"  experience gained {after['mons'][0]['exp'] - before['mons'][0]['exp']}, Key Stone {after['key_stone']}, "
          f"Ampharosite {after['ampharosite']}, Mega Evolution flag {after['mega_enabled']}")
    c.check("the battle was won (still in the light room)", (after["x"], after["z"]) == place, f"({after['x']}, {after['z']})")
    c.check("Key Stone received", after["key_stone"] == 1)
    c.check("Ampharosite received", after["ampharosite"] == 1)
    c.check("Mega Evolution enabled", after["mega_enabled"] == 1)
    game.press(game.Keys.KEY_A, wait=200)
    game.shot("korrina_again")
    for _ in range(4):
        game.press(game.Keys.KEY_A, wait=150)
    again = game.report() if game.back_to_field() else None
    c.check("no second battle and no second Key Stone", again is not None and again["key_stone"] == 1
            and again["mons"][0]["exp"] == after["mons"][0]["exp"])


def test_rocket_grunt(game, c):
    """an extra Team Rocket grunt: battles when talked to, once"""
    before = game.report()
    place = (before["x"], before["z"])
    game.shot("grunt")
    game.press(game.Keys.KEY_A, wait=200)
    game.shot("grunt_intro")
    game.press(game.Keys.KEY_A, wait=200)
    game.press(game.Keys.KEY_A, wait=500)
    c.check("battle finished", game.mash_until_field(game.Keys.KEY_A, timeout=12000, shots=(300, 1500)))
    for step in range(5):
        game.press(game.Keys.KEY_A, wait=150)
    c.check("back in the overworld", game.back_to_field())
    after = game.report()
    gain = after["mons"][0]["exp"] - before["mons"][0]["exp"]
    print(f"  experience gained {gain}, money {after['money'] - before['money']}")
    c.check("the battle was won", gain > 0 and (after["x"], after["z"]) == place and after["money"] > before["money"])
    game.press(game.Keys.KEY_A, wait=250)
    game.shot("grunt_again")
    for _ in range(3):
        game.press(game.Keys.KEY_A, wait=150)
    again = game.report() if game.back_to_field() else None
    c.check("no second battle", again is not None and again["mons"][0]["exp"] == after["mons"][0]["exp"])


def test_giovanni(game, c):
    """hidden cave of Tohjo Falls after the Radio Tower: Giovanni battles, leaves the Kangaskhanite and goes"""
    before = game.report()
    place = (before["x"], before["z"])
    game.shot("giovanni")
    for step in range(9):
        game.press(game.Keys.KEY_A, wait=150)
        if step in (0, 3):
            game.shot(f"giovanni_intro{step}")
    game.run(400)
    c.check("battle finished", game.mash_until_field(game.Keys.KEY_A, timeout=20000, shots=(300, 2400, 6000)))
    for step in range(12):
        game.press(game.Keys.KEY_A, wait=150)
        if step in (0, 3, 6):
            game.shot(f"giovanni_after{step}")
    game.run(300)
    c.check("back in the overworld", game.back_to_field())
    after = game.report()
    game.shot("giovanni_gone")
    print(f"  experience gained {after['mons'][0]['exp'] - before['mons'][0]['exp']}, Kangaskhanite {after['kangaskhanite']}, done {after['giovanni_done']}")
    c.check("the battle was won (still in the cave)", (after["x"], after["z"]) == place)
    c.check("Kangaskhanite received", after["kangaskhanite"] == 1)
    c.check("Giovanni is done", after["giovanni_done"] == 1)
    game.press(game.Keys.KEY_A, wait=200)
    game.shot("giovanni_talk_again")
    c.check("he is gone: nothing to talk to", game.field_is_running() and game.report()["mons"][0]["exp"] == after["mons"][0]["exp"])


def test_mart_robber(game, c):
    """random event: on its day a grunt robs the Poké Mart; beating him gets an Elixir, once a day"""
    before = game.report()
    game.shot("robber")
    for step in range(5):
        game.press(game.Keys.KEY_A, wait=150)
        if step == 1:
            game.shot("robber_intro")
    game.run(400)
    c.check("battle finished", game.mash_until_field(game.Keys.KEY_A, timeout=12000, shots=(300,)))
    for step in range(8):
        game.press(game.Keys.KEY_A, wait=150)
        if step in (0, 2, 4):
            game.shot(f"robber_after{step}")
    c.check("back in the overworld", game.back_to_field())
    after = game.report()
    print(f"  experience gained {after['mons'][0]['exp'] - before['mons'][0]['exp']}, Elixirs {before['elixirs']} -> {after['elixirs']}")
    c.check("the battle was won", after["mons"][0]["exp"] > before["mons"][0]["exp"])
    c.check("Elixir received", after["elixirs"] == before["elixirs"] + 1)
    game.press(game.Keys.KEY_A, wait=200)
    game.shot("robber_talk_again")
    c.check("he is gone: nothing to talk to", game.field_is_running() and game.report()["elixirs"] == after["elixirs"])


def test_visitor(game, c):
    """a famous visitor on its day: battles once, gives its reward and leaves until the next time"""
    before = game.report()
    place = (before["x"], before["z"])
    game.shot("visitor")
    for step in range(8):
        game.press(game.Keys.KEY_A, wait=150)
        if step == 0:
            game.shot("visitor_intro")
    game.run(400)
    c.check("battle finished", game.mash_until_field(game.Keys.KEY_A, timeout=20000, shots=(300, 3000)))
    for step in range(10):
        game.press(game.Keys.KEY_A, wait=150)
        if step in (0, 2, 4):
            game.shot(f"visitor_after{step}")
    game.run(300)
    c.check("back in the overworld", game.back_to_field())
    after = game.report()
    game.shot("visitor_gone")
    gain = after["mons"][0]["exp"] - before["mons"][0]["exp"]
    print(f"  experience gained {gain}, money {after['money'] - before['money']}")
    c.check("the battle was won", gain > 0 and (after["x"], after["z"]) == place and after["money"] > before["money"])
    game.press(game.Keys.KEY_A, wait=200)
    c.check("the visitor left: nothing to talk to", game.field_is_running() and game.report()["mons"][0]["exp"] == after["mons"][0]["exp"])


# tests that start in a chapter: name -> (chapter, function)
CHAPTER_TESTS = {
    # one "view" test per chapter: opens it and takes a screenshot
    **{f"view_{name}": (name, test_chapter_view) for name in (
        "lighthouse_korrina", "mahogany_rocket", "lake_rocket", "route43_rocket", "goldenrod_takeover",
        "union_cave_specialist", "route31_static", "tohjo_giovanni", "mart_robber", "lake_wake")},
    "korrina": ("lighthouse_korrina", test_korrina),
    "giovanni": ("tohjo_giovanni", test_giovanni),
    "mart_robber": ("mart_robber", test_mart_robber),
    "visitor_wake": ("lake_wake", test_visitor),
    "rocket_mahogany": ("mahogany_rocket", test_rocket_grunt),
    "rocket_lake": ("lake_rocket", test_rocket_grunt),
    "rocket_route43": ("route43_rocket", test_rocket_grunt),
    "rocket_goldenrod": ("goldenrod_takeover", test_rocket_grunt),
}


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
    "leader": test_leader,
}


CHAPTER_BASE = 100  # scenario number of chapter 0, see hack/scripts/gen_chapters.py


def chapter_number(name):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from gen_chapters import CHAPTERS
    return [chapter["name"] for chapter in CHAPTERS].index(name)


def start_chapter(game, name):
    """ask the debug ROM for a chapter and wait until the player stands there"""
    game.start_scenario(CHAPTER_BASE + chapter_number(name))
    start = (game.report()["x"], game.report()["z"])
    for _ in range(60):  # fade out, warp, fade in: wait until the player is somewhere else
        game.run(30)
        report = game.report()
        if (report["x"], report["z"]) != start:
            break
    game.run(240)
    game.shot(f"chapter_{name}")


# play mode keyboard: SDL scancode -> DS key.  the key handling that ships with the DeSmuME window is
# not used: its fixed mapping is wrong on macOS (an arrow key ends up closing the DS lid)
PLAY_KEYS = {
    79: "KEY_RIGHT", 80: "KEY_LEFT", 81: "KEY_DOWN", 82: "KEY_UP",  # arrows
    27: "KEY_A", 29: "KEY_B", 22: "KEY_X", 4: "KEY_Y",              # X, Z, S, A
    20: "KEY_L", 26: "KEY_R", 40: "KEY_START", 229: "KEY_SELECT",   # Q, W, Enter, right Shift
}
SDL_QUIT = 0x100


def play(args):
    """open a chapter and hand the game over to the keyboard and mouse until the window is closed"""
    game = Game(args.rom, args.sav, os.path.join(args.out, "play"))
    if game.window is None:
        sys.exit("--play needs the window: do not combine it with --headless")
    start_chapter(game, args.play)
    game.frame_time = 1 / 60  # real time from here on
    sdl = ctypes.CDLL(None)
    sdl.SDL_GetKeyboardState.restype = ctypes.POINTER(ctypes.c_uint8)
    sdl.SDL_GetKeyboardFocus.restype = ctypes.c_void_p
    sdl.SDL_GetWindowSize.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
    masks = {scancode: game.keymask(getattr(game.Keys, name)) for scancode, name in PLAY_KEYS.items()}
    print(f"chapter {args.play}: arrows move, X is A, Z is B, S is X, A is Y, Q and W are L and R, Enter is START, "
          "right Shift is SELECT; click on the lower screen to touch it.  Close the window to stop.", flush=True)
    touching = False
    while True:
        sdl.SDL_PumpEvents()
        if sdl.SDL_HasEvent(SDL_QUIT):
            break
        sdl.SDL_FlushEvents(0, 0xFFFF)
        keys = sdl.SDL_GetKeyboardState(None)
        game.emu.input.keypad_update(sum(mask for scancode, mask in masks.items() if keys[scancode]))
        # the mouse on the lower half of the window is the stylus
        x, y, width, height = ctypes.c_int(), ctypes.c_int(), ctypes.c_int(256), ctypes.c_int(384)
        buttons = sdl.SDL_GetMouseState(ctypes.byref(x), ctypes.byref(y))
        window = sdl.SDL_GetKeyboardFocus()
        if window:
            sdl.SDL_GetWindowSize(window, ctypes.byref(width), ctypes.byref(height))
        touch_x = x.value * 256 // max(width.value, 1)
        touch_y = y.value * 384 // max(height.value, 1) - 192
        if buttons & 1 and window and 0 <= touch_x < 256 and 0 <= touch_y < 192:
            game.emu.input.touch_set_pos(touch_x, touch_y)
            touching = True
        elif touching:
            game.emu.input.touch_release()
            touching = False
        game.emu.cycle(False)
        game.window.draw()
        game.next_frame += game.frame_time
        delay = game.next_frame - time.monotonic()
        if delay > 0:
            time.sleep(delay)
        else:
            game.next_frame = time.monotonic()


def run_one(args, name):
    game = Game(args.rom, args.sav, os.path.join(args.out, name))
    checker = Checker()
    print(f"{name}:")
    if name in CHAPTER_TESTS:
        start_chapter(game, CHAPTER_TESTS[name][0])
        CHAPTER_TESTS[name][1](game, checker)
        return checker.failures
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
    parser.add_argument("--headless", action="store_true", help="do not open the emulator window")
    parser.add_argument("--window", action="store_true", help="kept for compatibility: the window is the default")
    parser.add_argument("--speed", type=float, default=6.0, help="speed of the window mode (1 = real time, 0 = unlimited)")
    parser.add_argument("--play", metavar="CHAPTER", help="open a chapter and play it with the keyboard")
    parser.add_argument("--list", action="store_true", help="list scenarios and chapters")
    parser.add_argument("scenarios", nargs="*", default=[])
    args = parser.parse_args()
    if args.list:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from gen_chapters import CHAPTERS
        print("scenarios:", " ".join(list(TESTS) + list(CHAPTER_TESTS)))
        print("chapters (for --play):")
        for chapter in CHAPTERS:
            print(f"  {chapter['name']}: {chapter['about']}")
        return
    if args.play:
        play(args)
        return
    names = args.scenarios or list(TESTS) + list(CHAPTER_TESTS)

    if args.single:
        sys.exit(1 if run_one(args, names[0]) else 0)

    failed = []
    for name in names:
        command = [sys.executable, __file__, "--rom", args.rom, "--sav", args.sav, "--out", args.out, "--single", name]
        command += ["--headless"] if args.headless else ["--speed", str(args.speed)]
        result = subprocess.run(command)
        if result.returncode != 0:
            failed.append(name)
    print(f"\n{len(names) - len(failed)}/{len(names)} scenarios passed" + (f"; FAILED: {', '.join(failed)}" if failed else ""))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
