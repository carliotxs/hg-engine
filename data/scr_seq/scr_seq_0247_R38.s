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

.include "data/scr_seq/include/event_R38.inc"


// text archive to grab from: 394.txt

.data


scrdef scr_seq_R38_000
scrdef scr_seq_R38_001
scrdef scr_seq_R38_002
scrdef scr_seq_R38_003
scrdef scr_seq_R38_004
scrdef scr_seq_R38_005
scrdef scr_seq_R38_006
scrdef scr_seq_R38_007
scrdef scr_seq_R38_008
scrdef scr_seq_R38_009
scrdef_end

scr_seq_R38_000:
	end

scr_seq_R38_001:
	direction_signpost 15, 1, 8, VAR_SPECIAL_RESULT
	scrcmd_057 3
	scrcmd_058
	scrcmd_060 VAR_SPECIAL_RESULT
	callstd std_signpost
	end

scr_seq_R38_002:
	scrcmd_055 3, 0
	scrcmd_057 3
	scrcmd_058
	trainer_tips 16, VAR_SPECIAL_RESULT
	callstd std_signpost
	end
// hack: visible static Pokémon with daily respawn (hack/scripts/gen_static_mons.py)
scr_seq_R38_003:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	play_cry SPECIES_MIMIKYU, 0
	wait_cry
	setflag FLAG_ENGAGING_STATIC_POKEMON
	wild_battle SPECIES_MIMIKYU, 18, 0
	clearflag FLAG_ENGAGING_STATIC_POKEMON
	check_battle_won VAR_SPECIAL_RESULT
	compare VAR_SPECIAL_RESULT, 0
	goto_if_eq scr_seq_R38_003_lost
	setflag FLAG_UNK_B59
	hide_person obj_R38_hack_static
	releaseall
	end

scr_seq_R38_003_lost:
	white_out
	releaseall
	end
// hack: MAGNEZONE specialist (hack/scripts/gen_specialists.py)
scr_seq_R38_004:
	setvar VAR_SPECIAL_x8004, SPECIES_MAGNEZONE
	setvar VAR_SPECIAL_x8005, 30
	setvar VAR_SPECIAL_x8006, ITEM_SCOPE_LENS
	setvar VAR_SPECIAL_x8007, 2122
	callstd 2077
	end
// hack: TOXTRICITY specialist (hack/scripts/gen_specialists.py)
scr_seq_R38_005:
	setvar VAR_SPECIAL_x8004, SPECIES_TOXTRICITY
	setvar VAR_SPECIAL_x8005, 30
	setvar VAR_SPECIAL_x8006, ITEM_CHOICE_SPECS
	setvar VAR_SPECIAL_x8007, 2271
	callstd 2077
	end
// hack: SCOLIPEDE specialist (hack/scripts/gen_specialists.py)
scr_seq_R38_006:
	setvar VAR_SPECIAL_x8004, SPECIES_SCOLIPEDE
	setvar VAR_SPECIAL_x8005, 30
	setvar VAR_SPECIAL_x8006, ITEM_ROCKY_HELMET
	setvar VAR_SPECIAL_x8007, 2320
	callstd 2077
	end
// hack: BLISSEY specialist (hack/scripts/gen_specialists.py)
scr_seq_R38_007:
	setvar VAR_SPECIAL_x8004, SPECIES_BLISSEY
	setvar VAR_SPECIAL_x8005, 16
	setvar VAR_SPECIAL_x8006, ITEM_AIR_BALLOON
	setvar VAR_SPECIAL_x8007, 2353
	callstd 2077
	end
// hack: PORYGON_Z specialist (hack/scripts/gen_specialists.py)
scr_seq_R38_008:
	setvar VAR_SPECIAL_x8004, SPECIES_PORYGON_Z
	setvar VAR_SPECIAL_x8005, 16
	setvar VAR_SPECIAL_x8006, ITEM_LUM_BERRY
	setvar VAR_SPECIAL_x8007, 2359
	callstd 2077
	end
// hack: GRIMMSNARL specialist (hack/scripts/gen_specialists.py)
scr_seq_R38_009:
	setvar VAR_SPECIAL_x8004, SPECIES_GRIMMSNARL
	setvar VAR_SPECIAL_x8005, 42
	setvar VAR_SPECIAL_x8006, ITEM_BRIGHT_POWDER
	setvar VAR_SPECIAL_x8007, 2385
	callstd 2077
	end
	.balign 4
