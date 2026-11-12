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

.include "data/scr_seq/include/event_R43.inc"


// text archive to grab from: 401.txt

.data


scrdef scr_seq_R43_000
scrdef scr_seq_R43_001
scrdef scr_seq_R43_002
scrdef scr_seq_R43_003
scrdef scr_seq_R43_004
scrdef scr_seq_R43_005
scrdef scr_seq_R43_006
scrdef scr_seq_R43_007
scrdef scr_seq_R43_008
scrdef scr_seq_R43_009
scrdef_end

scr_seq_R43_000:
	end

scr_seq_R43_001:
	direction_signpost 18, 1, 3, VAR_SPECIAL_RESULT
	scrcmd_057 3
	scrcmd_058
	scrcmd_060 VAR_SPECIAL_RESULT
	callstd std_signpost
	end

scr_seq_R43_002:
	scrcmd_055 3, 0
	scrcmd_057 3
	scrcmd_058
	trainer_tips 19, VAR_SPECIAL_RESULT
	callstd std_signpost
	end

scr_seq_R43_003:
	direction_signpost 20, 1, 6, VAR_SPECIAL_RESULT
	scrcmd_057 3
	scrcmd_058
	scrcmd_060 VAR_SPECIAL_RESULT
	callstd std_signpost
	end
// hack: CARNIVINE specialist (hack/scripts/gen_specialists.py)
scr_seq_R43_004:
	setvar VAR_SPECIAL_x8004, SPECIES_CARNIVINE
	setvar VAR_SPECIAL_x8005, 18
	setvar VAR_SPECIAL_x8006, ITEM_ROCKY_HELMET
	setvar VAR_SPECIAL_x8007, 2577
	callstd 2077
	end
// hack: QUAQUAVAL specialist (hack/scripts/gen_specialists.py)
scr_seq_R43_005:
	setvar VAR_SPECIAL_x8004, SPECIES_QUAQUAVAL
	setvar VAR_SPECIAL_x8005, 36
	setvar VAR_SPECIAL_x8006, ITEM_MUSCLE_BAND
	setvar VAR_SPECIAL_x8007, 2274
	callstd 2077
	end
// hack: INTELEON specialist (hack/scripts/gen_specialists.py)
scr_seq_R43_006:
	setvar VAR_SPECIAL_x8004, SPECIES_INTELEON
	setvar VAR_SPECIAL_x8005, 35
	setvar VAR_SPECIAL_x8006, ITEM_LEFTOVERS
	setvar VAR_SPECIAL_x8007, 2340
	callstd 2077
	end
// hack: DUSKNOIR specialist (hack/scripts/gen_specialists.py)
scr_seq_R43_007:
	setvar VAR_SPECIAL_x8004, SPECIES_DUSKNOIR
	setvar VAR_SPECIAL_x8005, 37
	setvar VAR_SPECIAL_x8006, ITEM_LIFE_ORB
	setvar VAR_SPECIAL_x8007, 2378
	callstd 2077
	end
// hack: GOODRA specialist (hack/scripts/gen_specialists.py)
scr_seq_R43_008:
	setvar VAR_SPECIAL_x8004, SPECIES_GOODRA
	setvar VAR_SPECIAL_x8005, 50
	setvar VAR_SPECIAL_x8006, ITEM_LEFTOVERS
	setvar VAR_SPECIAL_x8007, 2634
	callstd 2077
	end
// hack: extra Team Rocket grunt, Route 43, until the Mahogany hideout is cleared (hack/scripts/gen_rocket.py)
scr_seq_R43_009:
	setvar VAR_SPECIAL_x8007, 2595
	callstd 2078
	compare VAR_SPECIAL_RESULT, 0
	goto_if_eq scr_seq_R43_009_end
	trainer_battle TRAINER_HACK_739, 0, 0, 0
	check_battle_won VAR_SPECIAL_RESULT
	compare VAR_SPECIAL_RESULT, 0
	goto_if_eq scr_seq_R43_009_lost
	setflag 2595
	callstd 2079
scr_seq_R43_009_end:
	releaseall
	end

scr_seq_R43_009_lost:
	white_out
	releaseall
	end
	.balign 4
