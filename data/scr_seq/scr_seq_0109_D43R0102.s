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

.include "data/scr_seq/include/event_D43R0102.inc"


// text archive to grab from: 003.txt

.data


scrdef scr_seq_D43R0102_000
scrdef scr_seq_D43R0102_001
scrdef scr_seq_D43R0102_002
scrdef scr_seq_D43R0102_003
scrdef scr_seq_D43R0102_004
scrdef scr_seq_D43R0102_005
scrdef scr_seq_D43R0102_006
scrdef scr_seq_D43R0102_007
scrdef_end

scr_seq_D43R0102_000:
	play_se SEQ_SE_GS_RAKKA01
	apply_movement obj_player, _0048
	scrcmd_374 obj_player
	wait_movement
	screen_shake 0, 1, 1, 8
	play_se SEQ_SE_DP_SUTYA2
	setvar VAR_UNK_40CA, 0
	end

scr_seq_D43R0102_001:
	compare VAR_UNK_40CA, 1
	goto_if_ne _0043
	make_object_visible obj_player
_0043:
	end

	.byte 0x00, 0x00, 0x00
	.balign 4
_0048:

	step 68, 1
	step_end
// hack: DRUDDIGON specialist (hack/scripts/gen_specialists.py)
scr_seq_D43R0102_002:
	setvar VAR_SPECIAL_x8004, SPECIES_DRUDDIGON
	setvar VAR_SPECIAL_x8005, 39
	setvar VAR_SPECIAL_x8006, ITEM_SITRUS_BERRY
	setvar VAR_SPECIAL_x8007, 2135
	callstd 2077
	end
// hack: AEGISLASH specialist (hack/scripts/gen_specialists.py)
scr_seq_D43R0102_003:
	setvar VAR_SPECIAL_x8004, SPECIES_AEGISLASH
	setvar VAR_SPECIAL_x8005, 36
	setvar VAR_SPECIAL_x8006, ITEM_CHOICE_SPECS
	setvar VAR_SPECIAL_x8007, 2180
	callstd 2077
	end
// hack: FALINKS specialist (hack/scripts/gen_specialists.py)
scr_seq_D43R0102_004:
	setvar VAR_SPECIAL_x8004, SPECIES_FALINKS
	setvar VAR_SPECIAL_x8005, 36
	setvar VAR_SPECIAL_x8006, ITEM_FALINKSITE
	setvar VAR_SPECIAL_x8007, 2229
	callstd 2077
	end
// hack: ARMAROUGE specialist (hack/scripts/gen_specialists.py)
scr_seq_D43R0102_005:
	setvar VAR_SPECIAL_x8004, SPECIES_ARMAROUGE
	setvar VAR_SPECIAL_x8005, 36
	setvar VAR_SPECIAL_x8006, ITEM_EXPERT_BELT
	setvar VAR_SPECIAL_x8007, 2235
	callstd 2077
	end
// hack: CERULEDGE specialist (hack/scripts/gen_specialists.py)
scr_seq_D43R0102_006:
	setvar VAR_SPECIAL_x8004, SPECIES_CERULEDGE
	setvar VAR_SPECIAL_x8005, 36
	setvar VAR_SPECIAL_x8006, ITEM_ROCKY_HELMET
	setvar VAR_SPECIAL_x8007, 2236
	callstd 2077
	end
// hack: GOLURK specialist (hack/scripts/gen_specialists.py)
scr_seq_D43R0102_007:
	setvar VAR_SPECIAL_x8004, SPECIES_GOLURK
	setvar VAR_SPECIAL_x8005, 43
	setvar VAR_SPECIAL_x8006, ITEM_GOLURKITE
	setvar VAR_SPECIAL_x8007, 2328
	callstd 2077
	end
	.balign 4
