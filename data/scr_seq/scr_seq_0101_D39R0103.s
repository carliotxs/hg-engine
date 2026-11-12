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

.include "data/scr_seq/include/event_D39R0103.inc"


// text archive to grab from: 123.txt

.data


scrdef scr_seq_D39R0103_000
scrdef scr_seq_D39R0103_001
scrdef scr_seq_D39R0103_002
scrdef scr_seq_D39R0103_003
scrdef scr_seq_D39R0103_004
scrdef scr_seq_D39R0103_005
scrdef scr_seq_D39R0103_006
scrdef_end

scr_seq_D39R0103_000:
	play_se SEQ_SE_GS_RAKKA01
	apply_movement obj_player, _0050
	wait 1, VAR_SPECIAL_RESULT
	scrcmd_374 obj_player
	wait_movement
	screen_shake 0, 1, 1, 8
	play_se SEQ_SE_DP_SUTYA2
	setvar VAR_UNK_40AB, 0
	end

scr_seq_D39R0103_001:
	compare VAR_UNK_40AB, 1
	goto_if_ne _004D
	make_object_visible obj_player
_004D:
	end

	.byte 0x00
	.balign 4
_0050:

	step 68, 1
	step_end
scr_seq_D39R0103_002:
	simple_npc_msg 0
	end
// hack: DELIBIRD specialist (hack/scripts/gen_specialists.py)
scr_seq_D39R0103_003:
	setvar VAR_SPECIAL_x8004, SPECIES_DELIBIRD
	setvar VAR_SPECIAL_x8005, 26
	setvar VAR_SPECIAL_x8006, ITEM_LIFE_ORB
	setvar VAR_SPECIAL_x8007, 2286
	callstd 2077
	end
// hack: VANILLUXE specialist (hack/scripts/gen_specialists.py)
scr_seq_D39R0103_004:
	setvar VAR_SPECIAL_x8004, SPECIES_VANILLUXE
	setvar VAR_SPECIAL_x8005, 47
	setvar VAR_SPECIAL_x8006, ITEM_AIR_BALLOON
	setvar VAR_SPECIAL_x8007, 2323
	callstd 2077
	end
// hack: FROSMOTH specialist (hack/scripts/gen_specialists.py)
scr_seq_D39R0103_005:
	setvar VAR_SPECIAL_x8004, SPECIES_FROSMOTH
	setvar VAR_SPECIAL_x8005, 26
	setvar VAR_SPECIAL_x8006, ITEM_SITRUS_BERRY
	setvar VAR_SPECIAL_x8007, 2342
	callstd 2077
	end
// hack: CROBAT specialist (hack/scripts/gen_specialists.py)
scr_seq_D39R0103_006:
	setvar VAR_SPECIAL_x8004, SPECIES_CROBAT
	setvar VAR_SPECIAL_x8005, 26
	setvar VAR_SPECIAL_x8006, ITEM_LIFE_ORB
	setvar VAR_SPECIAL_x8007, 2680
	callstd 2077
	end
	.balign 4
