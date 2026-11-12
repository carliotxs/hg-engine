#ifndef HACK_STORY_H
#define HACK_STORY_H

#include "config.h"
#include "types.h"

// story objects of the hack that come and go, see src/hack_story.c.
// flags 1340 to 1359 were unused in the original game (hack/README.md)
#define HACK_FLAG_HIDE_TOHJO_CAVE_BLOCK        1340
#define HACK_FLAG_HIDE_GIOVANNI                1341
#define HACK_FLAG_GIOVANNI_DONE                1342
#define HACK_FLAG_HIDE_MART_ROBBER_CHERRYGROVE 1343
#define HACK_FLAG_HIDE_MART_ROBBER_VIOLET      1344
#define HACK_FLAG_HIDE_MART_ROBBER_AZALEA      1345
#define HACK_FLAG_HIDE_VISITOR_WAKE            1346
#define HACK_DAILY_FLAG_VISITOR_WAKE           2881 // unused daily flag: Crasher Wake was battled today
#define HACK_DAILY_FLAG_MART_ROBBER            2880 // unused daily flag: the robber of the day was beaten

#define FLAG_BEAT_RADIO_TOWER_ROCKETS_ID 198 // FLAG_BEAT_RADIO_TOWER_ROCKETS in asm/include/flags.inc

#ifdef HACK_TEST
extern u8 gHackStoryTestDay;
extern u8 gHackStoryTestHour;
#endif

void LONG_CALL HackStory_Update(void);
void LONG_CALL HackStory_FieldTick(void);

#endif // HACK_STORY_H
