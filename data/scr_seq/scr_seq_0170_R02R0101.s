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

.include "data/scr_seq/include/event_R02R0101.inc"


// text archive to grab from: 321.txt

.data


scrdef scr_seq_R02R0101_000
scrdef scr_seq_R02R0101_001
scrdef scr_seq_R02R0101_002
scrdef scr_seq_R02R0101_003
scrdef scr_seq_R02R0101_004
scrdef scr_seq_R02R0101_005
scrdef scr_seq_R02R0101_006
scrdef scr_seq_R02R0101_007
scrdef scr_seq_R02R0101_008
scrdef scr_seq_R02R0101_009
scrdef_end

scr_seq_R02R0101_000:
	scrcmd_055 2, 0
	scrcmd_057 3
	scrcmd_058
	trainer_tips 0, VAR_SPECIAL_RESULT
	callstd std_signpost
	end
// hack: BEAUTIFLY specialist (hack/scripts/gen_specialists.py)
scr_seq_R02R0101_001:
	setvar VAR_SPECIAL_x8004, SPECIES_BEAUTIFLY
	setvar VAR_SPECIAL_x8005, 10
	setvar VAR_SPECIAL_x8006, ITEM_BRIGHT_POWDER
	setvar VAR_SPECIAL_x8007, 2540
	callstd 2077
	end
// hack: DUSTOX specialist (hack/scripts/gen_specialists.py)
scr_seq_R02R0101_002:
	setvar VAR_SPECIAL_x8004, SPECIES_DUSTOX
	setvar VAR_SPECIAL_x8005, 10
	setvar VAR_SPECIAL_x8006, ITEM_KINGS_ROCK
	setvar VAR_SPECIAL_x8007, 2541
	callstd 2077
	end
// hack: SHIFTRY specialist (hack/scripts/gen_specialists.py)
scr_seq_R02R0101_003:
	setvar VAR_SPECIAL_x8004, SPECIES_SHIFTRY
	setvar VAR_SPECIAL_x8005, 14
	setvar VAR_SPECIAL_x8006, ITEM_RARE_CANDY
	setvar VAR_SPECIAL_x8007, 2542
	callstd 2077
	end
// hack: BRELOOM specialist (hack/scripts/gen_specialists.py)
scr_seq_R02R0101_004:
	setvar VAR_SPECIAL_x8004, SPECIES_BRELOOM
	setvar VAR_SPECIAL_x8005, 23
	setvar VAR_SPECIAL_x8006, ITEM_EXPERT_BELT
	setvar VAR_SPECIAL_x8007, 2543
	callstd 2077
	end
// hack: NINJASK specialist (hack/scripts/gen_specialists.py)
scr_seq_R02R0101_005:
	setvar VAR_SPECIAL_x8004, SPECIES_NINJASK
	setvar VAR_SPECIAL_x8005, 20
	setvar VAR_SPECIAL_x8006, ITEM_SHELL_BELL
	setvar VAR_SPECIAL_x8007, 2544
	callstd 2077
	end
// hack: SHEDINJA specialist (hack/scripts/gen_specialists.py)
scr_seq_R02R0101_006:
	setvar VAR_SPECIAL_x8004, SPECIES_SHEDINJA
	setvar VAR_SPECIAL_x8005, 20
	setvar VAR_SPECIAL_x8006, ITEM_MUSCLE_BAND
	setvar VAR_SPECIAL_x8007, 2545
	callstd 2077
	end
// hack: ESCAVALIER specialist (hack/scripts/gen_specialists.py)
scr_seq_R02R0101_007:
	setvar VAR_SPECIAL_x8004, SPECIES_ESCAVALIER
	setvar VAR_SPECIAL_x8005, 13
	setvar VAR_SPECIAL_x8006, ITEM_RARE_CANDY
	setvar VAR_SPECIAL_x8007, 2546
	callstd 2077
	end
// hack: VIKAVOLT specialist (hack/scripts/gen_specialists.py)
scr_seq_R02R0101_008:
	setvar VAR_SPECIAL_x8004, SPECIES_VIKAVOLT
	setvar VAR_SPECIAL_x8005, 20
	setvar VAR_SPECIAL_x8006, ITEM_CHOICE_SCARF
	setvar VAR_SPECIAL_x8007, 2547
	callstd 2077
	end
// hack: ORBEETLE specialist (hack/scripts/gen_specialists.py)
scr_seq_R02R0101_009:
	setvar VAR_SPECIAL_x8004, SPECIES_ORBEETLE
	setvar VAR_SPECIAL_x8005, 30
	setvar VAR_SPECIAL_x8006, ITEM_ASSAULT_VEST
	setvar VAR_SPECIAL_x8007, 2548
	callstd 2077
	end
	.balign 4
