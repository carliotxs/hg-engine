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

.include "data/scr_seq/include/event_D11R0105.inc"


// text archive to grab from: 003.txt

.data


scrdef scr_seq_D11R0105_000
scrdef scr_seq_D11R0105_001
scrdef scr_seq_D11R0105_002
scrdef scr_seq_D11R0105_003
scrdef scr_seq_D11R0105_004
scrdef scr_seq_D11R0105_005
scrdef_end

scr_seq_D11R0105_001:
	goto_if_set FLAG_ENGAGING_STATIC_POKEMON, _0017
	end

_0017:
	setflag FLAG_HIDE_SEAFOAM_ISLAND_ARTICUNO
	hide_person obj_D11R0105_follower_mon_static_articuno
	clearflag FLAG_ENGAGING_STATIC_POKEMON
	end

scr_seq_D11R0105_000:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	play_cry SPECIES_ARTICUNO, 0
	wait_cry
	setflag FLAG_ENGAGING_STATIC_POKEMON
	wild_battle SPECIES_ARTICUNO, 50, 0
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
	setflag FLAG_CAUGHT_ARTICUNO
	return
// hack: KINGDRA specialist (hack/scripts/gen_specialists.py)
scr_seq_D11R0105_002:
	setvar VAR_SPECIAL_x8004, SPECIES_KINGDRA
	setvar VAR_SPECIAL_x8005, 43
	setvar VAR_SPECIAL_x8006, ITEM_EXPERT_BELT
	setvar VAR_SPECIAL_x8007, 2202
	callstd 2077
	end
// hack: ABOMASNOW specialist (hack/scripts/gen_specialists.py)
scr_seq_D11R0105_003:
	setvar VAR_SPECIAL_x8004, SPECIES_ABOMASNOW
	setvar VAR_SPECIAL_x8005, 42
	setvar VAR_SPECIAL_x8006, ITEM_MUSCLE_BAND
	setvar VAR_SPECIAL_x8007, 2309
	callstd 2077
	end
// hack: CRYOGONAL specialist (hack/scripts/gen_specialists.py)
scr_seq_D11R0105_004:
	setvar VAR_SPECIAL_x8004, SPECIES_CRYOGONAL
	setvar VAR_SPECIAL_x8005, 43
	setvar VAR_SPECIAL_x8006, ITEM_HEAVY_DUTY_BOOTS
	setvar VAR_SPECIAL_x8007, 2327
	callstd 2077
	end
// hack: CETITAN specialist (hack/scripts/gen_specialists.py)
scr_seq_D11R0105_005:
	setvar VAR_SPECIAL_x8004, SPECIES_CETITAN
	setvar VAR_SPECIAL_x8005, 42
	setvar VAR_SPECIAL_x8006, ITEM_KINGS_ROCK
	setvar VAR_SPECIAL_x8007, 2348
	callstd 2077
	end
	.balign 4
