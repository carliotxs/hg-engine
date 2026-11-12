#!/usr/bin/env python3
"""Write the boss teams of the hack into data/Trainers.c.

Usage: python3 hack/scripts/gen_trainer_teams.py [--check]

TEAMS below is the source of truth for the trainers it lists: the script replaces their `.party`
block (and makes sure the trainer uses moves and items) every time it runs, so edit the table and
run it again instead of editing those parties by hand.  Trainers that are not in the table are left
alone.  Every species, move and item name is checked against the engine constants.

Design rules of Phase 3 (hack/docs/PLANO.md): gym leaders keep their original type, teams are
complete and coherent, and levels are 2 to 4 above the original game.

A Pokémon is "SPECIES level [@ITEM]: MOVE, MOVE, MOVE, MOVE".
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TRAINERS = ROOT / "data/Trainers.c"

# trainer id -> (comment, IVs out of 255, team)
TEAMS = {
    20: ("Falkner, Violet City: Flying", 60, """
        ROOKIDEE 11: PECK, LEER, POWER_TRIP, HONE_CLAWS
        FLETCHLING 12: PECK, QUICK_ATTACK, EMBER, GROWL
        PIDGEOTTO 15 @ORAN_BERRY: GUST, QUICK_ATTACK, ROOST, SAND_ATTACK"""),
    21: ("Bugsy, Azalea Town: Bug", 80, """
        DWEBBLE 17: SMACK_DOWN, BUG_BITE, WITHDRAW, SAND_ATTACK
        JOLTIK 17: ELECTROWEB, BUG_BITE, STRING_SHOT, ABSORB
        SCYTHER 20 @SITRUS_BERRY: U_TURN, QUICK_ATTACK, WING_ATTACK, FOCUS_ENERGY"""),
    30: ("Whitney, Goldenrod City: Normal", 100, """
        CLEFAIRY 19: DOUBLE_SLAP, MIMIC, ENCORE, METRONOME
        MINCCINO 20: SWIFT, TICKLE, ENCORE, DOUBLE_SLAP
        MILTANK 22 @SITRUS_BERRY: ROLLOUT, STOMP, MILK_DRINK, ATTRACT"""),
    31: ("Morty, Ecruteak City: Ghost", 120, """
        DRIFLOON 24: HEX, GUST, WILL_O_WISP, FOCUS_ENERGY
        HAUNTER 25: SHADOW_PUNCH, SUCKER_PUNCH, HYPNOSIS, CURSE
        MISDREAVUS 26: HEX, CONFUSE_RAY, PAIN_SPLIT, PSYBEAM
        GENGAR 28 @SITRUS_BERRY: SHADOW_BALL, HYPNOSIS, DREAM_EATER, SUCKER_PUNCH"""),
    34: ("Chuck, Cianwood City: Fighting", 140, """
        PRIMEAPE 31: KARATE_CHOP, ROCK_SLIDE, SWAGGER, U_TURN
        HAWLUCHA 32: FLYING_PRESS, AERIAL_ACE, HONE_CLAWS, BOUNCE
        BRELOOM 32: MACH_PUNCH, SEED_BOMB, LEECH_SEED, STUN_SPORE
        POLIWRATH 34 @SITRUS_BERRY: WATERFALL, BRICK_BREAK, HYPNOSIS, BULK_UP"""),
    33: ("Jasmine, Olivine City: Steel", 150, """
        MAGNETON 34: THUNDERBOLT, FLASH_CANNON, THUNDER_WAVE, SUPERSONIC
        SKARMORY 34: STEEL_WING, AERIAL_ACE, SPIKES, ROOST
        LAIRON 35: IRON_HEAD, ROCK_SLIDE, PROTECT, ROAR
        STEELIX 38 @SITRUS_BERRY: IRON_TAIL, DIG, ROCK_SLIDE, SCREECH"""),
    32: ("Pryce, Mahogany Town: Ice", 160, """
        DEWGONG 33: AURORA_BEAM, AQUA_JET, REST, SLEEP_TALK
        SNEASEL 33: ICE_PUNCH, FEINT_ATTACK, QUICK_ATTACK, ICY_WIND
        GLALIE 34: ICE_FANG, CRUNCH, PROTECT, HAIL
        PILOSWINE 37 @SITRUS_BERRY: ICE_FANG, EARTHQUAKE, HAIL, BLIZZARD"""),
    35: ("Clair, Blackthorn City: Dragon", 180, """
        GYARADOS 41: WATERFALL, ICE_FANG, DRAGON_DANCE, BITE
        DRAGONAIR 41: DRAGON_PULSE, THUNDER_WAVE, AQUA_TAIL, FLAMETHROWER
        ALTARIA 42: DRAGON_PULSE, DAZZLING_GLEAM, ROOST, COTTON_GUARD
        FLYGON 43: EARTHQUAKE, DRAGON_CLAW, U_TURN, ROCK_SLIDE
        KINGDRA 45 @SITRUS_BERRY: SURF, DRAGON_PULSE, ICE_BEAM, SMOKESCREEN"""),
    245: ("Will, Elite Four: Psychic", 200, """
        XATU 43: PSYCHIC, AIR_SLASH, CONFUSE_RAY, U_TURN
        JYNX 44: ICE_BEAM, PSYCHIC, LOVELY_KISS, NASTY_PLOT
        EXEGGUTOR 44: PSYCHIC, GIGA_DRAIN, SLEEP_POWDER, LEECH_SEED
        SLOWBRO 44: SURF, PSYCHIC, SLACK_OFF, YAWN
        GARDEVOIR 44: PSYCHIC, DAZZLING_GLEAM, CALM_MIND, THUNDERBOLT
        ALAKAZAM 46 @SITRUS_BERRY: PSYCHIC, SHADOW_BALL, FOCUS_BLAST, RECOVER"""),
    247: ("Koga, Elite Four: Poison", 200, """
        ARIADOS 43: POISON_JAB, SUCKER_PUNCH, STICKY_WEB, SHADOW_SNEAK
        VENOMOTH 44: SLUDGE_BOMB, BUG_BUZZ, QUIVER_DANCE, SLEEP_POWDER
        FORRETRESS 46: GYRO_BALL, TOXIC_SPIKES, SPIKES, EXPLOSION
        MUK 45: GUNK_SHOT, SHADOW_SNEAK, MINIMIZE, TOXIC
        TOXICROAK 45: POISON_JAB, DRAIN_PUNCH, SUCKER_PUNCH, SWORDS_DANCE
        CROBAT 47 @SITRUS_BERRY: CROSS_POISON, BRAVE_BIRD, U_TURN, CONFUSE_RAY"""),
    418: ("Bruno, Elite Four: Fighting", 200, """
        HITMONTOP 45: CLOSE_COMBAT, SUCKER_PUNCH, RAPID_SPIN, FAKE_OUT
        HITMONLEE 45: HIGH_JUMP_KICK, BLAZE_KICK, KNOCK_OFF, FAKE_OUT
        HITMONCHAN 45: DRAIN_PUNCH, ICE_PUNCH, THUNDER_PUNCH, MACH_PUNCH
        HARIYAMA 45: CLOSE_COMBAT, KNOCK_OFF, BULLET_PUNCH, FAKE_OUT
        LUCARIO 47: AURA_SPHERE, FLASH_CANNON, EXTREME_SPEED, CALM_MIND
        MACHAMP 49 @SITRUS_BERRY: DYNAMIC_PUNCH, STONE_EDGE, BULLET_PUNCH, KNOCK_OFF"""),
    246: ("Karen, Elite Four: Dark", 200, """
        UMBREON 45: FOUL_PLAY, MOONLIGHT, TOXIC, CONFUSE_RAY
        WEAVILE 46: NIGHT_SLASH, ICE_PUNCH, FAKE_OUT, SWORDS_DANCE
        HONCHKROW 47: BRAVE_BIRD, SUCKER_PUNCH, NIGHT_SLASH, ROOST
        ABSOL 47: NIGHT_SLASH, PSYCHO_CUT, SUCKER_PUNCH, SWORDS_DANCE
        GENGAR 48: SHADOW_BALL, SLUDGE_BOMB, FOCUS_BLAST, DESTINY_BOND
        HOUNDOOM 50 @SITRUS_BERRY: DARK_PULSE, FLAMETHROWER, NASTY_PLOT, SLUDGE_BOMB"""),
    244: ("Lance, Champion: Dragon", 250, """
        GYARADOS 50: WATERFALL, ICE_FANG, EARTHQUAKE, DRAGON_DANCE
        AERODACTYL 51: STONE_EDGE, EARTHQUAKE, CRUNCH, AERIAL_ACE
        CHARIZARD 51: FLAMETHROWER, AIR_SLASH, DRAGON_PULSE, FOCUS_BLAST
        SALAMENCE 52: DRAGON_CLAW, EARTHQUAKE, FIRE_FANG, DRAGON_DANCE
        GARCHOMP 52: EARTHQUAKE, DRAGON_CLAW, STONE_EDGE, SWORDS_DANCE
        DRAGONITE 54 @SITRUS_BERRY: OUTRAGE, EXTREME_SPEED, FIRE_PUNCH, DRAGON_DANCE"""),
}


def constants(path, prefix):
    return set(re.findall(rf"#define {prefix}_(\w+)\s", (ROOT / path).read_text()))


def main():
    species, moves, items = (constants("include/constants/species.h", "SPECIES"), constants("include/constants/moves.h", "MOVE"),
                             constants("include/constants/item.h", "ITEM"))
    text = TRAINERS.read_text()
    errors = []
    for trainer, (comment, ivs, team) in TEAMS.items():
        start = text.index(f"\n    [{trainer}] = {{")
        end = text.index("\n    },\n", start)
        block = text[start:end]
        mons = []
        for line in filter(None, (line.strip() for line in team.splitlines())):
            match = re.fullmatch(r"(\w+) (\d+)(?: @(\w+))?: (\w+), (\w+), (\w+), (\w+)", line)
            if not match:
                errors.append(f"trainer {trainer}: cannot read '{line}'")
                continue
            name, level, item, *mon_moves = match.groups()
            errors += [f"trainer {trainer}: unknown species {name}"] * (name not in species)
            errors += [f"trainer {trainer}: unknown item {item}" for _ in [0] if item and item not in items]
            errors += [f"trainer {trainer}: unknown move {move}" for move in mon_moves if move not in moves]
            mons.append(f"""            {{
                .ivs = {ivs},
                .abilitySlot = TRAINER_POKEMON_ABILITY_1,
                .level = {level},
                .species = SPECIES_{name},
                .item = ITEM_{item or 'NONE'},
                .moves = {{ {', '.join('MOVE_' + move for move in mon_moves)} }},
                .ballSeal = 0,
            }},""")
        party_start = block.index("        .party = {")
        party_end = block.index("\n        },", party_start) + len("\n        },")
        party = f"        // hack: {comment} (hack/scripts/gen_trainer_teams.py)\n        .party = {{\n" + "\n".join(mons) + "\n        },"
        previous_comment = re.search(r"        // hack: [^\n]*gen_trainer_teams\.py\)\n$", block[:party_start])
        if previous_comment:
            party_start = previous_comment.start()
        block = block[:party_start] + party + block[party_end:]
        block = re.sub(r"\.trainerType = [^,]+,", ".trainerType = TRAINER_DATA_TYPE_MOVES | TRAINER_DATA_TYPE_ITEMS,", block, count=1)
        text = text[:start] + block + text[end:]
    if errors:
        print("\n".join(sorted(set(errors))))
        sys.exit(1)
    print(f"{len(TEAMS)} trainers written")
    if "--check" not in sys.argv:
        TRAINERS.write_text(text)


if __name__ == "__main__":
    main()
