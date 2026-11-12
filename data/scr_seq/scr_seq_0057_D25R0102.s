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

.include "data/scr_seq/include/event_D25R0102.inc"


// text archive to grab from: 088.txt

.data


scrdef scr_seq_D25R0102_000
scrdef scr_seq_D25R0102_001
scrdef scr_seq_D25R0102_002
scrdef scr_seq_D25R0102_003
scrdef scr_seq_D25R0102_004
scrdef scr_seq_D25R0102_005
scrdef_end

scr_seq_D25R0102_000:
	end
// hack: LUNATONE specialist (hack/scripts/gen_specialists.py)
scr_seq_D25R0102_001:
	setvar VAR_SPECIAL_x8004, SPECIES_LUNATONE
	setvar VAR_SPECIAL_x8005, 10
	setvar VAR_SPECIAL_x8006, ITEM_LIFE_ORB
	setvar VAR_SPECIAL_x8007, 2300
	callstd 2077
	end
// hack: CLAYDOL specialist (hack/scripts/gen_specialists.py)
scr_seq_D25R0102_002:
	setvar VAR_SPECIAL_x8004, SPECIES_CLAYDOL
	setvar VAR_SPECIAL_x8005, 36
	setvar VAR_SPECIAL_x8006, ITEM_ASSAULT_VEST
	setvar VAR_SPECIAL_x8007, 2302
	callstd 2077
	end
// hack: KLINKLANG specialist (hack/scripts/gen_specialists.py)
scr_seq_D25R0102_003:
	setvar VAR_SPECIAL_x8004, SPECIES_KLINKLANG
	setvar VAR_SPECIAL_x8005, 49
	setvar VAR_SPECIAL_x8006, ITEM_ROCKY_HELMET
	setvar VAR_SPECIAL_x8007, 2361
	callstd 2077
	end
// hack: CHARIZARD specialist (hack/scripts/gen_specialists.py)
scr_seq_D25R0102_004:
	setvar VAR_SPECIAL_x8004, SPECIES_CHARIZARD
	setvar VAR_SPECIAL_x8005, 36
	setvar VAR_SPECIAL_x8006, ITEM_CHARIZARDITE_X
	setvar VAR_SPECIAL_x8007, 2636
	callstd 2077
	end
// hack: RATICATE specialist (hack/scripts/gen_specialists.py)
scr_seq_D25R0102_005:
	setvar VAR_SPECIAL_x8004, SPECIES_RATICATE
	setvar VAR_SPECIAL_x8005, 20
	setvar VAR_SPECIAL_x8006, ITEM_EJECT_BUTTON
	setvar VAR_SPECIAL_x8007, 2681
	callstd 2077
	end
	.balign 4
