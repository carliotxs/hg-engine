#!/usr/bin/env python3
"""Generate data/Encounters.c for the hack from the vanilla tables.

Usage: python3 hack/scripts/gen_encounters.py [--check]

Source of truth: hack/data/Encounters.vanilla.c (the untouched hg-engine file) plus the pools below.
The script rewrites data/Encounters.c and prints a report; never edit data/Encounters.c by hand,
change the pools or the rules here and run it again (it is deterministic).

Rules ("mix" design):
  * land: the four most common slots (20/20/10/10 %) stay vanilla, so every route keeps its
    recognisable Pokémon and the vanilla morning/day/night species.  slots 4-5 (10 % each) get a
    species that depends on the time of day, slots 6-9 (5/5/4/4 %) get species of the habitat of the
    area, slots 10-11 (1 % each) get a rare one (starters of every generation, pseudo-legendaries...)
  * surf and the three rods: the two most common slots stay vanilla, the other three are new
    (sea species in sea areas, river and lake species elsewhere)
  * rock smash: the second slot (10 %) is new
  * the evolution stage follows the level of the slot (level-up evolutions only)
  * a vanilla species that would disappear from the whole game gets one of its slots back
  * no legendary, mythical, Ultra Beast or paradox Pokémon: they are reserved for static encounters
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VANILLA = ROOT / "hack/data/Encounters.vanilla.c"
OUTPUT = ROOT / "data/Encounters.c"
SPECIES_H = ROOT / "include/constants/species.h"
EVOLUTIONS = ROOT / "data/Evolutions.c"

# ---------------------------------------------------------------------------------------------
# pools: base species of each family.  "NAME:20" means "only in slots of level 20 or more".
# every area takes the next entries of the pool of its habitat, so neighbouring areas differ.
# ---------------------------------------------------------------------------------------------
POOLS = {
    "field": """ZIGZAGOON STARLY LILLIPUP BUNNELBY YUNGOOS SKWOVET LECHONK PAWMI POOCHYENA BIDOOF PATRAT
        FLETCHLING PIKIPEK ROOKIDEE WOOLOO FIDOUGH TAILLOW SHINX PIDOVE SCATTERBUG TAROUNTULA YAMPER
        ELECTRIKE RALTS BUDEW BLITZLE MINCCINO COTTONEE PETILIL FLABEBE LITLEO SKIDDO ROCKRUFF MUDBRAY
        NYMBLE TANDEMAUS WATTREL SMOLIV KRICKETOT PACHIRISU SKITTY MEDITITE SPOINK SWABLU DEERLING
        EMOLGA HELIOPTILE DEDENNE GOSSIFLEUR NICKIT SQUAWKABILLY FURFROU:20 ORICORIO:20 TADBULB""",
    "forest": """WURMPLE SEEDOT SHROOMISH SEWADDLE VENIPEDE GRUBBIN BLIPBUG NINCADA BURMY COMBEE CHERUBI
        KARRABLAST SHELMET FOONGUS PHANTUMP PUMPKABOO FOMANTIS MORELULL BOUNSWEET CUTIEFLY APPLIN
        TOEDSCOOL CAPSAKID RELLOR BRAMBLIN SLAKOTH PANSAGE PANSEAR PANPOUR JOLTIK DWEBBLE TEDDIURSA
        STUFFUL PANCHAM SHROODLE KOMALA:20 PASSIMIAN:20 HERACROSS:15 PINSIR:15 SCYTHER:15""",
    "cave": """WHISMUR MAKUHITA ARON ROGGENROLA WOOBAT DRILBUR TIMBURR NOIBAT ROLYCOLY NACLI NOSEPASS
        SABLEYE MAWILE BRONZOR CARBINK GLIMMET BALTOY LUNATONE SOLROCK KLINK FERROSEED TYNAMO DURANT:20
        HEATMOR:20 MIENFOO CUFANT TINKATINK ORTHWORM:20 SANDILE SILICOBRA TORKOAL:15 NUMEL MINIOR:20
        MEDITITE RIOLU:15 PAWNIARD:15 GOLETT:15""",
    "mountain": """SPOINK NUMEL SWABLU ZANGOOSE:15 SEVIPER:15 TROPIUS:20 RUFFLET VULLABY BOUFFALANT:25
        MIENFOO HAWLUCHA:20 SKIDDO ROCKRUFF ROOKIDEE STONJOURNER:25 FALINKS:25 KLAWF:20 BOMBIRDIER:20
        CYCLIZAR:20 HIPPOPOTAS SKORUPI TRAPINCH CACNEA MARACTUS:20 SANDILE DARUMAKA SCRAGGY SIGILYPH:20
        HELIOPTILE DRILBUR TIMBURR SALANDIT ROLYCOLY""",
    "wet": """LOTAD SURSKIT WINGULL SHELLOS BUIZEL CROAGUNK TYMPOLE DUCKLETT STUNFISK:15 DEWPIDER CHEWTLE
        WIGLETT CARNIVINE:15 BIDOOF AZURILL BARBOACH YANMA:15 CORPHISH MAREANIE:15 CRAMORANT:20
        TADBULB FLAMIGO:20 SOBBLE:99""",
    "urban": """TRUBBISH GULPIN STUNKY PURRLOIN PLUSLE MINUN VOLBEAT ILLUMISE KECLEON:15 CHATOT:15 GLAMEOW
        BUNEARY MIME_JR BONSLY KLEFKI:20 ESPURR SPRITZEE SWIRLIX VAROOM SHROODLE MASCHIFF GOTHITA
        SOLOSIS ELGYEM MILCERY HATENNA IMPIDIMP INDEEDEE:20 MORPEKO:20 TOXEL PINCURCHIN:20 HAPPINY
        CASTFORM:20 ROTOM:25 SPINDA""",
    "tower": """SHUPPET DUSKULL DRIFLOON YAMASK LITWICK GOLETT HONEDGE:20 SINISTEA GREAVARD CHINGLING
        BRONZOR SANDYGAST PUMPKABOO PHANTUMP MIMIKYU:20 SPIRITOMB:25""",
    "fire": """NUMEL TORKOAL:15 HOUNDOUR SLUGMA LITWICK SALANDIT DARUMAKA LITLEO SIZZLIPEDE ROLYCOLY
        FLETCHLING VULPIX PONYTA CHARCADET:15 LARVESTA:20 PANSEAR""",
    "ruins": """BALTOY SIGILYPH:20 ELGYEM YAMASK GOLETT BRONZOR SOLROCK LUNATONE CHINGLING RALTS SPOINK
        MEDITITE WOOBAT ESPURR INKAY HATENNA FLITTLE RELLOR""",
    "ice": """SNORUNT SPHEAL SNOVER VANILLITE CUBCHOO BERGMITE SNOM EISCUE:20 CETODDLE SMOOCHUM DELIBIRD
        SNEASEL CRYOGONAL:25 FRIGIBAX:25 AMAURA:25""",
    "seacave": """CLAMPERL CORSOLA WAILMER SPHEAL BINACLE DWEBBLE WIMPOD PYUKUMUKU:20 MAREANIE CLOBBOPUS
        SANDYGAST SKRELP CLAUNCHER FRILLISH STARYU HORSEA TIRTOUGA:25 DHELMISE:30""",
    "savanna": """LITLEO MUDBRAY BLITZLE DEERLING BOUFFALANT:25 SAWK:25 THROH:25 PANCHAM MIENFOO
        HAWLUCHA:20 ORANGURU:25 PASSIMIAN:25 KOMALA:25 DRAMPA:30 ORICORIO FLAMIGO CYCLIZAR CUFANT
        STONJOURNER:25 FALINKS:25 ZANGOOSE SEVIPER TROPIUS ABSOL:30 KANGASKHAN:25 RHYHORN EXEGGCUTE
        TRAPINCH HIPPOPOTAS""",
    "elite": """BAGON GIBLE DEINO AXEW GOOMY JANGMO_O DREEPY FRIGIBAX RIOLU ZORUA LARVESTA HONEDGE PAWNIARD
        GOLETT DRUDDIGON DURALUDON FALINKS TINKATINK CHARCADET NOIBAT ARON TRAPINCH SHINX ROCKRUFF
        MIENFOO SCRAGGY LITWICK KLINK FERROSEED TYNAMO SANDILE SALANDIT""",
}

# slots 4 and 5 of outdoor areas: one list per time of day
TIME_POOLS = {
    "morning": """TAILLOW STARLY PIDOVE FLETCHLING PIKIPEK ROOKIDEE COMBEE CUTIEFLY BUDEW CHERUBI PETILIL
        FLABEBE BOUNSWEET SMOLIV WATTREL SWABLU DUCKLETT SKIDDO WOOLOO WINGULL SURSKIT BURMY SEWADDLE
        COTTONEE DEERLING SQUAWKABILLY GOSSIFLEUR HAPPINY AZURILL""",
    "day": """ZIGZAGOON LILLIPUP BUNNELBY YUNGOOS SKWOVET LECHONK PAWMI BIDOOF PATRAT FIDOUGH SHINX
        ELECTRIKE BLITZLE MINCCINO LITLEO MUDBRAY NYMBLE TANDEMAUS PACHIRISU SKITTY MEDITITE SPOINK
        HELIOPTILE DEDENNE YAMPER RALTS TAROUNTULA SCATTERBUG PLUSLE MINUN""",
    "night": """POOCHYENA SHUPPET DUSKULL STUNKY DRIFLOON PURRLOIN WOOBAT NOIBAT PUMPKABOO PHANTUMP MORELULL
        ROCKRUFF NICKIT IMPIDIMP SHROODLE SABLEYE KRICKETOT VOLBEAT ILLUMISE LITWICK GREAVARD INKAY
        ESPURR ZORUA:15 HOUNDOUR GLAMEOW VENIPEDE JOLTIK FOONGUS""",
}

# slots 10 and 11 (1 % each)
RARE_POOLS = {
    "field": "BULBASAUR CHIKORITA TREECKO TURTWIG SNIVY CHESPIN ROWLET GROOKEY SPRIGATITO EEVEE RIOLU ZORUA",
    "forest": "SNIVY ROWLET GROOKEY CHESPIN TREECKO TURTWIG BULBASAUR SPRIGATITO CHIKORITA LARVESTA SCYTHER HERACROSS",
    "cave": "CHARMANDER CYNDAQUIL TORCHIC CHIMCHAR TEPIG FENNEKIN LITTEN SCORBUNNY FUECOCO GIBLE BAGON AXEW",
    "mountain": "TORCHIC CHIMCHAR CYNDAQUIL LITTEN FUECOCO CHARMANDER SCORBUNNY TEPIG FENNEKIN DEINO JANGMO_O ABSOL",
    "wet": "SQUIRTLE TOTODILE MUDKIP PIPLUP OSHAWOTT FROAKIE POPPLIO SOBBLE QUAXLY GOOMY FEEBAS DRATINI",
    "urban": "EEVEE PORYGON ROTOM DITTO KLEFKI MIMIKYU TOGEPI RIOLU ZORUA SPIRITOMB CASTFORM",
    "tower": "MIMIKYU SPIRITOMB DREEPY HONEDGE ZORUA ROTOM",
    "fire": "CHARMANDER CYNDAQUIL TORCHIC CHIMCHAR TEPIG FENNEKIN LITTEN SCORBUNNY FUECOCO LARVESTA",
    "ruins": "LILEEP ANORITH CRANIDOS SHIELDON TIRTOUGA ARCHEN TYRUNT AMAURA OMANYTE KABUTO AERODACTYL BELDUM",
    "ice": "PIPLUP POPPLIO FRIGIBAX AMAURA CRYOGONAL EISCUE",
    "seacave": "SQUIRTLE TOTODILE MUDKIP PIPLUP OSHAWOTT FROAKIE POPPLIO SOBBLE QUAXLY DHELMISE",
    "savanna": "LARVITAR DRATINI BELDUM BAGON GIBLE AXEW DEINO GOOMY JANGMO_O DREEPY",
    "elite": "LARVITAR DRATINI BELDUM BAGON GIBLE AXEW DEINO GOOMY JANGMO_O DREEPY FRIGIBAX LARVESTA",
}

WATER_POOLS = {
    "surf_sea": """WINGULL CARVANHA WAILMER FINNEON MANTYKE FRILLISH ALOMOMOLA:20 SKRELP CLAUNCHER WISHIWASHI
        MAREANIE BRUXISH:20 ARROKUDA WIGLETT FINIZEN CRAMORANT:20 PYUKUMUKU:20 BINACLE SPHEAL""",
    "surf_fresh": "DUCKLETT BUIZEL SHELLOS SURSKIT LOTAD TYMPOLE BASCULIN DEWPIDER CHEWTLE AZURILL BIDOOF CROAGUNK",
    "fish_sea": """CARVANHA FINNEON WISHIWASHI WIGLETT LUVDISC CLAMPERL WAILMER:20 SKRELP CLAUNCHER BINACLE
        MAREANIE WIMPOD FRILLISH CLOBBOPUS PINCURCHIN ARROKUDA FINIZEN RELICANTH:30 ALOMOMOLA:30 DHELMISE:35
        BRUXISH:30 VELUZA:35 TATSUGIRI:35 DONDOZO:40""",
    "fish_fresh": "BARBOACH BASCULIN TYMPOLE CORPHISH CHEWTLE FEEBAS STUNFISK:15 TYNAMO:20 ARROKUDA LOTAD SURSKIT",
    "rock": """DWEBBLE BINACLE ROGGENROLA ROLYCOLY NACLI NOSEPASS ARON CARBINK MINIOR GLIMMET OMANYTE KABUTO
        LILEEP ANORITH CRANIDOS SHIELDON TIRTOUGA ARCHEN TYRUNT AMAURA""",
}
# areas whose water is the sea; everything else is fresh water
SEA = r"NEW_BARK|CHERRYGROVE|OLIVINE|CIANWOOD|WHIRL|ROUTE_4[017]|ROUTE_19|ROUTE_2[0167]|ROUTE_34|PALLET|VERMILION|CINNABAR|SEAFOAM|ROUTE_12|ROUTE_13|FUCHSIA|CLIFF"

# habitat of every area, first match wins.  None: the table is left untouched
HABITATS = [
    (r"UNUSED|SAFARI|BUG_CATCHING|RUINS_OF_ALPH_INSIDE", None),
    (r"BURNED_TOWER", "fire"),
    (r"SPROUT_TOWER|BELL_TOWER", "tower"),
    (r"RUINS_OF_ALPH_OUTSIDE", "ruins"),
    (r"ICE_PATH|SEAFOAM|MT_SILVER_TOP", "ice"),
    (r"WHIRL_ISLANDS", "seacave"),
    (r"VICTORY_ROAD|MT_SILVER_(\dF|MOLTRES|EXPERT|MOUNTAINSIDE)|CERULEAN_CAVE", "elite"),
    (r"CAVE|MT_MORTAR|ROCK_TUNNEL|MT_MOON|TOHJO|SLOWPOKE_WELL", "cave"),
    (r"ILEX|VIRIDIAN_FOREST|NATIONAL_PARK|ROUTE_2_", "forest"),
    (r"ROUTE_4[56]\b|ROUTE_2[678]\b|ROUTE_22|ROUTE_9\b|ROUTE_10\b|ROUTE_3\b|ROUTE_4\b", "mountain"),
    (r"ROUTE_4[78]|MT_SILVER_OUTSIDE|ROUTE_1[345]", "savanna"),
    (r"ROUTE_4[234]|ROUTE_3[02]\b|ROUTE_2[45]|ROUTE_21|ROUTE_12|ROUTE_6\b", "wet"),
    (r"ROUTE_3[45]\b|ROUTE_1[678]|ROUTE_[78]\b|ROUTE_11|ROUTE_5\b|ROUTE_3[89]", "urban"),
    (r".", "field"),
]
OUTDOOR = {"field", "forest", "mountain", "wet", "urban", "savanna", "ruins"}
# habitats with few areas: slots 6-9 also change with the time of day, so that their pools get used
SMALL = {"forest", "ruins", "tower", "fire", "ice", "seacave", "savanna", "urban"}

LAND_TIMES = (("speciesMorning", "morning"), ("speciesDay", "day"), ("speciesNight", "night"))
LAND_KEEP = 4  # slots 0-3 stay vanilla
RARE_MIN_LEVEL = 8  # the 1 % slots of the first routes stay vanilla
WATER_KEEP = 2


def parse_pool(text):
    pool = []
    for token in text.split():
        name, _, level = token.partition(":")
        pool.append((name, int(level) if level else 0))
    return pool


def load_species():
    return set(re.findall(r"#define SPECIES_(\w+)\s", SPECIES_H.read_text()))


def load_evolutions():
    """base species -> list of (level, evolved species) for plain level-up evolutions"""
    text = EVOLUTIONS.read_text()
    evolutions = {}
    for block in re.split(r"\n(?=    \[SPECIES_)", text)[1:]:
        base = re.match(r"    \[SPECIES_(\w+)\]", block).group(1)
        found = re.findall(r"\{ EVO_LEVEL(?:_MALE|_FEMALE|_DAY|_NIGHT)?, (\d+), SPECIES_(\w+) \}", block)
        if found:
            evolutions[base] = [(int(level), target) for level, target in found]
    return evolutions


def evolve(species, level, evolutions):
    """highest stage a wild Pokémon of this level would have reached by level-up"""
    for _ in range(3):
        options = [target for needed, target in evolutions.get(species, []) if needed <= level]
        if not options:
            break
        species = options[0]
    return species


class Picker:
    """walks through a pool; every call continues where the previous area stopped"""

    def __init__(self, pool, known, name):
        self.pool = [(species, level) for species, level in pool if species in known]
        missing = [species for species, _ in pool if species not in known]
        if missing:
            print(f"warning: pool {name}: unknown species ignored: {' '.join(missing)}")
        self.cursor = 0
        self.used = set()

    def pick(self, level, taken):
        for offset in range(len(self.pool)):
            species, min_level = self.pool[(self.cursor + offset) % len(self.pool)]
            if level >= min_level and species not in taken:
                self.cursor = (self.cursor + offset + 1) % len(self.pool)
                self.used.add(species)
                return species
        return None


def habitat_of(name):
    for pattern, habitat in HABITATS:
        if re.search(pattern, name):
            return habitat
    return None


def family_root(species, evolutions, roots={}):
    if not roots:
        for base, targets in evolutions.items():
            for _, target in targets:
                roots[target] = base
    while species in roots:
        species = roots[species]
    return species


def main():
    check_only = "--check" in sys.argv
    known = load_species()
    evolutions = load_evolutions()
    text = VANILLA.read_text()
    head, *blocks = re.split(r"\n(?=    \[ENCDATA_)", text)

    pickers = {name: Picker(parse_pool(pool), known, name) for name, pool in POOLS.items()}
    time_pickers = {name: Picker(parse_pool(pool), known, name) for name, pool in TIME_POOLS.items()}
    rare_pickers = {name: Picker(parse_pool(pool), known, "rare " + name) for name, pool in RARE_POOLS.items()}
    water_pickers = {name: Picker(parse_pool(pool), known, name) for name, pool in WATER_POOLS.items()}

    vanilla_species = set(re.findall(r"SPECIES_(\w+)", text)) - {"NONE"}
    restored = []
    output = None
    protected = set()  # (area, field, slot) that must keep the vanilla species

    for attempt in range(6):
        for picker in (*pickers.values(), *time_pickers.values(), *rare_pickers.values(), *water_pickers.values()):
            picker.cursor = 0
            picker.used = set()
        new_blocks = []
        stats = {"areas": 0, "land": 0, "water": 0}
        for block in blocks:
            name = re.match(r"    \[ENCDATA_(\w+)\]", block).group(1)
            habitat = habitat_of(name)
            if habitat is None:
                new_blocks.append(block)
                continue
            stats["areas"] += 1
            levels = [int(x) for x in re.search(r"\.levels = \{\s*([^}]*)\}", block).group(1).split(",") if x.strip()]
            has_land = int(re.search(r"\.rateWalk = (\d+)", block).group(1)) > 0

            if has_land:
                lists = {field: re.findall(r"SPECIES_(\w+)", re.search(rf"\.{field} = \{{([^}}]*)\}}", block).group(1))
                         for field, _ in LAND_TIMES}
                taken = {family_root(s, evolutions) for field in lists for s in lists[field][:LAND_KEEP]}
                chosen = {}
                all_taken = set()
                for field, time in LAND_TIMES:
                    species = lists[field]
                    time_taken = set(taken)
                    for slot in range(LAND_KEEP, 12):
                        if (name, field, slot) in protected:
                            continue
                        if slot in (4, 5):
                            picker = time_pickers[time] if habitat in OUTDOOR else pickers[habitat]
                        elif slot >= 10:
                            if levels[slot] < RARE_MIN_LEVEL:
                                continue
                            picker = rare_pickers[habitat]
                        else:
                            picker = pickers[habitat]
                        key = (slot, time if (slot in (4, 5) or slot >= 10 or habitat in SMALL) else "any")
                        if key not in chosen:
                            base = picker.pick(levels[slot], time_taken | all_taken) or picker.pick(levels[slot], time_taken)
                            chosen[key] = base
                            if base:
                                all_taken.add(base)
                        base = chosen[key]
                        if base:
                            time_taken.add(base)
                            species[slot] = evolve(base, levels[slot], evolutions)
                            stats["land"] += 1
                    body = "".join(f"\n                SPECIES_{s}," for s in species) + "\n            "
                    block = re.sub(rf"(\.{field} = \{{)[^}}]*(\}})", lambda m: m.group(1) + body + m.group(2), block, count=1)

            water = "sea" if re.search(SEA, name) else "fresh"
            for field, pool, rate in (("surfSlots", "surf_" + water, "rateSurf"), ("oldRodSlots", "fish_" + water, "rateOldRod"),
                                      ("goodRodSlots", "fish_" + water, "rateGoodRod"), ("superRodSlots", "fish_" + water, "rateSuperRod"),
                                      ("rockSmashSlots", "rock", "rateRockSmash")):
                if int(re.search(rf"\.{rate} = (\d+)", block).group(1)) == 0:
                    continue
                match = re.search(rf"\.{field} = \{{(.*?)\n        \}}", block, re.S)
                slots = re.findall(r"\{ (\d+), (\d+), SPECIES_(\w+) \}", match.group(1))
                keep = 1 if field == "rockSmashSlots" else WATER_KEEP
                taken = {family_root(s, evolutions) for _, _, s in slots[:keep]}
                lines = []
                for slot, (low, high, species) in enumerate(slots):
                    if slot >= keep and int(high) > 0 and (name, field, slot) not in protected:
                        base = water_pickers[pool].pick(int(high), taken)
                        if base:
                            taken.add(base)
                            species = evolve(base, int(low), evolutions)
                            stats["water"] += 1
                    lines.append(f"\n            {{ {low}, {high}, SPECIES_{species} }},")
                block = block[:match.start(1)] + "".join(lines) + block[match.end(1):]
            new_blocks.append(block)

        output = head + "\n" + "\n".join(new_blocks)
        lost = vanilla_species - set(re.findall(r"SPECIES_(\w+)", output))
        if not lost:
            break
        # give every lost vanilla species its most common vanilla slot back and generate again
        for species in sorted(lost):
            for block in blocks:
                name = re.match(r"    \[ENCDATA_(\w+)\]", block).group(1)
                if habitat_of(name) is None:
                    continue
                found = False
                for field in ("speciesMorning", "speciesDay", "speciesNight", "surfSlots", "oldRodSlots", "goodRodSlots",
                              "superRodSlots", "rockSmashSlots"):
                    if field.startswith("species"):
                        match = re.search(rf"\.{field} = \{{([^}}]*)\}}", block)
                    else:
                        match = re.search(rf"\.{field} = \{{(.*?)\n        \}}", block, re.S)
                    slots = re.findall(r"SPECIES_(\w+)", match.group(1))
                    keep = LAND_KEEP if field.startswith("species") else 1 if field == "rockSmashSlots" else WATER_KEEP
                    positions = [i for i, s in enumerate(slots) if s == species and i >= keep]
                    if positions:
                        protected.add((name, field, positions[0]))
                        restored.append(f"{species} ({name})")
                        found = True
                        break
                if found:
                    break

    final_species = set(re.findall(r"SPECIES_(\w+)", output)) - {"NONE"}
    new_species = final_species - vanilla_species
    lost = vanilla_species - final_species
    all_pool = {s for picker in (*pickers.values(), *time_pickers.values(), *rare_pickers.values(), *water_pickers.values())
                for s, _ in picker.pool}
    unused = sorted(base for base in all_pool if not any(base in picker.used for picker in
                    (*pickers.values(), *time_pickers.values(), *rare_pickers.values(), *water_pickers.values())))
    print(f"areas changed: {stats['areas']}, land slots replaced: {stats['land']}, water/rock slots replaced: {stats['water']}")
    print(f"species in the wild: vanilla {len(vanilla_species)}, now {len(final_species)} ({len(new_species)} new)")
    print(f"vanilla slots restored so nothing disappears: {len(set(restored))} {sorted(set(restored))[:12]}")
    print(f"vanilla species lost: {sorted(lost)}")
    print(f"pool families never placed: {unused}")
    if lost:
        sys.exit(1)
    if not check_only:
        OUTPUT.write_text(output)
        print(f"written: {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
