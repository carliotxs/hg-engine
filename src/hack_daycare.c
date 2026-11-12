#include "../include/config.h"
#include "../include/types.h"

#include "../include/bag.h"
#include "../include/constants/item.h"
#include "../include/pokemon.h"
#include "../include/save.h"

/*
 * Day Care changes of the hack.  Both functions replace small vanilla routines of the arm9
 * (see the hooks file); the vanilla code they call is declared in rom.ld.
 */

s32 LONG_CALL Daycare_GetEverstoneParent(Daycare *daycare); // index of the parent that passes its nature, negative if none
u32 LONG_CALL Daycare_CalcCompatibilityInternal(struct BoxPokemon **parents); // 0, 20, 50 or 70
u32 LONG_CALL gf_mtRand(void);
void LONG_CALL Save_Daycare_SetEggPID(Daycare *daycare, u32 pid);

#ifdef HACK_OVAL_CHARM

// return address of the call in the vanilla step routine that rolls for an egg every 256 steps
#define DAYCARE_STEP_COMPATIBILITY_CALLER (0x0206CD80 | 1)

/**
 *  @brief egg chance with the Oval Charm, same values as Gen 5 and later
 */
u32 LONG_CALL Daycare_ApplyOvalCharm(u32 compatibility)
{
    if (!PlayerHasKeyItem(ITEM_OVAL_CHARM)) {
        return compatibility;
    }
    switch (compatibility) {
    case 20:
        return 40;
    case 50:
        return 80;
    case 70:
        return 88;
    default:
        return compatibility;
    }
}

/**
 *  @brief replaces the vanilla compatibility getter.  the Day-Care Man's dialogue uses the same getter
 *         and compares the exact values, so the Oval Charm only applies to the egg roll of the step routine
 */
u32 LONG_CALL Daycare_GetCompatibility_Hack(Daycare *daycare)
{
    struct BoxPokemon *parents[2];
    u32 caller = (u32)__builtin_return_address(0);
    u32 compatibility;

    Daycare_GetBothBoxMonsPtr(daycare, parents);
    compatibility = Daycare_CalcCompatibilityInternal(parents);
    if (caller == DAYCARE_STEP_COMPATIBILITY_CALLER) {
        compatibility = Daycare_ApplyOvalCharm(compatibility);
    }
    return compatibility;
}

#endif // HACK_OVAL_CHARM

#ifdef HACK_SHINY_CHARM

/**
 *  @brief vanilla behaviour: a random personality, with the nature of the Everstone parent if there is one
 */
static u32 Daycare_RollEggPersonality(Daycare *daycare, s32 everstoneParent)
{
    u32 pid = gf_mtRand();
    if (everstoneParent >= 0) {
        u8 nature = GetNatureFromPersonality(GetBoxMonData(Daycare_GetBoxMonI(daycare, everstoneParent), MON_DATA_PERSONALITY, NULL));
        for (u32 tries = 0; tries <= 2400; tries++) {
            if (GetNatureFromPersonality(pid) == nature && pid != 0) {
                break;
            }
            pid = gf_mtRand();
        }
    }
    return pid;
}

/**
 *  @brief replaces the vanilla routine that decides the personality of a new egg,
 *         adding the extra shiny rolls of the Shiny Charm (the Masuda method rolls still happen later)
 */
void LONG_CALL Daycare_SetPendingEgg_Hack(Daycare *daycare)
{
    s32 everstoneParent = Daycare_GetEverstoneParent(daycare);
    u32 pid = Daycare_RollEggPersonality(daycare, everstoneParent);

    if (PlayerHasKeyItem(ITEM_SHINY_CHARM)) {
        u32 id = Sav2_PlayerData_GetProfileAddr(SaveBlock2_get())->id;
        for (u32 roll = 0; roll < SHINY_CHARM_EXTRA_ROLLS && !SHINY_CHECK(id, pid); roll++) {
            u32 newPid = Daycare_RollEggPersonality(daycare, everstoneParent);
            if (newPid != 0) {
                pid = newPid;
            }
        }
    }
    Save_Daycare_SetEggPID(daycare, pid);
}

#endif // HACK_SHINY_CHARM
