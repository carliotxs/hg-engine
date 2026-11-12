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

.include "data/scr_seq/include/event_R05.inc"


// text archive to grab from: 329.txt

.data


scrdef scr_seq_R05_000
scrdef scr_seq_R05_001
scrdef scr_seq_R05_002
scrdef scr_seq_R05_003
scrdef scr_seq_R05_004
scrdef scr_seq_R05_005
scrdef scr_seq_R05_006
scrdef scr_seq_R05_007
scrdef_end

scr_seq_R05_000:
	simple_npc_msg 0
	end

scr_seq_R05_001:
	scrcmd_055 2, 0
	scrcmd_057 3
	scrcmd_058
	trainer_tips 1, VAR_SPECIAL_RESULT
	callstd std_signpost
	end
// hack: SPINDA specialist (hack/scripts/gen_specialists.py)
scr_seq_R05_002:
	setvar VAR_SPECIAL_x8004, SPECIES_SPINDA
	setvar VAR_SPECIAL_x8005, 17
	setvar VAR_SPECIAL_x8006, ITEM_RED_CARD
	setvar VAR_SPECIAL_x8007, 2243
	callstd 2077
	end
// hack: GOTHITELLE specialist (hack/scripts/gen_specialists.py)
scr_seq_R05_003:
	setvar VAR_SPECIAL_x8004, SPECIES_GOTHITELLE
	setvar VAR_SPECIAL_x8005, 41
	setvar VAR_SPECIAL_x8006, ITEM_EVIOLITE
	setvar VAR_SPECIAL_x8007, 2257
	callstd 2077
	end
// hack: HATTERENE specialist (hack/scripts/gen_specialists.py)
scr_seq_R05_004:
	setvar VAR_SPECIAL_x8004, SPECIES_HATTERENE
	setvar VAR_SPECIAL_x8005, 42
	setvar VAR_SPECIAL_x8006, ITEM_MUSCLE_BAND
	setvar VAR_SPECIAL_x8007, 2272
	callstd 2077
	end
// hack: GARBODOR specialist (hack/scripts/gen_specialists.py)
scr_seq_R05_005:
	setvar VAR_SPECIAL_x8004, SPECIES_GARBODOR
	setvar VAR_SPECIAL_x8005, 36
	setvar VAR_SPECIAL_x8006, ITEM_CHOICE_SPECS
	setvar VAR_SPECIAL_x8007, 2322
	callstd 2077
	end
// hack: BEHEEYEM specialist (hack/scripts/gen_specialists.py)
scr_seq_R05_006:
	setvar VAR_SPECIAL_x8004, SPECIES_BEHEEYEM
	setvar VAR_SPECIAL_x8005, 42
	setvar VAR_SPECIAL_x8006, ITEM_MUSCLE_BAND
	setvar VAR_SPECIAL_x8007, 2325
	callstd 2077
	end
// hack: KLEFKI specialist (hack/scripts/gen_specialists.py)
scr_seq_R05_007:
	setvar VAR_SPECIAL_x8004, SPECIES_KLEFKI
	setvar VAR_SPECIAL_x8005, 15
	setvar VAR_SPECIAL_x8006, ITEM_LIFE_ORB
	setvar VAR_SPECIAL_x8007, 2364
	callstd 2077
	end
	.balign 4
