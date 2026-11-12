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

.include "data/scr_seq/include/event_R13.inc"


// text archive to grab from: 350.txt

.data


scrdef scr_seq_R13_000
scrdef scr_seq_R13_001
scrdef scr_seq_R13_002
scrdef scr_seq_R13_003
scrdef scr_seq_R13_004
scrdef_end

scr_seq_R13_000:
	scrcmd_055 3, 0
	scrcmd_057 3
	scrcmd_058
	trainer_tips 0, VAR_SPECIAL_RESULT
	callstd std_signpost
	end

scr_seq_R13_001:
	direction_signpost 1, 1, 10, VAR_SPECIAL_RESULT
	scrcmd_057 3
	scrcmd_058
	scrcmd_060 VAR_SPECIAL_RESULT
	callstd std_signpost
	end

scr_seq_R13_002:
	direction_signpost 2, 1, 14, VAR_SPECIAL_RESULT
	scrcmd_057 3
	scrcmd_058
	scrcmd_060 VAR_SPECIAL_RESULT
	callstd std_signpost
	end
// hack: EXEGGUTOR specialist (hack/scripts/gen_specialists.py)
scr_seq_R13_003:
	setvar VAR_SPECIAL_x8004, SPECIES_EXEGGUTOR
	setvar VAR_SPECIAL_x8005, 25
	setvar VAR_SPECIAL_x8006, ITEM_RED_CARD
	setvar VAR_SPECIAL_x8007, 2554
	callstd 2077
	end
// hack: RHYPERIOR specialist (hack/scripts/gen_specialists.py)
scr_seq_R13_004:
	setvar VAR_SPECIAL_x8004, SPECIES_RHYPERIOR
	setvar VAR_SPECIAL_x8005, 42
	setvar VAR_SPECIAL_x8006, ITEM_QUICK_CLAW
	setvar VAR_SPECIAL_x8007, 2211
	callstd 2077
	end
	.balign 4
