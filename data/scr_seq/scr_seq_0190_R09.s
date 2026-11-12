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

.include "data/scr_seq/include/event_R09.inc"


// text archive to grab from: 340.txt

.data


scrdef scr_seq_R09_000
scrdef scr_seq_R09_001
scrdef scr_seq_R09_002
scrdef scr_seq_R09_003
scrdef scr_seq_R09_004
scrdef scr_seq_R09_005
scrdef scr_seq_R09_006
scrdef_end

scr_seq_R09_000:
	direction_signpost 0, 1, 1, VAR_SPECIAL_RESULT
	scrcmd_057 3
	scrcmd_058
	scrcmd_060 VAR_SPECIAL_RESULT
	callstd std_signpost
	end
// hack: ALTARIA specialist (hack/scripts/gen_specialists.py)
scr_seq_R09_001:
	setvar VAR_SPECIAL_x8004, SPECIES_ALTARIA
	setvar VAR_SPECIAL_x8005, 35
	setvar VAR_SPECIAL_x8006, ITEM_ALTARIANITE
	setvar VAR_SPECIAL_x8007, 2298
	callstd 2077
	end
// hack: ZANGOOSE specialist (hack/scripts/gen_specialists.py)
scr_seq_R09_002:
	setvar VAR_SPECIAL_x8004, SPECIES_ZANGOOSE
	setvar VAR_SPECIAL_x8005, 18
	setvar VAR_SPECIAL_x8006, ITEM_SITRUS_BERRY
	setvar VAR_SPECIAL_x8007, 2299
	callstd 2077
	end
// hack: GRUMPIG specialist (hack/scripts/gen_specialists.py)
scr_seq_R09_003:
	setvar VAR_SPECIAL_x8004, SPECIES_GRUMPIG
	setvar VAR_SPECIAL_x8005, 32
	setvar VAR_SPECIAL_x8006, ITEM_AIR_BALLOON
	setvar VAR_SPECIAL_x8007, 2355
	callstd 2077
	end
// hack: VESPIQUEN specialist (hack/scripts/gen_specialists.py)
scr_seq_R09_004:
	setvar VAR_SPECIAL_x8004, SPECIES_VESPIQUEN
	setvar VAR_SPECIAL_x8005, 21
	setvar VAR_SPECIAL_x8006, ITEM_BOTTLE_CAP
	setvar VAR_SPECIAL_x8007, 2357
	callstd 2077
	end
// hack: MUDSDALE specialist (hack/scripts/gen_specialists.py)
scr_seq_R09_005:
	setvar VAR_SPECIAL_x8004, SPECIES_MUDSDALE
	setvar VAR_SPECIAL_x8005, 30
	setvar VAR_SPECIAL_x8006, ITEM_QUICK_CLAW
	setvar VAR_SPECIAL_x8007, 2365
	callstd 2077
	end
// hack: SHIINOTIC specialist (hack/scripts/gen_specialists.py)
scr_seq_R09_006:
	setvar VAR_SPECIAL_x8004, SPECIES_SHIINOTIC
	setvar VAR_SPECIAL_x8005, 24
	setvar VAR_SPECIAL_x8006, ITEM_PP_UP
	setvar VAR_SPECIAL_x8007, 2366
	callstd 2077
	end
	.balign 4
