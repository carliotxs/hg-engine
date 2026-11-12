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

.include "data/scr_seq/include/event_R15.inc"


// text archive to grab from: 352.txt

.data


scrdef scr_seq_R15_000
scrdef scr_seq_R15_001
scrdef scr_seq_R15_002
scrdef scr_seq_R15_003
scrdef scr_seq_R15_004
scrdef scr_seq_R15_005
scrdef scr_seq_R15_006
scrdef_end

scr_seq_R15_000:
	direction_signpost 0, 1, 10, VAR_SPECIAL_RESULT
	scrcmd_057 3
	scrcmd_058
	scrcmd_060 VAR_SPECIAL_RESULT
	callstd std_signpost
	end
// hack: TROPIUS specialist (hack/scripts/gen_specialists.py)
scr_seq_R15_001:
	setvar VAR_SPECIAL_x8004, SPECIES_TROPIUS
	setvar VAR_SPECIAL_x8005, 27
	setvar VAR_SPECIAL_x8006, ITEM_HEAVY_DUTY_BOOTS
	setvar VAR_SPECIAL_x8007, 2208
	callstd 2077
	end
// hack: MALAMAR specialist (hack/scripts/gen_specialists.py)
scr_seq_R15_002:
	setvar VAR_SPECIAL_x8004, SPECIES_MALAMAR
	setvar VAR_SPECIAL_x8005, 30
	setvar VAR_SPECIAL_x8006, ITEM_MALAMARITE
	setvar VAR_SPECIAL_x8007, 2221
	callstd 2077
	end
// hack: SEVIPER specialist (hack/scripts/gen_specialists.py)
scr_seq_R15_003:
	setvar VAR_SPECIAL_x8004, SPECIES_SEVIPER
	setvar VAR_SPECIAL_x8005, 25
	setvar VAR_SPECIAL_x8006, ITEM_LEFTOVERS
	setvar VAR_SPECIAL_x8007, 2244
	callstd 2077
	end
// hack: NIDOQUEEN specialist (hack/scripts/gen_specialists.py)
scr_seq_R15_004:
	setvar VAR_SPECIAL_x8004, SPECIES_NIDOQUEEN
	setvar VAR_SPECIAL_x8005, 26
	setvar VAR_SPECIAL_x8006, ITEM_CHOICE_SPECS
	setvar VAR_SPECIAL_x8007, 2280
	callstd 2077
	end
// hack: NIDOKING specialist (hack/scripts/gen_specialists.py)
scr_seq_R15_005:
	setvar VAR_SPECIAL_x8004, SPECIES_NIDOKING
	setvar VAR_SPECIAL_x8005, 26
	setvar VAR_SPECIAL_x8006, ITEM_EXPERT_BELT
	setvar VAR_SPECIAL_x8007, 2281
	callstd 2077
	end
// hack: HOUNDSTONE specialist (hack/scripts/gen_specialists.py)
scr_seq_R15_006:
	setvar VAR_SPECIAL_x8004, SPECIES_HOUNDSTONE
	setvar VAR_SPECIAL_x8005, 30
	setvar VAR_SPECIAL_x8006, ITEM_SCOPE_LENS
	setvar VAR_SPECIAL_x8007, 2368
	callstd 2077
	end
	.balign 4
