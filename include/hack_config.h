#ifndef HACK_CONFIG_H
#define HACK_CONFIG_H

/*
 * Feature toggles for the HeartGold rom hack built on top of hg-engine.
 * Every hack-specific change in the C sources is wrapped in one of these defines
 * so it can be switched off (comment the line) without touching the engine code.
 */

// Kalos-style Exp. Share: a key item; when the player owns it and it is switched on,
// every healthy party member that did not battle gets 50% of the experience.
// The flag stores the OFF state so the Exp. Share starts switched ON when obtained.
#define HACK_KALOS_EXP_SHARE
#define FLAG_EXP_SHARE_DISABLED 2602
#define SCRIPT_EXP_SHARE_TOGGLE 2074 // common script scr_seq_0003_074_expshare
#define ITEM_FIELD_USE_EXP_SHARE 36  // NUM_VANILLA_FIELD_USE_FUNCS + index in sNewItemFieldUseFuncs

// Shiny Charm: extra shiny rolls for Pokémon created with the player's trainer id
// (wild encounters, gifts, Day Care eggs). Gen 5+ behaviour is 2 extra rolls.
#define HACK_SHINY_CHARM
#define SHINY_CHARM_EXTRA_ROLLS 2

// Oval Charm: better egg chance at the Day Care every 256 steps (20/50/70% become 40/80/88%).
#define HACK_OVAL_CHARM

// Starters: Dratini, Beldum and Larvitar instead of the Johto trio (src/starters.c).
// The rival's parties in data/Trainers.c and the texts are edited directly, not behind this define.
#define HACK_ALT_STARTERS

// "Add to party?" prompt after catching a Pokémon with a full party (src/hack_capture.c).
#define HACK_CAPTURE_PARTY_PROMPT
#define SCRIPT_CAPTURE_PROMPT 2076 // common script scr_seq_0003_076_capture_prompt
#define HACK_SCRCMD_CAPTURE_SWAP 0x4843 // value of the result var that turns day_care_sanitize_mon into the swap

// Species specialists ("mirror match"), see src/hack_mirror.c and hack/scripts/gen_specialists.py.
#define HACK_MIRROR_SPECIALISTS
#define SCRIPT_MIRROR_SPECIALIST 2077 // common script scr_seq_0003_077_mirror_specialist
#define HACK_TRAINER_MIRROR 738       // the generic specialist in data/Trainers.c
#define HACK_VAR_MIRROR_WINS 0x416F   // number of specialists beaten

// Bicycle with twice the vanilla top speed (2 frames per tile), see bytereplacement.
#define HACK_FAST_BIKE

// Bottle Cap / Gold Bottle Cap usable from the bag.
// Gold Bottle Cap: all IVs to 31. Bottle Cap: the lowest IV goes to 31.
#define HACK_BOTTLE_CAPS
#define MSG_PARTY_MENU_BOTTLE_CAP 226 // index of the new line in data/text/300.txt

#endif // HACK_CONFIG_H
