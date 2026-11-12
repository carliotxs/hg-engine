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

.include "data/scr_seq/include/event_R08.inc"


// text archive to grab from: 338.txt

.data


scrdef scr_seq_R08_000
scrdef scr_seq_R08_001
scrdef scr_seq_R08_002
scrdef scr_seq_R08_003
scrdef scr_seq_R08_004
scrdef scr_seq_R08_005
scrdef scr_seq_R08_006
scrdef scr_seq_R08_007
scrdef scr_seq_R08_008
scrdef_end

scr_seq_R08_000:
	play_se SEQ_SE_DP_SELECT
	lockall
	npc_msg 0
	wait_button
	closemsg
	releaseall
	end

scr_seq_R08_001:
	scrcmd_055 2, 0
	scrcmd_057 3
	scrcmd_058
	trainer_tips 1, VAR_SPECIAL_RESULT
	callstd std_signpost
	end
// hack: GENGAR specialist (hack/scripts/gen_specialists.py)
scr_seq_R08_002:
	setvar VAR_SPECIAL_x8004, SPECIES_GENGAR
	setvar VAR_SPECIAL_x8005, 25
	setvar VAR_SPECIAL_x8006, ITEM_GENGARITE
	setvar VAR_SPECIAL_x8007, 2240
	callstd 2077
	end
// hack: CINCCINO specialist (hack/scripts/gen_specialists.py)
scr_seq_R08_003:
	setvar VAR_SPECIAL_x8004, SPECIES_CINCCINO
	setvar VAR_SPECIAL_x8005, 18
	setvar VAR_SPECIAL_x8006, ITEM_ROCKY_HELMET
	setvar VAR_SPECIAL_x8007, 2256
	callstd 2077
	end
// hack: ALCREMIE specialist (hack/scripts/gen_specialists.py)
scr_seq_R08_004:
	setvar VAR_SPECIAL_x8004, SPECIES_ALCREMIE
	setvar VAR_SPECIAL_x8005, 20
	setvar VAR_SPECIAL_x8006, ITEM_RARE_CANDY
	setvar VAR_SPECIAL_x8007, 2273
	callstd 2077
	end
// hack: MABOSSTIFF specialist (hack/scripts/gen_specialists.py)
scr_seq_R08_005:
	setvar VAR_SPECIAL_x8004, SPECIES_MABOSSTIFF
	setvar VAR_SPECIAL_x8005, 30
	setvar VAR_SPECIAL_x8006, ITEM_WISE_GLASSES
	setvar VAR_SPECIAL_x8007, 2275
	callstd 2077
	end
// hack: TOGEKISS specialist (hack/scripts/gen_specialists.py)
scr_seq_R08_006:
	setvar VAR_SPECIAL_x8004, SPECIES_TOGEKISS
	setvar VAR_SPECIAL_x8005, 18
	setvar VAR_SPECIAL_x8006, ITEM_EJECT_BUTTON
	setvar VAR_SPECIAL_x8007, 2358
	callstd 2077
	end
// hack: DITTO specialist (hack/scripts/gen_specialists.py)
scr_seq_R08_007:
	setvar VAR_SPECIAL_x8004, SPECIES_DITTO
	setvar VAR_SPECIAL_x8005, 20
	setvar VAR_SPECIAL_x8006, ITEM_EJECT_BUTTON
	setvar VAR_SPECIAL_x8007, 2371
	callstd 2077
	end
// hack: GRAFAIAI specialist (hack/scripts/gen_specialists.py)
scr_seq_R08_008:
	setvar VAR_SPECIAL_x8004, SPECIES_GRAFAIAI
	setvar VAR_SPECIAL_x8005, 28
	setvar VAR_SPECIAL_x8006, ITEM_BRIGHT_POWDER
	setvar VAR_SPECIAL_x8007, 2611
	callstd 2077
	end
	.balign 4
