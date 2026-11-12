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

.include "data/scr_seq/include/event_R47.inc"


// text archive to grab from: 407.txt

.data


scrdef scr_seq_R47_000
scrdef scr_seq_R47_001
scrdef scr_seq_R47_002
scrdef scr_seq_R47_003
scrdef scr_seq_R47_004
scrdef scr_seq_R47_005
scrdef scr_seq_R47_006
scrdef scr_seq_R47_007
scrdef scr_seq_R47_008
scrdef scr_seq_R47_009
scrdef scr_seq_R47_010
scrdef scr_seq_R47_011
scrdef scr_seq_R47_012
scrdef_end

scr_seq_R47_000:
	setvar VAR_UNK_40EB, 1
	setflag FLAG_UNK_9C9
	get_game_version VAR_TEMP_x4000
	compare VAR_TEMP_x4000, 7
	goto_if_ne _004F
	move_warp 4, 87, 385
	move_warp 5, 87, 389
	move_warp 6, 87, 385
	goto _0067

_004F:
	move_warp 4, 87, 389
	move_warp 5, 87, 385
	move_warp 6, 87, 385
_0067:
	compare VAR_SCENE_EMBEDDED_TOWER, 2
	goto_if_eq _00E6
	compare VAR_SCENE_EMBEDDED_TOWER, 3
	goto_if_eq _00E6
	compare VAR_SCENE_EMBEDDED_TOWER, 5
	goto_if_ge _00EC
	goto_if_unset FLAG_UNK_189, _009F
	clearflag FLAG_UNK_189
	end

_009F:
	goto_if_set FLAG_GAME_CLEAR, _00B2
	goto _00E6

	.byte 0x02, 0x00
_00B2:
	get_phone_book_rematch PHONE_CONTACT_CHUCK, VAR_TEMP_x4001
	compare VAR_TEMP_x4001, 0
	goto_if_ne _00E6
	get_weekday VAR_TEMP_x4002
	compare VAR_TEMP_x4002, 0
	goto_if_ne _00E0
	clearflag FLAG_UNK_304
	goto _00E4

_00E0:
	setflag FLAG_UNK_304
_00E4:
	end

_00E6:
	setflag FLAG_UNK_304
	end

_00EC:
	move_warp 4, 87, 385
	move_warp 5, 87, 385
	move_warp 6, 87, 389
	goto _00E6

	.byte 0x02, 0x00
scr_seq_R47_002:
	compare VAR_SCENE_EMBEDDED_TOWER, 5
	goto_if_ge _0162
	get_game_version VAR_TEMP_x4000
	compare VAR_TEMP_x4000, 7
	goto_if_ne _0148
	move_warp 4, 87, 385
	move_warp 5, 87, 389
	move_warp 6, 87, 385
	goto _0160

_0148:
	move_warp 4, 87, 389
	move_warp 5, 87, 385
	move_warp 6, 87, 385
_0160:
	end

_0162:
	move_warp 4, 87, 385
	move_warp 5, 87, 385
	move_warp 6, 87, 389
	end

scr_seq_R47_001:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	goto_if_set FLAG_MET_ROUTE_47_EMBEDDED_TOWER_HIKER, _019E
	npc_msg 0
	wait_button
	closemsg
	setflag FLAG_MET_ROUTE_47_EMBEDDED_TOWER_HIKER
	releaseall
	end

_019E:
	npc_msg 1
	wait_button
	closemsg
	releaseall
	end

scr_seq_R47_003:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	goto_if_set FLAG_UNK_157, _0210
	npc_msg 2
	apply_movement obj_R47_leader3, _022C
	wait_movement
	npc_msg 3
	get_player_facing VAR_SPECIAL_RESULT
	compare VAR_SPECIAL_RESULT, 0
	goto_if_ne _01EB
	apply_movement obj_R47_leader3, _0234
	goto _020E

_01EB:
	compare VAR_SPECIAL_RESULT, 3
	goto_if_ne _0206
	apply_movement obj_R47_leader3, _023C
	goto _020E

_0206:
	apply_movement obj_R47_leader3, _0244
_020E:
	wait_movement
_0210:
	buffer_players_name 0
	npc_msg 4
	closemsg
	apply_movement obj_R47_leader3, _022C
	wait_movement
	setflag FLAG_UNK_157
	releaseall
	end

	.byte 0x00, 0x00
	.balign 4
_022C:

	step 32, 1
	step_end
	.balign 4
_0234:

	step 33, 1
	step_end
	.balign 4
_023C:

	step 34, 1
	step_end
	.balign 4
_0244:

	step 35, 1
	step_end
scr_seq_R47_004:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	npc_msg 5
	touchscreen_menu_hide
	getmenuchoice VAR_SPECIAL_RESULT
	touchscreen_menu_show
	compare VAR_SPECIAL_RESULT, 1
	goto_if_eq _02B5
	photo_album_is_full VAR_SPECIAL_RESULT
	compare VAR_SPECIAL_RESULT, 1
	goto_if_eq _02C0
	npc_msg 6
	closemsg
	setflag FLAG_UNK_189
	fade_screen 6, 1, 0, RGB_BLACK
	wait_fade
	cameron_photo 91
	faceplayer
	lockall
	fade_screen 6, 1, 1, RGB_BLACK
	wait_fade
	clearflag FLAG_UNK_189
	npc_msg 7
	wait_button
	closemsg
	releaseall
	end

_02B5:
	npc_msg 8
	wait_button
	closemsg
	releaseall
	end

_02C0:
	npc_msg 9
	wait_button
	closemsg
	releaseall
	end
// hack: visible static Pokémon with daily respawn (hack/scripts/gen_static_mons.py)
scr_seq_R47_005:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	play_cry SPECIES_DRAMPA, 0
	wait_cry
	setflag FLAG_ENGAGING_STATIC_POKEMON
	wild_battle SPECIES_DRAMPA, 32, 0
	clearflag FLAG_ENGAGING_STATIC_POKEMON
	check_battle_won VAR_SPECIAL_RESULT
	compare VAR_SPECIAL_RESULT, 0
	goto_if_eq scr_seq_R47_005_lost
	setflag FLAG_UNK_B5D
	hide_person obj_R47_hack_static
	releaseall
	end

scr_seq_R47_005_lost:
	white_out
	releaseall
	end
// hack: MILTANK specialist (hack/scripts/gen_specialists.py)
scr_seq_R47_006:
	setvar VAR_SPECIAL_x8004, SPECIES_MILTANK
	setvar VAR_SPECIAL_x8005, 38
	setvar VAR_SPECIAL_x8006, ITEM_KINGS_ROCK
	setvar VAR_SPECIAL_x8007, 2583
	callstd 2077
	end
// hack: THROH specialist (hack/scripts/gen_specialists.py)
scr_seq_R47_007:
	setvar VAR_SPECIAL_x8004, SPECIES_THROH
	setvar VAR_SPECIAL_x8005, 34
	setvar VAR_SPECIAL_x8006, ITEM_LEFTOVERS
	setvar VAR_SPECIAL_x8007, 2584
	callstd 2077
	end
// hack: SAWK specialist (hack/scripts/gen_specialists.py)
scr_seq_R47_008:
	setvar VAR_SPECIAL_x8004, SPECIES_SAWK
	setvar VAR_SPECIAL_x8005, 37
	setvar VAR_SPECIAL_x8006, ITEM_LIFE_ORB
	setvar VAR_SPECIAL_x8007, 2585
	callstd 2077
	end
// hack: BOUFFALANT specialist (hack/scripts/gen_specialists.py)
scr_seq_R47_009:
	setvar VAR_SPECIAL_x8004, SPECIES_BOUFFALANT
	setvar VAR_SPECIAL_x8005, 34
	setvar VAR_SPECIAL_x8006, ITEM_CHOICE_SCARF
	setvar VAR_SPECIAL_x8007, 2586
	callstd 2077
	end
// hack: ORANGURU specialist (hack/scripts/gen_specialists.py)
scr_seq_R47_010:
	setvar VAR_SPECIAL_x8004, SPECIES_ORANGURU
	setvar VAR_SPECIAL_x8005, 34
	setvar VAR_SPECIAL_x8006, ITEM_CHOICE_SPECS
	setvar VAR_SPECIAL_x8007, 2587
	callstd 2077
	end
// hack: FARFETCHD specialist (hack/scripts/gen_specialists.py)
scr_seq_R47_011:
	setvar VAR_SPECIAL_x8004, SPECIES_FARFETCHD
	setvar VAR_SPECIAL_x8005, 38
	setvar VAR_SPECIAL_x8006, ITEM_SITRUS_BERRY
	setvar VAR_SPECIAL_x8007, 2588
	callstd 2077
	end
// hack: MAUSHOLD specialist (hack/scripts/gen_specialists.py)
scr_seq_R47_012:
	setvar VAR_SPECIAL_x8004, SPECIES_MAUSHOLD
	setvar VAR_SPECIAL_x8005, 34
	setvar VAR_SPECIAL_x8006, ITEM_RARE_CANDY
	setvar VAR_SPECIAL_x8007, 2232
	callstd 2077
	end
	.balign 4
