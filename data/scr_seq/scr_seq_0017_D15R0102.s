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

.include "data/scr_seq/include/event_D15R0102.inc"


// text archive to grab from: 055.txt

.data


scrdef scr_seq_D15R0102_000
scrdef scr_seq_D15R0102_001
scrdef scr_seq_D15R0102_002
scrdef scr_seq_D15R0102_003
scrdef scr_seq_D15R0102_004
scrdef_end

scr_seq_D15R0102_000:
	end

scr_seq_D15R0102_001:
	simple_npc_msg 0
	end

scr_seq_D15R0102_002:
	simple_npc_msg 1
	end
// hack: POLTEAGEIST specialist (hack/scripts/gen_specialists.py)
scr_seq_D15R0102_003:
	setvar VAR_SPECIAL_x8004, SPECIES_POLTEAGEIST
	setvar VAR_SPECIAL_x8005, 8
	setvar VAR_SPECIAL_x8006, ITEM_WEAKNESS_POLICY
	setvar VAR_SPECIAL_x8007, 2228
	callstd 2077
	end
// hack: CHIMECHO specialist (hack/scripts/gen_specialists.py)
scr_seq_D15R0102_004:
	setvar VAR_SPECIAL_x8004, SPECIES_CHIMECHO
	setvar VAR_SPECIAL_x8005, 6
	setvar VAR_SPECIAL_x8006, ITEM_CHIMECHITE
	setvar VAR_SPECIAL_x8007, 2246
	callstd 2077
	end
	.balign 4
