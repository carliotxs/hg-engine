#!/usr/bin/env python3
"""Write the boss teams of the hack into data/Trainers.c.

Usage: python3 hack/scripts/gen_trainer_teams.py [--check]

TEAMS below is the source of truth for the trainers it lists: the script replaces their `.party`
block (and makes sure the trainer uses moves and items) every time it runs, so edit the table and
run it again instead of editing those parties by hand.  Trainers that are not in the table are left
alone, except the Team Rocket grunts, which get a one-time automatic upgrade (see GRUNT_POOL).  Every species, move and item name is checked against the engine constants.

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
    # extra Team Rocket grunts (hack/scripts/gen_rocket.py places them).  no moves: default movesets
    739: ("extra grunt, Route 43", 100, """
        HOUNDOUR 20
        GOLBAT 22"""),
    740: ("extra grunt, Lake of Rage", 100, """
        MURKROW 21
        KOFFING 21
        CROAGUNK 22"""),
    741: ("extra grunt, Mahogany Town", 100, """
        STUNKY 21
        GRIMER 22"""),
    742: ("extra grunt, Goldenrod City", 120, """
        STUNKY 28
        GOLBAT 29
        HOUNDOOM 30"""),
    743: ("extra grunt, Goldenrod City", 120, """
        KOFFING 29
        SCRAGGY 29
        ARBOK 30"""),
    # random events: grunts robbing Poké Marts (hack/scripts/gen_story.py), levels of their towns
    745: ("mart robber, Cherrygrove City", 60, """
        POOCHYENA 6
        ZUBAT 7"""),
    746: ("mart robber, Violet City", 70, """
        PURRLOIN 10
        KOFFING 11"""),
    747: ("mart robber, Azalea Town", 80, """
        STUNKY 15
        GRIMER 15
        HOUNDOUR 16"""),
    # famous visitors (hack/scripts/gen_story.py): Crasher Wake at the Lake of Rage on Saturdays
    748: ("Crasher Wake, weekly visitor at the Lake of Rage", 180, """
        QUAGSIRE 38: EARTHQUAKE, WATERFALL, YAWN, RECOVER
        LUDICOLO 38: GIGA_DRAIN, SURF, FAKE_OUT, RAIN_DANCE
        GYARADOS 39: WATERFALL, ICE_FANG, DRAGON_DANCE, BITE
        FLOATZEL 41 @SITRUS_BERRY: WATERFALL, ICE_PUNCH, AQUA_JET, BULK_UP"""),
    # Korrina, top of the Olivine Lighthouse after Amphy is cured (hack/scripts/gen_korrina.py).
    # her Lucario holds its Mega Stone: the battle is where the player first sees a Mega Evolution
    744: ("Korrina, Olivine Lighthouse: Kalos arc", 200, """
        MIENFOO 36: DRAIN_PUNCH, U_TURN, FAKE_OUT, CALM_MIND
        HAWLUCHA 37: FLYING_PRESS, ACROBATICS, HONE_CLAWS, ROOST
        LUCARIO 39 @LUCARIONITE: AURA_SPHERE, FLASH_CANNON, BONE_RUSH, SWORDS_DANCE"""),
    # Team Rocket executives and Giovanni: Poison and Dark teams, 3 levels above the original
    486: ("Proton, Slowpoke Well", 90, """
        ZUBAT 11: LEECH_LIFE, SUPERSONIC, BITE, ASTONISH
        STUNKY 12: POISON_GAS, SCRATCH, FOCUS_ENERGY, SMOKESCREEN
        KOFFING 15 @ORAN_BERRY: SMOG, TACKLE, POISON_GAS, SMOKESCREEN"""),
    488: ("Petrel, Mahogany hideout", 140, """
        GOLBAT 25: WING_ATTACK, BITE, CONFUSE_RAY, POISON_FANG
        GRIMER 25: SLUDGE, MUD_BOMB, MINIMIZE, DISABLE
        KOFFING 25: SLUDGE, SELF_DESTRUCT, SMOKESCREEN, ASSURANCE
        RATICATE 26 @ORAN_BERRY: HYPER_FANG, CRUNCH, SCARY_FACE, QUICK_ATTACK"""),
    479: ("Ariana, Mahogany hideout", 150, """
        ARBOK 28: POISON_FANG, CRUNCH, GLARE, SCREECH
        GLOOM 28: ACID, GIGA_DRAIN, SLEEP_POWDER, MOONLIGHT
        HOUNDOUR 28: FIRE_FANG, BITE, ROAR, SMOG
        MURKROW 30 @SITRUS_BERRY: FEINT_ATTACK, WING_ATTACK, HAZE, NIGHT_SHADE"""),
    706: ("Proton, Radio Tower", 170, """
        GOLBAT 33: AIR_CUTTER, POISON_FANG, CONFUSE_RAY, BITE
        SKUNTANK 34: NIGHT_SLASH, POISON_JAB, FLAMETHROWER, SCREECH
        TOXICROAK 34: POISON_JAB, REVENGE, SUCKER_PUNCH, SWAGGER
        WEEZING 36 @SITRUS_BERRY: SLUDGE_BOMB, WILL_O_WISP, SHADOW_BALL, EXPLOSION"""),
    487: ("Petrel, Radio Tower", 170, """
        KOFFING 33: SLUDGE, SELF_DESTRUCT, SMOKESCREEN, ASSURANCE
        KOFFING 33: SLUDGE, SELF_DESTRUCT, SMOKESCREEN, ASSURANCE
        MUK 33: SLUDGE_BOMB, MUD_BOMB, MINIMIZE, SCREECH
        SWALOT 33: SLUDGE_BOMB, YAWN, STOCKPILE, SWALLOW
        WEEZING 34: SLUDGE_BOMB, WILL_O_WISP, SMOKESCREEN, EXPLOSION
        WEEZING 35 @SITRUS_BERRY: SLUDGE_BOMB, SHADOW_BALL, WILL_O_WISP, EXPLOSION"""),
    478: ("Ariana, Radio Tower", 180, """
        ARBOK 35: GUNK_SHOT, CRUNCH, GLARE, ICE_FANG
        VILEPLUME 35: SLUDGE_BOMB, GIGA_DRAIN, SLEEP_POWDER, MOONLIGHT
        DRAPION 36: NIGHT_SLASH, CROSS_POISON, ICE_FANG, TOXIC_SPIKES
        HONCHKROW 37 @SITRUS_BERRY: NIGHT_SLASH, DRILL_PECK, SUCKER_PUNCH, ROOST"""),
    485: ("Archer, Radio Tower", 200, """
        WEEZING 38: SLUDGE_BOMB, WILL_O_WISP, SHADOW_BALL, EXPLOSION
        CROBAT 38: CROSS_POISON, AIR_SLASH, CONFUSE_RAY, U_TURN
        PERSIAN 38: SLASH, POWER_GEM, FAKE_OUT, NASTY_PLOT
        HONCHKROW 39: NIGHT_SLASH, DRILL_PECK, SUCKER_PUNCH, ROOST
        HOUNDOOM 41 @SITRUS_BERRY: FLAMETHROWER, DARK_PULSE, NASTY_PLOT, SLUDGE_BOMB"""),
    700: ("Giovanni", 250, """
        PERSIAN 45: SLASH, POWER_GEM, FAKE_OUT, NASTY_PLOT
        KANGASKHAN 44: RETURN, EARTHQUAKE, SUCKER_PUNCH, FAKE_OUT
        NIDOKING 45: EARTH_POWER, SLUDGE_WAVE, ICE_BEAM, THUNDERBOLT
        HONCHKROW 46: NIGHT_SLASH, DRILL_PECK, SUCKER_PUNCH, ROOST
        RHYPERIOR 46: EARTHQUAKE, STONE_EDGE, MEGAHORN, ROCK_POLISH
        NIDOQUEEN 49 @SITRUS_BERRY: EARTH_POWER, SLUDGE_WAVE, ICE_BEAM, FLAMETHROWER"""),
}

# trainers that do not exist in the original game: id -> (name, class, text when beaten, text when winning).
# they are appended to data/Trainers.c (and to asm/include/trainers.inc as TRAINER_HACK_<id>) once
NEW_TRAINERS = {
    739: ("Grunt", "TEAM_ROCKET", "Tch! Beaten by a kid on patrol...", "Go home, kid!"),
    740: ("Grunt", "TEAM_ROCKET", "The lake experiment wasn’t supposed\\\\nto have witnesses!", "Nothing to see here!"),
    741: ("Grunt", "TEAM_ROCKET", "I was only told to watch the shop...", "Move along!"),
    742: ("Grunt", "TEAM_ROCKET", "The Radio Tower is ours anyway!", "Goldenrod belongs to Team Rocket!"),
    743: ("Grunt", "TEAM_ROCKET", "You’re too late to stop the broadcast!", "Stay off these streets!"),
    745: ("Grunt", "TEAM_ROCKET", "All this for a few Potions...", "Hands off the merchandise!"),
    746: ("Grunt", "TEAM_ROCKET", "The boss said this job was easy!", "This shop is closed, kid!"),
    747: ("Grunt", "TEAM_ROCKET", "I should’ve robbed the Berry shop...", "Keep walking!"),
    748: ("Wake", "LEADER_CRASHER_WAKE", "Hahaha! What a splash!\\\\nYou made a wave bigger than mine!", "Train harder and come back\\\\nnext week!"),
    744: ("Korrina", "BATTLE_GIRL", "That bond... You two are ready\\\\nfor Mega Evolution!", "Come back when you and your\\\\nPokémon are closer!"),
}

# Team Rocket grunts: every Pokémon gains GRUNT_LEVELS levels and, from the second one on, the
# endless Rattata and Zubat give way to this pool (evolved according to the level).  the first
# Pokémon of each grunt stays what it was.  a marker comment makes the pass run only once per grunt
GRUNT_LEVELS = 2
GRUNT_POOL = """ZUBAT KOFFING GRIMER EKANS HOUNDOUR MURKROW STUNKY PURRLOIN POOCHYENA GULPIN CROAGUNK
    TRUBBISH VENIPEDE SCRAGGY SANDILE SNEASEL SKORUPI NICKIT RATTATA DROWZEE""".split()
GRUNT_MARKER = "        // hack: grunt upgraded (hack/scripts/gen_trainer_teams.py)\n"


def load_evolutions():
    evolutions = {}
    for block in re.split(r"\n(?=    \[SPECIES_)", (ROOT / "data/Evolutions.c").read_text())[1:]:
        base = re.match(r"    \[SPECIES_(\w+)\]", block).group(1)
        found = re.findall(r"\{ EVO_LEVEL(?:_MALE|_FEMALE|_DAY|_NIGHT)?, (\d+), SPECIES_(\w+) \}", block)
        if found:
            evolutions[base] = [(int(level), target) for level, target in found]
    return evolutions


def evolve(species, level, evolutions):
    for _ in range(3):
        options = [target for needed, target in evolutions.get(species, []) if needed <= level]
        if not options:
            break
        species = options[0]
    return species


def upgrade_grunts(text, species):
    evolutions = load_evolutions()
    pool = [name for name in GRUNT_POOL if name in species]
    count = 0
    blocks = re.split(r"\n(?=    \[\d+\] = \{)", text)
    for index, block in enumerate(blocks):
        header = re.match(r"    \[(\d+)\]", block)
        if not header or int(header.group(1)) in TEAMS or GRUNT_MARKER in block:
            continue
        if not re.search(r"trainerClass = TRAINERCLASS_TEAM_ROCKET(_F)?,", block):
            continue
        trainer = int(header.group(1))
        position = [0]

        def mon(match):
            level = int(match.group(1)) + GRUNT_LEVELS
            name = match.group(3)
            if position[0] > 0:
                name = evolve(pool[(trainer * 7 + position[0] * 3) % len(pool)], level, evolutions)
            position[0] += 1
            return f".level = {level},{match.group(2)}.species = SPECIES_{name}"

        block = re.sub(r"\.level = (\d+),(\s*)\.species = SPECIES_(\w+)", mon, block)
        blocks[index] = block.replace("        .party = {", GRUNT_MARKER + "        .party = {", 1)
        count += 1
    return "\n".join(blocks), count


def constants(path, prefix):
    return set(re.findall(rf"#define {prefix}_(\w+)\s", (ROOT / path).read_text()))


def main():
    species, moves, items = (constants("include/constants/species.h", "SPECIES"), constants("include/constants/moves.h", "MOVE"),
                             constants("include/constants/item.h", "ITEM"))
    text = TRAINERS.read_text()
    errors = []
    inc_path = ROOT / "asm/include/trainers.inc"
    inc = inc_path.read_text()
    for trainer, (name, trainer_class, lose, win) in NEW_TRAINERS.items():
        if f"\n    [{trainer}] = {{" in text:
            continue
        entry = f"""
    // hack: new trainer (hack/scripts/gen_trainer_teams.py)
    [{trainer}] = {{
        .name = "{name}",
        .data = {{
            .trainerType = TRAINER_DATA_TYPE_NOTHING,
            .trainerClass = TRAINERCLASS_{trainer_class},
            .items = {{ ITEM_NONE, ITEM_NONE, ITEM_NONE, ITEM_NONE }},
            .aiFlags = F_PRIORITIZE_SUPER_EFFECTIVE | F_EVALUATE_ATTACKS,
            .battleType = SINGLE_BATTLE,
        }},
        .party = {{
        }},
        .text = {{
            {{
                .type = TRMSG_LOSE,
                .text = "{lose}\\\\n",
            }},
            {{
                .type = TRMSG_WIN,
                .text = "{win}\\\\n",
            }},
        }},
    }},
"""
        end_of_array = text.index("\n};\n\nconst u16 sTrainerTextOrder")
        text = text[:end_of_array] + entry.rstrip("\n") + "\n" + text[end_of_array:]
        end_of_order = text.rindex("};\n\nconst u32 sTrainerDataCount")
        text = text[:end_of_order] + f"    {trainer},\n" + text[end_of_order:]
        if f"TRAINER_HACK_{trainer}," not in inc:
            last = re.findall(r"^\.equ TRAINER_\w+, \d+[^\n]*\n", inc, re.M)[-1]
            inc = inc.replace(last, last + f".equ TRAINER_HACK_{trainer}, {trainer} // hack: {name}\n", 1)
    for trainer, (comment, ivs, team) in TEAMS.items():
        start = text.index(f"\n    [{trainer}] = {{")
        end = text.index("\n    },\n", start)
        block = text[start:end]
        mons = []
        for line in filter(None, (line.strip() for line in team.splitlines())):
            match = re.fullmatch(r"(\w+) (\d+)(?: @(\w+))?: (\w+), (\w+), (\w+), (\w+)", line)
            plain = re.fullmatch(r"(\w+) (\d+)", line)
            if plain:  # no moves and no item: the Pokémon uses its default moveset
                errors += [f"trainer {trainer}: unknown species {plain.group(1)}"] * (plain.group(1) not in species)
                mons.append(f"""            {{
                .ivs = {ivs},
                .abilitySlot = TRAINER_POKEMON_ABILITY_1,
                .level = {plain.group(2)},
                .species = SPECIES_{plain.group(1)},
                .ballSeal = 0,
            }},""")
                continue
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
        trainer_type = "TRAINER_DATA_TYPE_MOVES | TRAINER_DATA_TYPE_ITEMS" if ".moves = " in party else "TRAINER_DATA_TYPE_NOTHING"
        block = re.sub(r"\.trainerType = [^,]+,", f".trainerType = {trainer_type},", block, count=1)
        text = text[:start] + block + text[end:]
    if errors:
        print("\n".join(sorted(set(errors))))
        sys.exit(1)
    text, grunts = upgrade_grunts(text, species)
    print(f"{len(TEAMS)} trainers written, {grunts} grunts upgraded")
    if "--check" not in sys.argv:
        TRAINERS.write_text(text)
        inc_path.write_text(inc)


if __name__ == "__main__":
    main()
