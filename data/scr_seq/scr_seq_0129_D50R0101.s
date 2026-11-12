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

.include "data/scr_seq/include/event_D50R0101.inc"


// text archive to grab from: 144.txt

.data


scrdef scr_seq_D50R0101_000
scrdef scr_seq_D50R0101_001
scrdef scr_seq_D50R0101_002
scrdef scr_seq_D50R0101_003
scrdef scr_seq_D50R0101_004
scrdef scr_seq_D50R0101_005
scrdef_end

scr_seq_D50R0101_001:
	nat_dex_flag_action 2, VAR_TEMP_x4000
	compare VAR_TEMP_x4000, 1
	goto_if_eq _0064
	move_person_facing obj_D50R0101_breakrock, 30, 1, 30, DIR_NORTH
	move_person_facing obj_D50R0101_breakrock_2, 30, 1, 30, DIR_NORTH
	move_person_facing obj_D50R0101_breakrock_3, 30, 1, 30, DIR_NORTH
	move_person_facing obj_D50R0101_breakrock_4, 30, 1, 30, DIR_NORTH
	move_person_facing obj_D50R0101_breakrock_5, 30, 1, 30, DIR_NORTH
	move_person_facing obj_D50R0101_breakrock_6, 30, 1, 30, DIR_NORTH
_0064:
	end

scr_seq_D50R0101_000:
	simple_npc_msg 0
	end
// hack: DURANT specialist (hack/scripts/gen_specialists.py)
scr_seq_D50R0101_002:
	setvar VAR_SPECIAL_x8004, SPECIES_DURANT
	setvar VAR_SPECIAL_x8005, 23
	setvar VAR_SPECIAL_x8006, ITEM_EVIOLITE
	setvar VAR_SPECIAL_x8007, 2532
	callstd 2077
	end
// hack: TINKATON specialist (hack/scripts/gen_specialists.py)
scr_seq_D50R0101_003:
	setvar VAR_SPECIAL_x8004, SPECIES_TINKATON
	setvar VAR_SPECIAL_x8005, 38
	setvar VAR_SPECIAL_x8006, ITEM_LIFE_ORB
	setvar VAR_SPECIAL_x8007, 2276
	callstd 2077
	end
// hack: COPPERAJAH specialist (hack/scripts/gen_specialists.py)
scr_seq_D50R0101_004:
	setvar VAR_SPECIAL_x8004, SPECIES_COPPERAJAH
	setvar VAR_SPECIAL_x8005, 34
	setvar VAR_SPECIAL_x8006, ITEM_FOCUS_SASH
	setvar VAR_SPECIAL_x8007, 2386
	callstd 2077
	end
// hack: CINDERACE specialist (hack/scripts/gen_specialists.py)
scr_seq_D50R0101_005:
	setvar VAR_SPECIAL_x8004, SPECIES_CINDERACE
	setvar VAR_SPECIAL_x8005, 35
	setvar VAR_SPECIAL_x8006, ITEM_ABILITY_CAPSULE
	setvar VAR_SPECIAL_x8007, 2652
	callstd 2077
	end
	.balign 4
