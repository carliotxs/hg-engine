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

.include "data/scr_seq/include/event_R06.inc"


// text archive to grab from: 334.txt

.data


scrdef scr_seq_R06_000
scrdef scr_seq_R06_001
scrdef scr_seq_R06_002
scrdef scr_seq_R06_003
scrdef scr_seq_R06_004
scrdef scr_seq_R06_005
scrdef scr_seq_R06_006
scrdef scr_seq_R06_007
scrdef_end

scr_seq_R06_000:
	simple_npc_msg 0
	end

scr_seq_R06_001:
	scrcmd_055 2, 0
	scrcmd_057 3
	scrcmd_058
	trainer_tips 1, VAR_SPECIAL_RESULT
	callstd std_signpost
	end
// hack: BELLIBOLT specialist (hack/scripts/gen_specialists.py)
scr_seq_R06_002:
	setvar VAR_SPECIAL_x8004, SPECIES_BELLIBOLT
	setvar VAR_SPECIAL_x8005, 18
	setvar VAR_SPECIAL_x8006, ITEM_WEAKNESS_POLICY
	setvar VAR_SPECIAL_x8007, 2149
	callstd 2077
	end
// hack: STARAPTOR specialist (hack/scripts/gen_specialists.py)
scr_seq_R06_003:
	setvar VAR_SPECIAL_x8004, SPECIES_STARAPTOR
	setvar VAR_SPECIAL_x8005, 34
	setvar VAR_SPECIAL_x8006, ITEM_STARAPTITE
	setvar VAR_SPECIAL_x8007, 2248
	callstd 2077
	end
// hack: SWELLOW specialist (hack/scripts/gen_specialists.py)
scr_seq_R06_004:
	setvar VAR_SPECIAL_x8004, SPECIES_SWELLOW
	setvar VAR_SPECIAL_x8005, 22
	setvar VAR_SPECIAL_x8006, ITEM_ABILITY_CAPSULE
	setvar VAR_SPECIAL_x8007, 2291
	callstd 2077
	end
// hack: DACHSBUN specialist (hack/scripts/gen_specialists.py)
scr_seq_R06_005:
	setvar VAR_SPECIAL_x8004, SPECIES_DACHSBUN
	setvar VAR_SPECIAL_x8005, 26
	setvar VAR_SPECIAL_x8006, ITEM_ABILITY_CAPSULE
	setvar VAR_SPECIAL_x8007, 2346
	callstd 2077
	end
// hack: VILEPLUME specialist (hack/scripts/gen_specialists.py)
scr_seq_R06_006:
	setvar VAR_SPECIAL_x8004, SPECIES_VILEPLUME
	setvar VAR_SPECIAL_x8005, 21
	setvar VAR_SPECIAL_x8006, ITEM_KINGS_ROCK
	setvar VAR_SPECIAL_x8007, 2349
	callstd 2077
	end
// hack: PIDGEOT specialist (hack/scripts/gen_specialists.py)
scr_seq_R06_007:
	setvar VAR_SPECIAL_x8004, SPECIES_PIDGEOT
	setvar VAR_SPECIAL_x8005, 36
	setvar VAR_SPECIAL_x8006, ITEM_PIDGEOTITE
	setvar VAR_SPECIAL_x8007, 2654
	callstd 2077
	end
	.balign 4
