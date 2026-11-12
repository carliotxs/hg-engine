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

.include "data/scr_seq/include/event_D42R0101.inc"


// text archive to grab from: 127.txt

.data


scrdef scr_seq_D42R0101_000
scrdef scr_seq_D42R0101_001
scrdef scr_seq_D42R0101_002
scrdef scr_seq_D42R0101_003
scrdef scr_seq_D42R0101_004
scrdef_end

scr_seq_D42R0101_000:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	goto_if_set FLAG_GOT_BLACKGLASSES_FROM_DARK_CAVE_MAN, _0045
	npc_msg 0
	goto_if_no_item_space ITEM_BLACK_GLASSES, 1, _0050
	callstd std_give_item_verbose
	setflag FLAG_GOT_BLACKGLASSES_FROM_DARK_CAVE_MAN
_0045:
	npc_msg 2
	wait_button
	closemsg
	releaseall
	end

_0050:
	npc_msg 3
	wait_button
	closemsg
	releaseall
	end
// hack: WOBBUFFET specialist (hack/scripts/gen_specialists.py)
scr_seq_D42R0101_001:
	setvar VAR_SPECIAL_x8004, SPECIES_WOBBUFFET
	setvar VAR_SPECIAL_x8005, 23
	setvar VAR_SPECIAL_x8006, ITEM_EXPERT_BELT
	setvar VAR_SPECIAL_x8007, 2109
	callstd 2077
	end
// hack: GLIMMORA specialist (hack/scripts/gen_specialists.py)
scr_seq_D42R0101_002:
	setvar VAR_SPECIAL_x8004, SPECIES_GLIMMORA
	setvar VAR_SPECIAL_x8005, 35
	setvar VAR_SPECIAL_x8006, ITEM_GLIMMORANITE
	setvar VAR_SPECIAL_x8007, 2347
	callstd 2077
	end
// hack: COALOSSAL specialist (hack/scripts/gen_specialists.py)
scr_seq_D42R0101_003:
	setvar VAR_SPECIAL_x8004, SPECIES_COALOSSAL
	setvar VAR_SPECIAL_x8005, 34
	setvar VAR_SPECIAL_x8006, ITEM_HEAVY_DUTY_BOOTS
	setvar VAR_SPECIAL_x8007, 2622
	callstd 2077
	end
// hack: SALAMENCE specialist (hack/scripts/gen_specialists.py)
scr_seq_D42R0101_004:
	setvar VAR_SPECIAL_x8004, SPECIES_SALAMENCE
	setvar VAR_SPECIAL_x8005, 50
	setvar VAR_SPECIAL_x8006, ITEM_SALAMENCITE
	setvar VAR_SPECIAL_x8007, 2641
	callstd 2077
	end
	.balign 4
