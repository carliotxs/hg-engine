#ifndef HACK_TEST_H
#define HACK_TEST_H

// scenarios of the automated in-game tests (make HACK_TEST=Y), see src/hack_test.c
// and hack/scripts/ingame_tests.py
#define HACK_TEST_EXP_SHARE_ON     1 // wild battle, Exp. Share on
#define HACK_TEST_EXP_SHARE_OFF    2 // wild battle, Exp. Share switched off
#define HACK_TEST_NO_LEVEL_CAP     3 // wild battle with 0 badges: nobody is capped
#define HACK_TEST_SHOP             4 // Goldenrod Dept. Store 4F shop
#define HACK_TEST_BOTTLE_CAPS      5 // no script, the bag is used from the menu
#define HACK_TEST_EXP_SHARE_TOGGLE 6 // no script, the Exp. Share is used from the bag
#define HACK_TEST_EXP_SHARE_SWITCH 7 // wild battle, two mons fight
#define HACK_TEST_SWITCH_NO_SHARE   8 // same with the Exp. Share switched off
#define HACK_TEST_SHINY_CHARM       9 // no script, generates many mons and counts the shiny ones
#define HACK_TEST_DAY_CARE         10 // no script, runs the Day Care egg roll many times
#define HACK_TEST_BIKE             11 // no script, the Bicycle is used from the bag and ridden
#define HACK_TEST_CAPTURE_PROMPT   13 // wild battle with a full party and Master Balls
#define HACK_TEST_CAPTURE_PROMPT_NO 14 // same, answering no to the prompt
#define HACK_TEST_CAPTURE_PROMPT_MAIL 15 // same, the first party member holds Mail
#define HACK_TEST_MIRROR           16 // the Mantine specialist of Cherrygrove City, with a Mantine in the party
#define HACK_TEST_MIRROR_NO_MON    17 // the same specialist without a Mantine
#define HACK_TEST_LEADER           18 // trainer battle against Falkner
#define HACK_TEST_STATIC_MON       12 // no script, the visible static Pokémon of Cherrygrove City

#ifndef __ASSEMBLER__
void HackTest_FieldTick(void);
#endif

#endif // HACK_TEST_H
