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

// Level cap derived from the number of badges (see sBadgeLevelCaps in src/pokemon.c).
// A non-zero value in LEVEL_CAP_VARIABLE still overrides the table from scripts.
#define HACK_BADGE_LEVEL_CAPS

// Shiny Charm: extra shiny rolls for Pokémon created with the player's trainer id
// (wild encounters, gifts, Day Care eggs). Gen 5+ behaviour is 2 extra rolls.
#define HACK_SHINY_CHARM
#define SHINY_CHARM_EXTRA_ROLLS 2

// Oval Charm: better egg chance at the Day Care every 256 steps (20/50/70% become 40/80/88%).
#define HACK_OVAL_CHARM

// Bottle Cap / Gold Bottle Cap usable from the bag.
// Gold Bottle Cap: all IVs to 31. Bottle Cap: the lowest IV goes to 31.
#define HACK_BOTTLE_CAPS
#define MSG_PARTY_MENU_BOTTLE_CAP 226 // index of the new line in data/text/300.txt

#endif // HACK_CONFIG_H
