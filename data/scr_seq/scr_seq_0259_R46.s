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

.include "data/scr_seq/include/event_R46.inc"


// text archive to grab from: 406.txt

.data


scrdef scr_seq_R46_000
scrdef scr_seq_R46_001
scrdef scr_seq_R46_002
scrdef scr_seq_R46_003
scrdef scr_seq_R46_004
scrdef scr_seq_R46_005
scrdef scr_seq_R46_006
scrdef scr_seq_R46_007
scrdef_end

scr_seq_R46_000:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	goto_if_set FLAG_UNK_079, _002C
	npc_msg 2
	wait_button
	closemsg
	releaseall
	end

_002C:
	npc_msg 3
	wait_button
	closemsg
	releaseall
	end

scr_seq_R46_001:
	direction_signpost 0, 1, 3, VAR_SPECIAL_RESULT
	scrcmd_057 3
	scrcmd_058
	scrcmd_060 VAR_SPECIAL_RESULT
	callstd std_signpost
	end

scr_seq_R46_002:
	scrcmd_055 2, 0
	scrcmd_057 3
	scrcmd_058
	trainer_tips 1, VAR_SPECIAL_RESULT
	callstd std_signpost
	end
// hack: BRAVIARY specialist (hack/scripts/gen_specialists.py)
scr_seq_R46_003:
	setvar VAR_SPECIAL_x8004, SPECIES_BRAVIARY
	setvar VAR_SPECIAL_x8005, 54
	setvar VAR_SPECIAL_x8006, ITEM_EXPERT_BELT
	setvar VAR_SPECIAL_x8007, 2175
	callstd 2077
	end
// hack: MANDIBUZZ specialist (hack/scripts/gen_specialists.py)
scr_seq_R46_004:
	setvar VAR_SPECIAL_x8004, SPECIES_MANDIBUZZ
	setvar VAR_SPECIAL_x8005, 54
	setvar VAR_SPECIAL_x8006, ITEM_ASSAULT_VEST
	setvar VAR_SPECIAL_x8007, 2176
	callstd 2077
	end
// hack: GOGOAT specialist (hack/scripts/gen_specialists.py)
scr_seq_R46_005:
	setvar VAR_SPECIAL_x8004, SPECIES_GOGOAT
	setvar VAR_SPECIAL_x8005, 32
	setvar VAR_SPECIAL_x8006, ITEM_RARE_CANDY
	setvar VAR_SPECIAL_x8007, 2330
	callstd 2077
	end
// hack: CORVIKNIGHT specialist (hack/scripts/gen_specialists.py)
scr_seq_R46_006:
	setvar VAR_SPECIAL_x8004, SPECIES_CORVIKNIGHT
	setvar VAR_SPECIAL_x8005, 38
	setvar VAR_SPECIAL_x8006, ITEM_FOCUS_SASH
	setvar VAR_SPECIAL_x8007, 2384
	callstd 2077
	end
// hack: PYROAR specialist (hack/scripts/gen_specialists.py)
scr_seq_R46_007:
	setvar VAR_SPECIAL_x8004, SPECIES_PYROAR
	setvar VAR_SPECIAL_x8005, 35
	setvar VAR_SPECIAL_x8006, ITEM_PYROARITE
	setvar VAR_SPECIAL_x8007, 2618
	callstd 2077
	end
	.balign 4
