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
	.balign 4
