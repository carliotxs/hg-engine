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

.include "data/scr_seq/include/event_R44.inc"


// text archive to grab from: 404.txt

.data


scrdef scr_seq_R44_000
scrdef scr_seq_R44_001
scrdef scr_seq_R44_002
scrdef scr_seq_R44_003
scrdef scr_seq_R44_004
scrdef scr_seq_R44_005
scrdef scr_seq_R44_006
scrdef scr_seq_R44_007
scrdef scr_seq_R44_008
scrdef_end

scr_seq_R44_000:
	end

scr_seq_R44_001:
	scrcmd_055 2, 0
	scrcmd_057 3
	scrcmd_058
	trainer_tips 0, VAR_SPECIAL_RESULT
	callstd std_signpost
	end

scr_seq_R44_002:
	direction_signpost 1, 1, 1, VAR_SPECIAL_RESULT
	scrcmd_057 3
	scrcmd_058
	scrcmd_060 VAR_SPECIAL_RESULT
	callstd std_signpost
	end
// hack: visible static Pokémon with daily respawn (hack/scripts/gen_static_mons.py)
scr_seq_R44_003:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	play_cry SPECIES_AXEW, 0
	wait_cry
	setflag FLAG_ENGAGING_STATIC_POKEMON
	wild_battle SPECIES_AXEW, 25, 0
	clearflag FLAG_ENGAGING_STATIC_POKEMON
	check_battle_won VAR_SPECIAL_RESULT
	compare VAR_SPECIAL_RESULT, 0
	goto_if_eq scr_seq_R44_003_lost
	setflag FLAG_UNK_B5B
	hide_person obj_R44_hack_static
	releaseall
	end

scr_seq_R44_003_lost:
	white_out
	releaseall
	end
// hack: LICKILICKY specialist (hack/scripts/gen_specialists.py)
scr_seq_R44_004:
	setvar VAR_SPECIAL_x8004, SPECIES_LICKILICKY
	setvar VAR_SPECIAL_x8005, 27
	setvar VAR_SPECIAL_x8006, ITEM_BRIGHT_POWDER
	setvar VAR_SPECIAL_x8007, 2578
	callstd 2077
	end
// hack: YANMEGA specialist (hack/scripts/gen_specialists.py)
scr_seq_R44_005:
	setvar VAR_SPECIAL_x8004, SPECIES_YANMEGA
	setvar VAR_SPECIAL_x8005, 27
	setvar VAR_SPECIAL_x8006, ITEM_HEAVY_DUTY_BOOTS
	setvar VAR_SPECIAL_x8007, 2579
	callstd 2077
	end
// hack: TANGROWTH specialist (hack/scripts/gen_specialists.py)
scr_seq_R44_006:
	setvar VAR_SPECIAL_x8004, SPECIES_TANGROWTH
	setvar VAR_SPECIAL_x8005, 26
	setvar VAR_SPECIAL_x8006, ITEM_KINGS_ROCK
	setvar VAR_SPECIAL_x8007, 2251
	callstd 2077
	end
// hack: DRIFBLIM specialist (hack/scripts/gen_specialists.py)
scr_seq_R44_007:
	setvar VAR_SPECIAL_x8004, SPECIES_DRIFBLIM
	setvar VAR_SPECIAL_x8005, 28
	setvar VAR_SPECIAL_x8006, ITEM_EXPERT_BELT
	setvar VAR_SPECIAL_x8007, 2376
	callstd 2077
	end
// hack: LIEPARD specialist (hack/scripts/gen_specialists.py)
scr_seq_R44_008:
	setvar VAR_SPECIAL_x8004, SPECIES_LIEPARD
	setvar VAR_SPECIAL_x8005, 25
	setvar VAR_SPECIAL_x8006, ITEM_LEFTOVERS
	setvar VAR_SPECIAL_x8007, 2617
	callstd 2077
	end
	.balign 4
