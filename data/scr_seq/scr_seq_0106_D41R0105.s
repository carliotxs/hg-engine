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

.include "data/scr_seq/include/event_D41R0105.inc"


// text archive to grab from: 003.txt

.data


scrdef scr_seq_D41R0105_000
scrdef scr_seq_D41R0105_001
scrdef scr_seq_D41R0105_002
scrdef scr_seq_D41R0105_003
scrdef scr_seq_D41R0105_004
scrdef scr_seq_D41R0105_005
scrdef scr_seq_D41R0105_006
scrdef_end

scr_seq_D41R0105_001:
	goto_if_set FLAG_ENGAGING_STATIC_POKEMON, _0017
	end

_0017:
	setflag FLAG_HIDE_MT_SILVER_CAVE_MOLTRES
	hide_person obj_D41R0105_follower_mon_static_moltres
	clearflag FLAG_ENGAGING_STATIC_POKEMON
	end

scr_seq_D41R0105_000:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	play_cry SPECIES_MOLTRES, 0
	wait_cry
	setflag FLAG_ENGAGING_STATIC_POKEMON
	wild_battle SPECIES_MOLTRES, 50, 0
	clearflag FLAG_ENGAGING_STATIC_POKEMON
	check_battle_won VAR_SPECIAL_RESULT
	compare VAR_SPECIAL_RESULT, 0
	goto_if_eq _0077
	get_static_encounter_outcome VAR_TEMP_x4002
	compare VAR_TEMP_x4002, 3
	goto_if_eq _0073
	compare VAR_TEMP_x4002, 4
	call_if_eq _007D
_0073:
	releaseall
	end

_0077:
	white_out
	releaseall
	end

_007D:
	setflag FLAG_CAUGHT_MOLTRES
	return
// hack: STEELIX specialist (hack/scripts/gen_specialists.py)
scr_seq_D41R0105_002:
	setvar VAR_SPECIAL_x8004, SPECIES_STEELIX
	setvar VAR_SPECIAL_x8005, 51
	setvar VAR_SPECIAL_x8006, ITEM_STEELIXITE
	setvar VAR_SPECIAL_x8007, 2200
	callstd 2077
	end
// hack: VOLCARONA specialist (hack/scripts/gen_specialists.py)
scr_seq_D41R0105_003:
	setvar VAR_SPECIAL_x8004, SPECIES_VOLCARONA
	setvar VAR_SPECIAL_x8005, 59
	setvar VAR_SPECIAL_x8006, ITEM_BRIGHT_POWDER
	setvar VAR_SPECIAL_x8007, 2362
	callstd 2077
	end
// hack: GOLDUCK specialist (hack/scripts/gen_specialists.py)
scr_seq_D41R0105_004:
	setvar VAR_SPECIAL_x8004, SPECIES_GOLDUCK
	setvar VAR_SPECIAL_x8005, 51
	setvar VAR_SPECIAL_x8006, ITEM_SITRUS_BERRY
	setvar VAR_SPECIAL_x8007, 2370
	callstd 2077
	end
// hack: DRAGAPULT specialist (hack/scripts/gen_specialists.py)
scr_seq_D41R0105_005:
	setvar VAR_SPECIAL_x8004, SPECIES_DRAGAPULT
	setvar VAR_SPECIAL_x8005, 60
	setvar VAR_SPECIAL_x8006, ITEM_WISE_GLASSES
	setvar VAR_SPECIAL_x8007, 2610
	callstd 2077
	end
// hack: ZOROARK specialist (hack/scripts/gen_specialists.py)
scr_seq_D41R0105_006:
	setvar VAR_SPECIAL_x8004, SPECIES_ZOROARK
	setvar VAR_SPECIAL_x8005, 50
	setvar VAR_SPECIAL_x8006, ITEM_FOCUS_SASH
	setvar VAR_SPECIAL_x8007, 2631
	callstd 2077
	end
	.balign 4
