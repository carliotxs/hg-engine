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

.include "data/scr_seq/include/event_T21FS0101.inc"


// text archive to grab from: 551.txt

.data


scrdef scr_seq_T21FS0101_000
scrdef scr_seq_T21FS0101_001
scrdef scr_seq_T21FS0101_002
scrdef scr_seq_T21FS0101_003
scrdef scr_seq_T21FS0101_004
scrdef_end

scr_seq_T21FS0101_000:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	callstd std_mart_intro
	holdmsg
	setvar VAR_SPECIAL_x8004, 0
	callstd std_pokemart
	releaseall
	end

scr_seq_T21FS0101_003:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	callstd std_mart_intro
	holdmsg
	setvar VAR_SPECIAL_x8004, 0
	callstd std_special_mart
	releaseall
	end

scr_seq_T21FS0101_002:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	compare VAR_SCENE_ELMS_LAB, 4
	goto_if_lt _0068
	npc_msg 1
	goto _006B

_0068:
	npc_msg 0
_006B:
	wait_button
	closemsg
	releaseall
	end

scr_seq_T21FS0101_001:
	simple_npc_msg 2
	end
// hack: random event, a grunt robbing this Poké Mart (hack/scripts/gen_story.py)
scr_seq_T21FS0101_004:
	callstd 2080
	trainer_battle TRAINER_HACK_745, 0, 0, 0
	check_battle_won VAR_SPECIAL_RESULT
	compare VAR_SPECIAL_RESULT, 0
	goto_if_eq scr_seq_T21FS0101_004_lost
	setflag 2880 // HACK_DAILY_FLAG_MART_ROBBER: no more robberies today
	setflag 1343
	setvar VAR_SPECIAL_x8006, ITEM_ELIXIR
	callstd 2081
	hide_person obj_T21FS0101_hack_robber
	releaseall
	end

scr_seq_T21FS0101_004_lost:
	white_out
	releaseall
	end
	.balign 4
