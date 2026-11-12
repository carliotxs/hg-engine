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

.include "data/scr_seq/include/event_D26R0103.inc"


// text archive to grab from: 092.txt

.data


scrdef scr_seq_D26R0103_000
scrdef scr_seq_D26R0103_001
scrdef scr_seq_D26R0103_002
scrdef scr_seq_D26R0103_003
scrdef scr_seq_D26R0103_004
scrdef_end

scr_seq_D26R0103_000:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	goto_if_set FLAG_GOT_KINGS_ROCK_FROM_SLOWPOKE_WELL_MAN, _004F
	npc_msg 0
	wait_ab_press
	closemsg
	goto_if_no_item_space ITEM_KINGS_ROCK, 1, _005A
	callstd std_give_item_verbose
	setflag FLAG_GOT_KINGS_ROCK_FROM_SLOWPOKE_WELL_MAN
	goto _004F

_004F:
	npc_msg 2
	wait_button
	closemsg
	releaseall
	end

_005A:
	callstd std_bag_is_full
	closemsg
	releaseall
	end

	.byte 0x02, 0x00, 0x00, 0x00
// hack: SLOWKING specialist (hack/scripts/gen_specialists.py)
scr_seq_D26R0103_001:
	setvar VAR_SPECIAL_x8004, SPECIES_SLOWKING
	setvar VAR_SPECIAL_x8005, 28
	setvar VAR_SPECIAL_x8006, ITEM_CHOICE_SPECS
	setvar VAR_SPECIAL_x8007, 2199
	callstd 2077
	end
// hack: CARBINK specialist (hack/scripts/gen_specialists.py)
scr_seq_D26R0103_002:
	setvar VAR_SPECIAL_x8004, SPECIES_CARBINK
	setvar VAR_SPECIAL_x8005, 22
	setvar VAR_SPECIAL_x8006, ITEM_ABILITY_CAPSULE
	setvar VAR_SPECIAL_x8007, 2333
	callstd 2077
	end
// hack: BRONZONG specialist (hack/scripts/gen_specialists.py)
scr_seq_D26R0103_003:
	setvar VAR_SPECIAL_x8004, SPECIES_BRONZONG
	setvar VAR_SPECIAL_x8005, 33
	setvar VAR_SPECIAL_x8006, ITEM_KINGS_ROCK
	setvar VAR_SPECIAL_x8007, 2615
	callstd 2077
	end
// hack: DELPHOX specialist (hack/scripts/gen_specialists.py)
scr_seq_D26R0103_004:
	setvar VAR_SPECIAL_x8004, SPECIES_DELPHOX
	setvar VAR_SPECIAL_x8005, 36
	setvar VAR_SPECIAL_x8006, ITEM_DELPHOXITE
	setvar VAR_SPECIAL_x8007, 2649
	callstd 2077
	end
	.balign 4
