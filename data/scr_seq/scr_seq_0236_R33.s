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

.include "data/scr_seq/include/event_R33.inc"


// text archive to grab from: 383.txt

.data


scrdef scr_seq_R33_000
scrdef scr_seq_R33_001
scrdef scr_seq_R33_002
scrdef scr_seq_R33_003
scrdef scr_seq_R33_004
scrdef scr_seq_R33_005
scrdef scr_seq_R33_006
scrdef_end

scr_seq_R33_000:
	simple_npc_msg 0
	end

scr_seq_R33_001:
	direction_signpost 1, 1, 2, VAR_SPECIAL_RESULT
	scrcmd_057 3
	scrcmd_058
	scrcmd_060 VAR_SPECIAL_RESULT
	callstd std_signpost
	end
// hack: visible static Pokémon with daily respawn (hack/scripts/gen_static_mons.py)
scr_seq_R33_002:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	play_cry SPECIES_ZORUA, 0
	wait_cry
	setflag FLAG_ENGAGING_STATIC_POKEMON
	wild_battle SPECIES_ZORUA, 10, 0
	clearflag FLAG_ENGAGING_STATIC_POKEMON
	check_battle_won VAR_SPECIAL_RESULT
	compare VAR_SPECIAL_RESULT, 0
	goto_if_eq scr_seq_R33_002_lost
	setflag FLAG_UNK_B56
	hide_person obj_R33_hack_static
	releaseall
	end

scr_seq_R33_002_lost:
	white_out
	releaseall
	end
// hack: VENUSAUR specialist (hack/scripts/gen_specialists.py)
scr_seq_R33_003:
	setvar VAR_SPECIAL_x8004, SPECIES_VENUSAUR
	setvar VAR_SPECIAL_x8005, 32
	setvar VAR_SPECIAL_x8006, ITEM_VENUSAURITE
	setvar VAR_SPECIAL_x8007, 2567
	callstd 2077
	end
// hack: MEGANIUM specialist (hack/scripts/gen_specialists.py)
scr_seq_R33_004:
	setvar VAR_SPECIAL_x8004, SPECIES_MEGANIUM
	setvar VAR_SPECIAL_x8005, 32
	setvar VAR_SPECIAL_x8006, ITEM_MEGANIUMITE
	setvar VAR_SPECIAL_x8007, 2568
	callstd 2077
	end
// hack: LILLIGANT specialist (hack/scripts/gen_specialists.py)
scr_seq_R33_005:
	setvar VAR_SPECIAL_x8004, SPECIES_LILLIGANT
	setvar VAR_SPECIAL_x8005, 9
	setvar VAR_SPECIAL_x8006, ITEM_SHELL_BELL
	setvar VAR_SPECIAL_x8007, 2215
	callstd 2077
	end
// hack: FLORGES specialist (hack/scripts/gen_specialists.py)
scr_seq_R33_006:
	setvar VAR_SPECIAL_x8004, SPECIES_FLORGES
	setvar VAR_SPECIAL_x8005, 19
	setvar VAR_SPECIAL_x8006, ITEM_HEAVY_DUTY_BOOTS
	setvar VAR_SPECIAL_x8007, 2220
	callstd 2077
	end
	.balign 4
