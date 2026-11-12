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

.include "data/scr_seq/include/event_R02.inc"


// text archive to grab from: 320.txt

.data


scrdef scr_seq_R02_000
scrdef scr_seq_R02_001
scrdef scr_seq_R02_002
scrdef scr_seq_R02_003
scrdef scr_seq_R02_004
scrdef scr_seq_R02_005
scrdef scr_seq_R02_006
scrdef scr_seq_R02_007
scrdef_end

scr_seq_R02_000:
	direction_signpost 0, 1, 3, VAR_SPECIAL_RESULT
	scrcmd_057 3
	scrcmd_058
	scrcmd_060 VAR_SPECIAL_RESULT
	callstd std_signpost
	end
// hack: SLAKING specialist (hack/scripts/gen_specialists.py)
scr_seq_R02_001:
	setvar VAR_SPECIAL_x8004, SPECIES_SLAKING
	setvar VAR_SPECIAL_x8005, 36
	setvar VAR_SPECIAL_x8006, ITEM_WEAKNESS_POLICY
	setvar VAR_SPECIAL_x8007, 2113
	callstd 2077
	end
// hack: SIMISAGE specialist (hack/scripts/gen_specialists.py)
scr_seq_R02_002:
	setvar VAR_SPECIAL_x8004, SPECIES_SIMISAGE
	setvar VAR_SPECIAL_x8005, 13
	setvar VAR_SPECIAL_x8006, ITEM_CHOICE_BAND
	setvar VAR_SPECIAL_x8007, 2127
	callstd 2077
	end
// hack: SIMIPOUR specialist (hack/scripts/gen_specialists.py)
scr_seq_R02_003:
	setvar VAR_SPECIAL_x8004, SPECIES_SIMIPOUR
	setvar VAR_SPECIAL_x8005, 11
	setvar VAR_SPECIAL_x8006, ITEM_EXPERT_BELT
	setvar VAR_SPECIAL_x8007, 2128
	callstd 2077
	end
// hack: BEWEAR specialist (hack/scripts/gen_specialists.py)
scr_seq_R02_004:
	setvar VAR_SPECIAL_x8004, SPECIES_BEWEAR
	setvar VAR_SPECIAL_x8005, 27
	setvar VAR_SPECIAL_x8006, ITEM_LUM_BERRY
	setvar VAR_SPECIAL_x8007, 2137
	callstd 2077
	end
// hack: URSALUNA specialist (hack/scripts/gen_specialists.py)
scr_seq_R02_005:
	setvar VAR_SPECIAL_x8004, SPECIES_URSALUNA
	setvar VAR_SPECIAL_x8005, 30
	setvar VAR_SPECIAL_x8006, ITEM_SITRUS_BERRY
	setvar VAR_SPECIAL_x8007, 2147
	callstd 2077
	end
// hack: BRAMBLEGHAST specialist (hack/scripts/gen_specialists.py)
scr_seq_R02_006:
	setvar VAR_SPECIAL_x8004, SPECIES_BRAMBLEGHAST
	setvar VAR_SPECIAL_x8005, 11
	setvar VAR_SPECIAL_x8006, ITEM_KINGS_ROCK
	setvar VAR_SPECIAL_x8007, 2150
	callstd 2077
	end
// hack: SIMISEAR specialist (hack/scripts/gen_specialists.py)
scr_seq_R02_007:
	setvar VAR_SPECIAL_x8004, SPECIES_SIMISEAR
	setvar VAR_SPECIAL_x8005, 10
	setvar VAR_SPECIAL_x8006, ITEM_CHOICE_SCARF
	setvar VAR_SPECIAL_x8007, 2213
	callstd 2077
	end
	.balign 4
