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

.include "data/scr_seq/include/event_R28.inc"


// text archive to grab from: 371.txt

.data


scrdef scr_seq_R28_000
scrdef scr_seq_R28_001
scrdef scr_seq_R28_002
scrdef scr_seq_R28_003
scrdef scr_seq_R28_004
scrdef_end

scr_seq_R28_000:
	setvar VAR_UNK_4126, 0
	end

scr_seq_R28_001:
	direction_signpost 0, 1, 2, VAR_SPECIAL_RESULT
	scrcmd_057 3
	scrcmd_058
	scrcmd_060 VAR_SPECIAL_RESULT
	callstd std_signpost
	end
// hack: CACTURNE specialist (hack/scripts/gen_specialists.py)
scr_seq_R28_002:
	setvar VAR_SPECIAL_x8004, SPECIES_CACTURNE
	setvar VAR_SPECIAL_x8005, 44
	setvar VAR_SPECIAL_x8006, ITEM_BOTTLE_CAP
	setvar VAR_SPECIAL_x8007, 2114
	callstd 2077
	end
// hack: DRAPION specialist (hack/scripts/gen_specialists.py)
scr_seq_R28_003:
	setvar VAR_SPECIAL_x8004, SPECIES_DRAPION
	setvar VAR_SPECIAL_x8005, 45
	setvar VAR_SPECIAL_x8006, ITEM_CHOICE_SCARF
	setvar VAR_SPECIAL_x8007, 2120
	callstd 2077
	end
// hack: MARACTUS specialist (hack/scripts/gen_specialists.py)
scr_seq_R28_004:
	setvar VAR_SPECIAL_x8004, SPECIES_MARACTUS
	setvar VAR_SPECIAL_x8005, 46
	setvar VAR_SPECIAL_x8006, ITEM_AIR_BALLOON
	setvar VAR_SPECIAL_x8007, 2131
	callstd 2077
	end
	.balign 4
