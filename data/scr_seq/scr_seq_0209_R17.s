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

.include "data/scr_seq/include/event_R17.inc"


// text archive to grab from: 357.txt

.data


scrdef scr_seq_R17_000
scrdef scr_seq_R17_001
scrdef scr_seq_R17_002
scrdef scr_seq_R17_003
scrdef scr_seq_R17_004
scrdef_end

scr_seq_R17_000:
	scrcmd_186 1
	end

scr_seq_R17_001:
	scrcmd_186 1
	end
// hack: INDEEDEE specialist (hack/scripts/gen_specialists.py)
scr_seq_R17_002:
	setvar VAR_SPECIAL_x8004, SPECIES_INDEEDEE
	setvar VAR_SPECIAL_x8005, 33
	setvar VAR_SPECIAL_x8006, ITEM_CHOICE_BAND
	setvar VAR_SPECIAL_x8007, 2144
	callstd 2077
	end
// hack: MORPEKO specialist (hack/scripts/gen_specialists.py)
scr_seq_R17_003:
	setvar VAR_SPECIAL_x8004, SPECIES_MORPEKO
	setvar VAR_SPECIAL_x8005, 33
	setvar VAR_SPECIAL_x8006, ITEM_CHOICE_SPECS
	setvar VAR_SPECIAL_x8007, 2145
	callstd 2077
	end
// hack: MAGCARGO specialist (hack/scripts/gen_specialists.py)
scr_seq_R17_004:
	setvar VAR_SPECIAL_x8004, SPECIES_MAGCARGO
	setvar VAR_SPECIAL_x8005, 38
	setvar VAR_SPECIAL_x8006, ITEM_RARE_CANDY
	setvar VAR_SPECIAL_x8007, 2201
	callstd 2077
	end
	.balign 4
