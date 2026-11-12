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

.include "data/scr_seq/include/event_R07.inc"


// text archive to grab from: 336.txt

.data


scrdef scr_seq_R07_000
scrdef scr_seq_R07_001
scrdef scr_seq_R07_002
scrdef scr_seq_R07_003
scrdef scr_seq_R07_004
scrdef scr_seq_R07_005
scrdef scr_seq_R07_006
scrdef scr_seq_R07_007
scrdef scr_seq_R07_008
scrdef_end

scr_seq_R07_000:
	scrcmd_055 2, 0
	scrcmd_057 3
	scrcmd_058
	trainer_tips 0, VAR_SPECIAL_RESULT
	callstd std_signpost
	end

scr_seq_R07_001:
	play_se SEQ_SE_DP_SELECT
	lockall
	npc_msg 1
	wait_button
	closemsg
	releaseall
	end
// hack: HONCHKROW specialist (hack/scripts/gen_specialists.py)
scr_seq_R07_002:
	setvar VAR_SPECIAL_x8004, SPECIES_HONCHKROW
	setvar VAR_SPECIAL_x8005, 20
	setvar VAR_SPECIAL_x8006, ITEM_EVIOLITE
	setvar VAR_SPECIAL_x8007, 2551
	callstd 2077
	end
// hack: SUDOWOODO specialist (hack/scripts/gen_specialists.py)
scr_seq_R07_003:
	setvar VAR_SPECIAL_x8004, SPECIES_SUDOWOODO
	setvar VAR_SPECIAL_x8005, 22
	setvar VAR_SPECIAL_x8006, ITEM_KINGS_ROCK
	setvar VAR_SPECIAL_x8007, 2241
	callstd 2077
	end
// hack: CHATOT specialist (hack/scripts/gen_specialists.py)
scr_seq_R07_004:
	setvar VAR_SPECIAL_x8004, SPECIES_CHATOT
	setvar VAR_SPECIAL_x8005, 22
	setvar VAR_SPECIAL_x8006, ITEM_HEAVY_DUTY_BOOTS
	setvar VAR_SPECIAL_x8007, 2250
	callstd 2077
	end
// hack: LOPUNNY specialist (hack/scripts/gen_specialists.py)
scr_seq_R07_005:
	setvar VAR_SPECIAL_x8004, SPECIES_LOPUNNY
	setvar VAR_SPECIAL_x8005, 22
	setvar VAR_SPECIAL_x8006, ITEM_LOPUNNITE
	setvar VAR_SPECIAL_x8007, 2307
	callstd 2077
	end
// hack: MR_MIME specialist (hack/scripts/gen_specialists.py)
scr_seq_R07_006:
	setvar VAR_SPECIAL_x8004, SPECIES_MR_MIME
	setvar VAR_SPECIAL_x8005, 18
	setvar VAR_SPECIAL_x8006, ITEM_EVIOLITE
	setvar VAR_SPECIAL_x8007, 2351
	callstd 2077
	end
// hack: ROTOM specialist (hack/scripts/gen_specialists.py)
scr_seq_R07_007:
	setvar VAR_SPECIAL_x8004, SPECIES_ROTOM
	setvar VAR_SPECIAL_x8005, 18
	setvar VAR_SPECIAL_x8006, ITEM_CHOICE_SPECS
	setvar VAR_SPECIAL_x8007, 2379
	callstd 2077
	end
// hack: MINUN specialist (hack/scripts/gen_specialists.py)
scr_seq_R07_008:
	setvar VAR_SPECIAL_x8004, SPECIES_MINUN
	setvar VAR_SPECIAL_x8005, 22
	setvar VAR_SPECIAL_x8006, ITEM_CHOICE_SCARF
	setvar VAR_SPECIAL_x8007, 2396
	callstd 2077
	end
	.balign 4
