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

.include "data/scr_seq/include/event_D45R0101.inc"


// text archive to grab from: 003.txt

.data


scrdef scr_seq_D45R0101_000
scrdef scr_seq_D45R0101_001
scrdef scr_seq_D45R0101_002
scrdef scr_seq_D45R0101_003
scrdef scr_seq_D45R0101_004
scrdef_end

scr_seq_D45R0101_000:
	make_object_visible obj_D45R0101_stop
	end
// hack: PROBOPASS specialist (hack/scripts/gen_specialists.py)
scr_seq_D45R0101_001:
	setvar VAR_SPECIAL_x8004, SPECIES_PROBOPASS
	setvar VAR_SPECIAL_x8005, 25
	setvar VAR_SPECIAL_x8006, ITEM_LEFTOVERS
	setvar VAR_SPECIAL_x8007, 2312
	callstd 2077
	end
// hack: EXCADRILL specialist (hack/scripts/gen_specialists.py)
scr_seq_D45R0101_002:
	setvar VAR_SPECIAL_x8004, SPECIES_EXCADRILL
	setvar VAR_SPECIAL_x8005, 31
	setvar VAR_SPECIAL_x8006, ITEM_EJECT_BUTTON
	setvar VAR_SPECIAL_x8007, 2317
	callstd 2077
	end
// hack: NOIVERN specialist (hack/scripts/gen_specialists.py)
scr_seq_D45R0101_003:
	setvar VAR_SPECIAL_x8004, SPECIES_NOIVERN
	setvar VAR_SPECIAL_x8005, 48
	setvar VAR_SPECIAL_x8006, ITEM_WEAKNESS_POLICY
	setvar VAR_SPECIAL_x8007, 2621
	callstd 2077
	end
// hack: GARCHOMP specialist (hack/scripts/gen_specialists.py)
scr_seq_D45R0101_004:
	setvar VAR_SPECIAL_x8004, SPECIES_GARCHOMP
	setvar VAR_SPECIAL_x8005, 48
	setvar VAR_SPECIAL_x8006, ITEM_GARCHOMPITE
	setvar VAR_SPECIAL_x8007, 2645
	callstd 2077
	end
	.balign 4
