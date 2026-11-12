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

.include "data/scr_seq/include/event_D25R0101.inc"


// text archive to grab from: 087.txt

.data


scrdef scr_seq_D25R0101_000
scrdef scr_seq_D25R0101_001
scrdef scr_seq_D25R0101_002
scrdef scr_seq_D25R0101_003
scrdef scr_seq_D25R0101_004
scrdef scr_seq_D25R0101_005
scrdef_end

scr_seq_D25R0101_000:
	end
// hack: SANDSLASH specialist (hack/scripts/gen_specialists.py)
scr_seq_D25R0101_001:
	setvar VAR_SPECIAL_x8004, SPECIES_SANDSLASH
	setvar VAR_SPECIAL_x8005, 22
	setvar VAR_SPECIAL_x8006, ITEM_LEFTOVERS
	setvar VAR_SPECIAL_x8007, 2193
	callstd 2077
	end
// hack: HARIYAMA specialist (hack/scripts/gen_specialists.py)
scr_seq_D25R0101_002:
	setvar VAR_SPECIAL_x8004, SPECIES_HARIYAMA
	setvar VAR_SPECIAL_x8005, 24
	setvar VAR_SPECIAL_x8006, ITEM_KINGS_ROCK
	setvar VAR_SPECIAL_x8007, 2205
	callstd 2077
	end
// hack: SWOOBAT specialist (hack/scripts/gen_specialists.py)
scr_seq_D25R0101_003:
	setvar VAR_SPECIAL_x8004, SPECIES_SWOOBAT
	setvar VAR_SPECIAL_x8005, 10
	setvar VAR_SPECIAL_x8006, ITEM_AIR_BALLOON
	setvar VAR_SPECIAL_x8007, 2607
	callstd 2077
	end
// hack: GOLEM specialist (hack/scripts/gen_specialists.py)
scr_seq_D25R0101_004:
	setvar VAR_SPECIAL_x8004, SPECIES_GOLEM
	setvar VAR_SPECIAL_x8005, 25
	setvar VAR_SPECIAL_x8006, ITEM_EJECT_BUTTON
	setvar VAR_SPECIAL_x8007, 2655
	callstd 2077
	end
// hack: SEAKING specialist (hack/scripts/gen_specialists.py)
scr_seq_D25R0101_005:
	setvar VAR_SPECIAL_x8004, SPECIES_SEAKING
	setvar VAR_SPECIAL_x8005, 43
	setvar VAR_SPECIAL_x8006, ITEM_ROCKY_HELMET
	setvar VAR_SPECIAL_x8007, 2676
	callstd 2077
	end
	.balign 4
