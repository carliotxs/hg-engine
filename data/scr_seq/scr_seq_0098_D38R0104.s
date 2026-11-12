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

.include "data/scr_seq/include/event_D38R0104.inc"


// text archive to grab from: 121.txt

.data


scrdef scr_seq_D38R0104_000
scrdef scr_seq_D38R0104_001
scrdef scr_seq_D38R0104_002
scrdef scr_seq_D38R0104_003
scrdef scr_seq_D38R0104_004
scrdef_end

scr_seq_D38R0104_000:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	goto_if_set FLAG_GOT_TYROGUE_FROM_KARATE_KING, _0097
	goto_if_set FLAG_BEAT_KARATE_KING, _0046
	npc_msg 0
	closemsg
	trainer_battle TRAINER_BLACK_BELT_KIYO, 0, 0, 0
	check_battle_won VAR_SPECIAL_RESULT
	compare VAR_SPECIAL_RESULT, 0
	goto_if_eq _00CC
	setflag FLAG_BEAT_KARATE_KING
_0046:
	npc_msg 1
	get_party_count VAR_SPECIAL_x8005
	compare VAR_SPECIAL_x8005, 6
	goto_if_ne _0063
	npc_msg 4
	goto _00D2

_0063:
	buffer_players_name 0
	npc_msg 2
	play_fanfare SEQ_ME_POKEGET
	wait_fanfare
	give_mon SPECIES_TYROGUE, 10, 0, 0, 0, VAR_SPECIAL_RESULT
	npc_msg 5
	touchscreen_menu_hide
	getmenuchoice VAR_SPECIAL_RESULT
	closemsg
	compare VAR_SPECIAL_RESULT, 0
	call_if_eq _00A6
	touchscreen_menu_show
_0097:
	setflag FLAG_GOT_TYROGUE_FROM_KARATE_KING
	npc_msg 3
	wait_button
	closemsg
	releaseall
	end

_00A6:
	setvar VAR_TEMP_x4000, 0
	fade_screen 6, 1, 0, RGB_BLACK
	wait_fade
	nickname_input VAR_SPECIAL_x8005, VAR_TEMP_x4000
	fade_screen 6, 1, 1, RGB_BLACK
	wait_fade
	return

_00CC:
	white_out
	releaseall
	end

_00D2:
	wait_button
	closemsg
	releaseall
	end
// hack: TORKOAL specialist (hack/scripts/gen_specialists.py)
scr_seq_D38R0104_001:
	setvar VAR_SPECIAL_x8004, SPECIES_TORKOAL
	setvar VAR_SPECIAL_x8005, 19
	setvar VAR_SPECIAL_x8006, ITEM_QUICK_CLAW
	setvar VAR_SPECIAL_x8007, 2207
	callstd 2077
	end
// hack: SANDACONDA specialist (hack/scripts/gen_specialists.py)
scr_seq_D38R0104_002:
	setvar VAR_SPECIAL_x8004, SPECIES_SANDACONDA
	setvar VAR_SPECIAL_x8005, 36
	setvar VAR_SPECIAL_x8006, ITEM_LUM_BERRY
	setvar VAR_SPECIAL_x8007, 2227
	callstd 2077
	end
// hack: EELEKTROSS specialist (hack/scripts/gen_specialists.py)
scr_seq_D38R0104_003:
	setvar VAR_SPECIAL_x8004, SPECIES_EELEKTROSS
	setvar VAR_SPECIAL_x8005, 39
	setvar VAR_SPECIAL_x8006, ITEM_EELEKTROSSITE
	setvar VAR_SPECIAL_x8007, 2381
	callstd 2077
	end
// hack: INCINEROAR specialist (hack/scripts/gen_specialists.py)
scr_seq_D38R0104_004:
	setvar VAR_SPECIAL_x8004, SPECIES_INCINEROAR
	setvar VAR_SPECIAL_x8005, 34
	setvar VAR_SPECIAL_x8006, ITEM_HEAVY_DUTY_BOOTS
	setvar VAR_SPECIAL_x8007, 2650
	callstd 2077
	end
	.balign 4
