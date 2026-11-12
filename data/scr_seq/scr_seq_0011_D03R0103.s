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

.include "data/scr_seq/include/event_D03R0103.inc"


// text archive to grab from: 003.txt

.data


scrdef scr_seq_D03R0103_000
scrdef scr_seq_D03R0103_001
scrdef scr_seq_D03R0103_002
scrdef scr_seq_D03R0103_003
scrdef scr_seq_D03R0103_004
scrdef scr_seq_D03R0103_005
scrdef scr_seq_D03R0103_006
scrdef_end

scr_seq_D03R0103_001:
	goto_if_set FLAG_ENGAGING_STATIC_POKEMON, _0017
	end

_0017:
	setflag FLAG_HIDE_CERULEAN_CAVE_MEWTWO
	hide_person obj_D03R0103_follower_mon_static_mewtwo
	clearflag FLAG_ENGAGING_STATIC_POKEMON
	end

scr_seq_D03R0103_000:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	play_cry SPECIES_MEWTWO, 0
	wait_cry
	setflag FLAG_ENGAGING_STATIC_POKEMON
	wild_battle SPECIES_MEWTWO, 70, 0
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
	setflag FLAG_CAUGHT_MEWTWO
	return
// hack: MACHAMP specialist (hack/scripts/gen_specialists.py)
scr_seq_D03R0103_002:
	setvar VAR_SPECIAL_x8004, SPECIES_MACHAMP
	setvar VAR_SPECIAL_x8005, 48
	setvar VAR_SPECIAL_x8006, ITEM_MUSCLE_BAND
	setvar VAR_SPECIAL_x8007, 2694
	callstd 2077
	end
// hack: MINIOR specialist (hack/scripts/gen_specialists.py)
scr_seq_D03R0103_003:
	setvar VAR_SPECIAL_x8004, SPECIES_MINIOR
	setvar VAR_SPECIAL_x8005, 33
	setvar VAR_SPECIAL_x8006, ITEM_MUSCLE_BAND
	setvar VAR_SPECIAL_x8007, 2695
	callstd 2077
	end
// hack: PARASECT specialist (hack/scripts/gen_specialists.py)
scr_seq_D03R0103_004:
	setvar VAR_SPECIAL_x8004, SPECIES_PARASECT
	setvar VAR_SPECIAL_x8005, 48
	setvar VAR_SPECIAL_x8006, ITEM_RED_CARD
	setvar VAR_SPECIAL_x8007, 2696
	callstd 2077
	end
// hack: LUXRAY specialist (hack/scripts/gen_specialists.py)
scr_seq_D03R0103_005:
	setvar VAR_SPECIAL_x8004, SPECIES_LUXRAY
	setvar VAR_SPECIAL_x8005, 49
	setvar VAR_SPECIAL_x8006, ITEM_WISE_GLASSES
	setvar VAR_SPECIAL_x8007, 2375
	callstd 2077
	end
// hack: CHANDELURE specialist (hack/scripts/gen_specialists.py)
scr_seq_D03R0103_006:
	setvar VAR_SPECIAL_x8004, SPECIES_CHANDELURE
	setvar VAR_SPECIAL_x8005, 48
	setvar VAR_SPECIAL_x8006, ITEM_CHANDELURITE
	setvar VAR_SPECIAL_x8007, 2632
	callstd 2077
	end
	.balign 4
