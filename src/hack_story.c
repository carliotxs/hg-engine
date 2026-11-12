#include "../include/config.h"
#include "../include/types.h"

#ifdef HACK_STORY_RULES

/*
 * "Who is on the map when": objects that the hack adds to the story are shown or hidden by ordinary
 * hide flags, and this file keeps those flags up to date from simple rules (a story flag that must
 * be set, a flag that marks the event as done, a day of the week).  Hide flags are read when a map
 * loads, so refreshing them from the overworld tick is enough: no map load script has to be edited.
 *
 * The rules are in the table below; hack/README.md lists the flags.
 */

#include "../include/hack_story.h"
#include "../include/rtc.h"
#include "../include/save.h"

#define ANY_DAY 0xFF
#define DAYS(a, b) ((1 << (a)) | (1 << (b)))

struct HackStoryRule {
    u16 hideFlag; // the object's hidden_flag in the map data
    u16 needFlag; // 0, or a flag that must be set for the object to exist
    u16 doneFlag; // 0, or a flag that removes the object once set
    u8 days;      // ANY_DAY, or a bit mask of RTC_WEEK_* days on which the object exists
    u8 hourFrom;  // the object exists from this hour...
    u8 hourTo;    // ...up to, but not including, this one (0 and 24 for the whole day)
    u8 inverted;  // TRUE: the object exists when the conditions are NOT met (used for obstacles)
};

static const struct HackStoryRule sHackStoryRules[] = {
    // Tohjo Falls: the invisible obstacle in front of the hidden cave goes away after the Radio Tower
    { HACK_FLAG_HIDE_TOHJO_CAVE_BLOCK, FLAG_BEAT_RADIO_TOWER_ROCKETS_ID, 0, ANY_DAY, 0, 24, TRUE },
    // Giovanni waits in that cave until he is beaten
    { HACK_FLAG_HIDE_GIOVANNI, FLAG_BEAT_RADIO_TOWER_ROCKETS_ID, HACK_FLAG_GIOVANNI_DONE, ANY_DAY, 0, 24, FALSE },
    // random events: a Team Rocket grunt robs a different Poké Mart depending on the day, once a day
    { HACK_FLAG_HIDE_MART_ROBBER_CHERRYGROVE, 0, HACK_DAILY_FLAG_MART_ROBBER, DAYS(RTC_WEEK_MONDAY, RTC_WEEK_THURSDAY), 0, 24, FALSE },
    { HACK_FLAG_HIDE_MART_ROBBER_VIOLET, 0, HACK_DAILY_FLAG_MART_ROBBER, DAYS(RTC_WEEK_TUESDAY, RTC_WEEK_FRIDAY), 0, 24, FALSE },
    // famous visitors: Crasher Wake trains at the Lake of Rage on Saturdays, from 10:00 to 20:00, one battle a day
    { HACK_FLAG_HIDE_VISITOR_WAKE, 0, HACK_DAILY_FLAG_VISITOR_WAKE, 1 << RTC_WEEK_SATURDAY, 10, 20, FALSE },
    { HACK_FLAG_HIDE_MART_ROBBER_AZALEA, 0, HACK_DAILY_FLAG_MART_ROBBER, DAYS(RTC_WEEK_WEDNESDAY, RTC_WEEK_SATURDAY), 0, 24, FALSE },
};

static u8 sHackStoryCountdown = 0;

#ifdef HACK_TEST
u8 gHackStoryTestDay = 0xFF; // debug ROM: a chapter can pretend it is a given day of the week
u8 gHackStoryTestHour = 0xFF; // and a given hour
#endif

/**
 *  @brief apply every rule now
 */
void LONG_CALL HackStory_Update(void)
{
    struct RTCDate date;
    struct RTCTime time;
    GF_RTC_CopyDateTime(&date, &time);
#ifdef HACK_TEST
    if (gHackStoryTestDay != 0xFF) {
        date.week = gHackStoryTestDay;
    }
    if (gHackStoryTestHour != 0xFF) {
        time.hour = gHackStoryTestHour;
    }
#endif

    for (u32 i = 0; i < NELEMS(sHackStoryRules); i++) {
        const struct HackStoryRule *rule = &sHackStoryRules[i];
        BOOL exists = (rule->needFlag == 0 || CheckScriptFlag(rule->needFlag))
            && (rule->doneFlag == 0 || !CheckScriptFlag(rule->doneFlag))
            && (rule->days == ANY_DAY || (rule->days & (1 << date.week)))
            && time.hour >= rule->hourFrom && time.hour < rule->hourTo;
        if (rule->inverted) {
            exists = !exists;
        }
        if (exists) {
            ClearScriptFlag(rule->hideFlag);
        } else {
            SetScriptFlag(rule->hideFlag);
        }
    }
}

/**
 *  @brief called once per frame in the overworld: refresh the rules about twice a second
 */
void LONG_CALL HackStory_FieldTick(void)
{
    if (sHackStoryCountdown != 0) {
        sHackStoryCountdown--;
        return;
    }
    sHackStoryCountdown = 30;
    HackStory_Update();
}

#endif // HACK_STORY_RULES
