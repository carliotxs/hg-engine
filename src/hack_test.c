#include "../include/config.h"
#include "../include/debug.h"
#include "../include/types.h"

#ifdef HACK_TEST

/*
 * Automated in-game tests for the hack (built only with `make HACK_TEST=Y`, never in release ROMs).
 *
 * hack/scripts/ingame_tests.py boots the ROM with a save, writes 0xC0DE0000 | scenario into the
 * emulator communication address and this file then:
 *   1. builds a known party / bag / badge state for that scenario
 *   2. queues common script 2073 (wild battle) or 2075 (Goldenrod 4F shop) when the scenario needs one
 *   3. keeps a plain (unencrypted) report of the state in gHackTestReport, whose address is written
 *      back to the communication address so that the python side can read the results.
 */

#include "../include/bag.h"
#include "../include/constants/file.h"
#include "../include/constants/item.h"
#include "../include/constants/moves.h"
#include "../include/constants/species.h"
#include "../include/hack_test.h"
#include "../include/pokemon.h"
#include "../include/save.h"
#include "../include/script.h"

#define HACK_TEST_HOLE ((volatile u32 *)0x02FFF81C)
#define HACK_TEST_REQUEST_MAGIC 0xC0DE
#define HACK_TEST_STATIC_MON_FLAG 2910 // daily flag of the static Pokémon of Cherrygrove City

struct HackTestMonReport {
    u16 species;
    u8 level;
    u8 isEgg;
    u32 exp;
    u16 hp;
    u8 ivs[6];
};

struct HackTestReport {
    u32 magic; // "HKTS"
    u32 ticks;
    u16 scenario;
    u8 partyCount;
    u8 levelCap;
    u32 money;
    u8 badges;
    u8 expShareOwned;
    u8 expShareDisabledFlag;
    u8 padding;
    u16 bottleCaps;
    u16 goldBottleCaps;
    u16 mints; // adamant mints, bought in the shop scenario
    u16 padding2;
    struct HackTestMonReport mons[6];
    // shiny charm scenario: 0 = wild mons without the charm, 1 = wild mons with it, 2 = gift mons with it
    u32 shinyTotal[3];
    u32 shinyHits[3];
    // day care scenario: 0 = no charms, 1 = Oval Charm and Shiny Charm
    u32 eggRolls[2];
    u32 eggs[2];
    u32 shinyEggs[2];
    s16 playerX;
    s16 playerZ;
};

u32 LONG_CALL PlayerAvatar_GetXCoord(FIELD_PLAYER_AVATAR *playerAvatar);
u32 LONG_CALL PlayerAvatar_GetZCoord(FIELD_PLAYER_AVATAR *playerAvatar);

#define DAYCARE_MON_SIZE             0xEC
#define DAYCARE_STEPS_OFFSET         0xE8
#define DAYCARE_EGG_PID_OFFSET       0x1D8
#define DAYCARE_EGG_CYCLES_OFFSET    0x1DC
#define HACK_TEST_EGG_ROLLS          1000
#define HACK_TEST_EGG_ROLLS_PER_TICK 25

u32 LONG_CALL Daycare_CalcCompatibilityInternal(struct BoxPokemon **parents);
u16 LONG_CALL HackCapture_TestStoredSpecies(void);
BOOL LONG_CALL HandleDaycareStep(Daycare *daycare, struct Party *party, FieldSystem *fieldSystem);

// creating a mon is slow (it reads the learnsets), so HACK_TEST builds raise SHINY_ODDS in config.h
#define HACK_TEST_SHINY_SAMPLES   1500
#define HACK_TEST_SHINY_PER_TICK  10

struct HackTestReport ALIGN4 gHackTestReport = { .magic = 0x53544B48 };
static u32 sHackTestWait = 0;
static u8 sHackTestStarted = FALSE;

static struct PartyPokemon *HackTest_AddMon(u16 species, u8 level)
{
    void *save = SaveBlock2_get();
    struct Party *party = SaveData_GetPlayerPartyPtr(save);
    GiveMon(HEAPID_WORLD, save, species, level, 0, 0, 0, 0, 0);
    return Party_GetMonByIndex(party, party->count - 1);
}

static void HackTest_SetMove(struct PartyPokemon *pp, u16 move, u8 pp_count)
{
    u32 value = move;
    SetMonData(pp, MON_DATA_MOVE1, &value);
    value = pp_count;
    SetMonData(pp, MON_DATA_MOVE1PP, &value);
}

static void HackTest_SetIVs(struct PartyPokemon *pp, const u8 *ivs)
{
    for (u32 i = 0; i < 6; i++) {
        u32 value = ivs[i];
        SetMonData(pp, MON_DATA_HP_IV + i, &value);
    }
    RecalcPartyPokemonStats(pp);
}

static void HackTest_Setup(u16 scenario)
{
    void *save = SaveBlock2_get();
    struct Party *party = SaveData_GetPlayerPartyPtr(save);
    struct PlayerProfile *profile = Sav2_PlayerData_GetProfileAddr(save);
    BAG_DATA *bag = Sav2_Bag_get(save);
    struct PartyPokemon *pp;
    u32 value;

    PokeParty_Init(party, 6);
    for (u32 i = 0; i < NUM_BAG_ITEMS; i++) {
        bag->items[i].id = 0;
        bag->items[i].quantity = 0;
    }
    for (u32 i = 0; i < NUM_BAG_KEY_ITEMS; i++) {
        bag->keyItems[i].id = 0;
        bag->keyItems[i].quantity = 0;
    }
    bag->keyItems[0].id = ITEM_EXP_SHARE;
    bag->keyItems[0].quantity = 1;
    ClearScriptFlag(FLAG_EXP_SHARE_DISABLED);
    profile->johtoBadges = 0xFF;
    profile->kantoBadges = 0;
    profile->money = 500000;

    switch (scenario) {
    case HACK_TEST_EXP_SHARE_OFF:
        SetScriptFlag(FLAG_EXP_SHARE_DISABLED);
        FALLTHROUGH;
    case HACK_TEST_EXP_SHARE_ON:
        // 8 badges: cap 50. fighter, two benched mons and a fainted one
        pp = HackTest_AddMon(SPECIES_GARCHOMP, 40);
        HackTest_SetMove(pp, MOVE_EARTHQUAKE, 10);
        HackTest_AddMon(SPECIES_PIDGEY, 20);
        HackTest_AddMon(SPECIES_RATTATA, 10);
        pp = HackTest_AddMon(SPECIES_ZUBAT, 15);
        value = 0;
        SetMonData(pp, MON_DATA_HP, &value);
        break;

    case HACK_TEST_SWITCH_NO_SHARE:
        SetScriptFlag(FLAG_EXP_SHARE_DISABLED);
        FALLTHROUGH;
    case HACK_TEST_EXP_SHARE_SWITCH:
        // the lead uses Baton Pass, so two mons take part in the battle and split the experience
        pp = HackTest_AddMon(SPECIES_GARCHOMP, 40);
        HackTest_SetMove(pp, MOVE_BATON_PASS, 40);
        pp = HackTest_AddMon(SPECIES_GARCHOMP, 40);
        HackTest_SetMove(pp, MOVE_EARTHQUAKE, 10);
        HackTest_AddMon(SPECIES_RATTATA, 10);
        break;

    case HACK_TEST_NO_LEVEL_CAP:
        // 0 badges and low levels: there is no level cap, so everybody gains experience and can level up
        profile->johtoBadges = 0;
        pp = HackTest_AddMon(SPECIES_GARCHOMP, 13);
        HackTest_SetMove(pp, MOVE_EARTHQUAKE, 10);
        pp = HackTest_AddMon(SPECIES_MAGIKARP, 12);
        value = PokeLevelExpGet(SPECIES_MAGIKARP, 13) - 1;
        SetMonData(pp, MON_DATA_EXPERIENCE, &value);
        HackTest_AddMon(SPECIES_MAGIKARP, 5);
        break;

    case HACK_TEST_SHOP:
        HackTest_AddMon(SPECIES_GARCHOMP, 40);
        break;

    case HACK_TEST_CAPTURE_PROMPT:
    case HACK_TEST_CAPTURE_PROMPT_NO:
        // full party: the caught Rattata goes to the PC and the prompt offers to swap it in
        pp = HackTest_AddMon(SPECIES_GARCHOMP, 40);
        HackTest_SetMove(pp, MOVE_EARTHQUAKE, 10);
        HackTest_AddMon(SPECIES_PIDGEY, 20);
        HackTest_AddMon(SPECIES_MAGIKARP, 10);
        HackTest_AddMon(SPECIES_ZUBAT, 15);
        HackTest_AddMon(SPECIES_GEODUDE, 12);
        HackTest_AddMon(SPECIES_ODDISH, 11);
        for (u32 i = 0; i < NUM_BAG_BALLS; i++) {
            bag->balls[i].id = 0;
            bag->balls[i].quantity = 0;
        }
        bag->balls[0].id = ITEM_MASTER_BALL;
        bag->balls[0].quantity = 5;
        break;

    case HACK_TEST_STATIC_MON:
        pp = HackTest_AddMon(SPECIES_GARCHOMP, 40);
        HackTest_SetMove(pp, MOVE_EARTHQUAKE, 10);
        ClearScriptFlag(HACK_TEST_STATIC_MON_FLAG);
        break;

    case HACK_TEST_BIKE:
        HackTest_AddMon(SPECIES_GARCHOMP, 40);
        bag->keyItems[1].id = ITEM_BIKE;
        bag->keyItems[1].quantity = 1;
        break;

    case HACK_TEST_BOTTLE_CAPS: {
        static const u8 mixed[6] = { 5, 10, 31, 20, 31, 31 };
        static const u8 zero[6] = { 0, 0, 0, 0, 0, 0 };
        pp = HackTest_AddMon(SPECIES_GARCHOMP, 50);
        HackTest_SetIVs(pp, mixed);
        pp = HackTest_AddMon(SPECIES_PIDGEOT, 50);
        HackTest_SetIVs(pp, mixed);
        pp = HackTest_AddMon(SPECIES_RATICATE, 49);
        HackTest_SetIVs(pp, zero);
        bag->items[0].id = ITEM_BOTTLE_CAP;
        bag->items[0].quantity = 3;
        bag->items[1].id = ITEM_GOLD_BOTTLE_CAP;
        bag->items[1].quantity = 3;
        break;
    }

    default: // HACK_TEST_EXP_SHARE_TOGGLE and anything else: just a party
        HackTest_AddMon(SPECIES_GARCHOMP, 40);
        break;
    }
}

static void HackTest_UpdateReport(void)
{
    void *save = SaveBlock2_get();
    struct Party *party = SaveData_GetPlayerPartyPtr(save);
    struct PlayerProfile *profile = Sav2_PlayerData_GetProfileAddr(save);
    BAG_DATA *bag = Sav2_Bag_get(save);
    struct HackTestReport *report = &gHackTestReport;

    report->ticks++;
    report->playerX = PlayerAvatar_GetXCoord(gFieldSysPtr->playerAvatar);
    report->playerZ = PlayerAvatar_GetZCoord(gFieldSysPtr->playerAvatar);
    report->partyCount = party->count;
    report->levelCap = GetLevelCap();
    report->money = profile->money;
    report->badges = 0;
    for (s32 i = 0; i < 16; i++) {
        if (PlayerProfile_TestBadgeFlag(profile, i) == TRUE) {
            report->badges++;
        }
    }
    report->expShareOwned = PlayerHasKeyItem(ITEM_EXP_SHARE);
    report->expShareDisabledFlag = CheckScriptFlag(FLAG_EXP_SHARE_DISABLED);
    report->padding = CheckScriptFlag(HACK_TEST_STATIC_MON_FLAG);
    if (report->scenario == HACK_TEST_CAPTURE_PROMPT || report->scenario == HACK_TEST_CAPTURE_PROMPT_NO) {
        report->padding2 = HackCapture_TestStoredSpecies(); // reuses the debug field of the day care scenario
    }
    report->bottleCaps = Bag_GetQuantity(bag, ITEM_BOTTLE_CAP, HEAPID_WORLD);
    report->goldBottleCaps = Bag_GetQuantity(bag, ITEM_GOLD_BOTTLE_CAP, HEAPID_WORLD);
    report->mints = Bag_GetQuantity(bag, ITEM_ADAMANT_MINT, HEAPID_WORLD);
    for (s32 i = 0; i < 6; i++) {
        struct HackTestMonReport *mon = &report->mons[i];
        if (i >= party->count) {
            mon->species = 0;
            continue;
        }
        struct PartyPokemon *pp = Party_GetMonByIndex(party, i);
        mon->species = GetMonData(pp, MON_DATA_SPECIES, NULL);
        mon->level = GetMonData(pp, MON_DATA_LEVEL, NULL);
        mon->isEgg = GetMonData(pp, MON_DATA_IS_EGG, NULL);
        mon->exp = GetMonData(pp, MON_DATA_EXPERIENCE, NULL);
        mon->hp = GetMonData(pp, MON_DATA_HP, NULL);
        for (u32 stat = 0; stat < 6; stat++) {
            mon->ivs[stat] = GetMonData(pp, MON_DATA_HP_IV + stat, NULL);
        }
    }
}

/**
 *  @brief generate a batch of mons the way wild encounters (phases 0 and 1) and gifts (phase 2) do
 *         and count the shiny ones.  the Shiny Charm is added to the bag after phase 0
 */
static void HackTest_ShinyTick(void)
{
    static struct PartyPokemon ALIGN4 sMon;
    void *save = SaveBlock2_get();
    struct Party *party = SaveData_GetPlayerPartyPtr(save);
    struct PlayerProfile *profile = Sav2_PlayerData_GetProfileAddr(save);
    BAG_DATA *bag = Sav2_Bag_get(save);
    struct HackTestReport *report = &gHackTestReport;
    u32 phase;

    for (phase = 0; phase < 3; phase++) {
        if (report->shinyTotal[phase] < HACK_TEST_SHINY_SAMPLES) {
            break;
        }
    }
    if (phase == 3) {
        return;
    }
    if (phase != 0) {
        bag->keyItems[1].id = ITEM_SHINY_CHARM;
        bag->keyItems[1].quantity = 1;
    }
    for (u32 i = 0; i < HACK_TEST_SHINY_PER_TICK; i++) {
        BOOL shiny;
        if (phase == 2) {
            PokeParty_Init(party, 6);
            GiveMon(HEAPID_WORLD, save, SPECIES_RATTATA, 5, 0, 0, 0, 0, 0);
            shiny = MonIsShiny(Party_GetMonByIndex(party, 0));
        } else {
            PokeParaSet(&sMon, SPECIES_RATTATA, 5, 32, FALSE, 0, ID_SET, profile->id);
            shiny = MonIsShiny(&sMon);
        }
        report->shinyTotal[phase]++;
        if (shiny) {
            report->shinyHits[phase]++;
        }
    }
}

/**
 *  @brief run the vanilla Day Care step routine right at the step where it rolls for an egg, with a
 *         male and a female Rattata of the same trainer in the Day Care (compatibility 50)
 */
static void HackTest_DayCareTick(void)
{
    void *save = SaveBlock2_get();
    Daycare *daycare = Save_Daycare_Get(save);
    struct Party *party = SaveData_GetPlayerPartyPtr(save);
    struct PlayerProfile *profile = Sav2_PlayerData_GetProfileAddr(save);
    BAG_DATA *bag = Sav2_Bag_get(save);
    struct HackTestReport *report = &gHackTestReport;
    u32 phase = report->eggRolls[0] < HACK_TEST_EGG_ROLLS ? 0 : 1;
    // vanilla save layout.  the Daycare struct of include/pokemon.h is 4 bytes too big per mon
    // (alignment), so only the first mon can be reached through it
    u8 *raw = (u8 *)daycare;
    u32 *eggPid = (u32 *)(raw + DAYCARE_EGG_PID_OFFSET);

    if (report->eggRolls[1] >= HACK_TEST_EGG_ROLLS) {
        return;
    }
    if (report->eggRolls[0] == 0) {
        // Rattata is female when the low byte of the personality is below 127
        CreateBoxMonData(Daycare_GetBoxMonI(daycare, 0), SPECIES_RATTATA, 20, 32, TRUE, 0x000000C8, ID_NO_SET, 0);
        CreateBoxMonData(Daycare_GetBoxMonI(daycare, 1), SPECIES_RATTATA, 20, 32, TRUE, 0x00000010, ID_NO_SET, 0);
    }
    if (phase == 1) {
        bag->keyItems[1].id = ITEM_SHINY_CHARM;
        bag->keyItems[1].quantity = 1;
        bag->keyItems[2].id = ITEM_OVAL_CHARM;
        bag->keyItems[2].quantity = 1;
    }
    {
        struct BoxPokemon *parents[2];
        Daycare_GetBothBoxMonsPtr(daycare, parents);
        report->padding2 = Daycare_CalcCompatibilityInternal(parents); // debug aid: 50 is expected
    }
    for (u32 i = 0; i < HACK_TEST_EGG_ROLLS_PER_TICK; i++) {
        *eggPid = 0;
        raw[DAYCARE_EGG_CYCLES_OFFSET] = 0;
        // the routine adds a step and rolls when the low byte is 0xFF
        *(u32 *)(raw + DAYCARE_STEPS_OFFSET) = 0xFE;
        *(u32 *)(raw + DAYCARE_MON_SIZE + DAYCARE_STEPS_OFFSET) = 0xFE;
        HandleDaycareStep(daycare, party, gFieldSysPtr);
        report->eggRolls[phase]++;
        if (*eggPid != 0) {
            report->eggs[phase]++;
            if (SHINY_CHECK(profile->id, *eggPid)) {
                report->shinyEggs[phase]++;
            }
        }
    }
    *eggPid = 0;
}

/**
 *  @brief called once per frame while the player can move in the overworld
 */
void HackTest_FieldTick(void)
{
    if (!sHackTestStarted) {
        u32 request = *HACK_TEST_HOLE;
        if ((request >> 16) != HACK_TEST_REQUEST_MAGIC || ++sHackTestWait < 30) {
            return;
        }
        sHackTestStarted = TRUE;
        gHackTestReport.scenario = request & 0xFFFF;
        HackTest_Setup(gHackTestReport.scenario);
        switch (gHackTestReport.scenario) {
        case HACK_TEST_SHOP:
            EventSet_Script(gFieldSysPtr, 2075, NULL);
            break;
        case HACK_TEST_BOTTLE_CAPS:
        case HACK_TEST_EXP_SHARE_TOGGLE:
        case HACK_TEST_SHINY_CHARM:
        case HACK_TEST_DAY_CARE:
        case HACK_TEST_BIKE:
        case HACK_TEST_STATIC_MON:
            break; // driven from the menu by the python side
        default:
            EventSet_Script(gFieldSysPtr, 2073, NULL);
            break;
        }
    }
    if (gHackTestReport.scenario == HACK_TEST_SHINY_CHARM) {
        HackTest_ShinyTick();
    } else if (gHackTestReport.scenario == HACK_TEST_DAY_CARE) {
        HackTest_DayCareTick();
    }
    HackTest_UpdateReport();
    *HACK_TEST_HOLE = (u32)&gHackTestReport;
}

#endif // HACK_TEST
