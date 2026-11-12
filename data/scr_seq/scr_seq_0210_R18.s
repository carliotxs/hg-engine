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

.include "data/scr_seq/include/event_R18.inc"


// text archive to grab from: 358.txt

.data


scrdef scr_seq_R18_000
scrdef scr_seq_R18_001
scrdef scr_seq_R18_002
scrdef scr_seq_R18_003
scrdef scr_seq_R18_004
scrdef scr_seq_R18_005
scrdef scr_seq_R18_006
scrdef scr_seq_R18_007
scrdef scr_seq_R18_008
scrdef_end

scr_seq_R18_000:
	goto_if_set FLAG_UNK_149, _0017
	end

_0017:
	scrcmd_186 1
	end

scr_seq_R18_001:
	direction_signpost 0, 1, 1, VAR_SPECIAL_RESULT
	scrcmd_057 3
	scrcmd_058
	scrcmd_060 VAR_SPECIAL_RESULT
	callstd std_signpost
	end
// hack: WHIMSICOTT specialist (hack/scripts/gen_specialists.py)
scr_seq_R18_002:
	setvar VAR_SPECIAL_x8004, SPECIES_WHIMSICOTT
	setvar VAR_SPECIAL_x8005, 31
	setvar VAR_SPECIAL_x8006, ITEM_WEAKNESS_POLICY
	setvar VAR_SPECIAL_x8007, 2214
	callstd 2077
	end
// hack: MUK specialist (hack/scripts/gen_specialists.py)
scr_seq_R18_003:
	setvar VAR_SPECIAL_x8004, SPECIES_MUK
	setvar VAR_SPECIAL_x8005, 38
	setvar VAR_SPECIAL_x8006, ITEM_FOCUS_SASH
	setvar VAR_SPECIAL_x8007, 2239
	callstd 2077
	end
// hack: SWALOT specialist (hack/scripts/gen_specialists.py)
scr_seq_R18_004:
	setvar VAR_SPECIAL_x8004, SPECIES_SWALOT
	setvar VAR_SPECIAL_x8005, 32
	setvar VAR_SPECIAL_x8006, ITEM_WEAKNESS_POLICY
	setvar VAR_SPECIAL_x8007, 2297
	callstd 2077
	end
// hack: LEAVANNY specialist (hack/scripts/gen_specialists.py)
scr_seq_R18_005:
	setvar VAR_SPECIAL_x8004, SPECIES_LEAVANNY
	setvar VAR_SPECIAL_x8005, 31
	setvar VAR_SPECIAL_x8006, ITEM_CHOICE_SCARF
	setvar VAR_SPECIAL_x8007, 2319
	callstd 2077
	end
// hack: CASTFORM specialist (hack/scripts/gen_specialists.py)
scr_seq_R18_006:
	setvar VAR_SPECIAL_x8004, SPECIES_CASTFORM
	setvar VAR_SPECIAL_x8005, 30
	setvar VAR_SPECIAL_x8006, ITEM_BRIGHT_POWDER
	setvar VAR_SPECIAL_x8007, 2372
	callstd 2077
	end
// hack: JOLTEON specialist (hack/scripts/gen_specialists.py)
scr_seq_R18_007:
	setvar VAR_SPECIAL_x8004, SPECIES_JOLTEON
	setvar VAR_SPECIAL_x8005, 33
	setvar VAR_SPECIAL_x8006, ITEM_RARE_CANDY
	setvar VAR_SPECIAL_x8007, 2388
	callstd 2077
	end
// hack: PURUGLY specialist (hack/scripts/gen_specialists.py)
scr_seq_R18_008:
	setvar VAR_SPECIAL_x8004, SPECIES_PURUGLY
	setvar VAR_SPECIAL_x8005, 38
	setvar VAR_SPECIAL_x8006, ITEM_MUSCLE_BAND
	setvar VAR_SPECIAL_x8007, 2399
	callstd 2077
	end
	.balign 4
