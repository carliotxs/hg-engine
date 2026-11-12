.include "asm/include/interop_macros.inc"

.include "asm/include/scriptmacros.inc"
.include "asm/include/flags.inc"
.include "asm/include/soundeffects.inc"
.include "asm/include/vars.inc"

.include "asm/include/events.inc"
.include "asm/include/game_stats.inc"
.include "asm/include/maps.inc"
.include "asm/include/map_sections.inc"
.include "asm/include/movements.inc"
.include "asm/include/rankings.inc"
.include "asm/include/spawns.inc"
.include "asm/include/std_scripts.inc"
.include "asm/include/trainers.inc"

#include "constants/item.h"
#include "constants/moves.h"
#include "constants/species.h"

.include "data/scr_seq/include/event_D40R0102.inc"


// text archive to grab from: 003.txt

.data


scrdef scr_seq_D40R0102_000
scrdef scr_seq_D40R0102_001
scrdef scr_seq_D40R0102_002
scrdef scr_seq_D40R0102_003
scrdef scr_seq_D40R0102_004
scrdef_end

scr_seq_D40R0102_000:
	end
// hack: DHELMISE specialist (hack/scripts/gen_specialists.py)
scr_seq_D40R0102_001:
	setvar VAR_SPECIAL_x8004, SPECIES_DHELMISE
	setvar VAR_SPECIAL_x8005, 27
	setvar VAR_SPECIAL_x8006, ITEM_RED_CARD
	setvar VAR_SPECIAL_x8007, 2719
	callstd 2077
	end
// hack: STARMIE specialist (hack/scripts/gen_specialists.py)
scr_seq_D40R0102_002:
	setvar VAR_SPECIAL_x8004, SPECIES_STARMIE
	setvar VAR_SPECIAL_x8005, 27
	setvar VAR_SPECIAL_x8006, ITEM_WEAKNESS_POLICY
	setvar VAR_SPECIAL_x8007, 2522
	callstd 2077
	end
// hack: CRUSTLE specialist (hack/scripts/gen_specialists.py)
scr_seq_D40R0102_003:
	setvar VAR_SPECIAL_x8004, SPECIES_CRUSTLE
	setvar VAR_SPECIAL_x8005, 34
	setvar VAR_SPECIAL_x8006, ITEM_EJECT_BUTTON
	setvar VAR_SPECIAL_x8007, 2254
	callstd 2077
	end
// hack: PALOSSAND specialist (hack/scripts/gen_specialists.py)
scr_seq_D40R0102_004:
	setvar VAR_SPECIAL_x8004, SPECIES_PALOSSAND
	setvar VAR_SPECIAL_x8005, 42
	setvar VAR_SPECIAL_x8006, ITEM_ASSAULT_VEST
	setvar VAR_SPECIAL_x8007, 2338
	callstd 2077
	end
	.balign 4
