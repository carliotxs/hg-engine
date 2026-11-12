#include "../include/config.h"
#include "../include/types.h"

#ifdef HACK_CAPTURE_PARTY_PROMPT

/*
 * "Add to party?" prompt after catching a Pokémon with a full party.
 *
 * The capture sequence of the battle is left alone: the Pokémon goes to the PC as usual.  This file
 * remembers where it went and, back in the overworld, queues common script SCRIPT_CAPTURE_PROMPT,
 * which asks the question and lets the player pick the party member that goes to the PC instead.
 * The script cannot touch the PC itself, so it writes the chosen party slot (plus 1) to
 * HACK_VAR_PARTY_SWAP and the swap is done here on the next field tick.
 */

#include "../include/constants/file.h"
#include "../include/hack_capture.h"
#include "../include/pokemon.h"
#include "../include/pokemon_storage_system.h"
#include "../include/save.h"
#include "../include/script.h"

#define CAPTURE_PROMPT_DELAY 8 // field ticks to wait after the battle before the script starts

struct BoxPokemon *PCStorage_GetMonByIndexPair(PCStorage *storage, u32 boxno, u32 slotno);
BOOL PCStorage_PlaceMonInBoxByIndexPair(PCStorage *storage, u32 boxno, u32 slotno, struct BoxPokemon *boxMon);

static PCStorage *sStorage = NULL;
static u8 sCaughtInBattle = FALSE;
static u8 sPromptDelay = 0;
static u8 sBox = 0;
static u8 sSlot = 0;

#ifdef HACK_TEST
/**
 *  @brief in-game tests only: species in the PC slot where the last caught Pokémon was stored
 */
u16 LONG_CALL HackCapture_TestStoredSpecies(void)
{
    static PCStorage *lastStorage = NULL;
    if (sStorage != NULL) {
        lastStorage = sStorage;
    }
    if (lastStorage == NULL) {
        return 0;
    }
    return GetBoxMonData(PCStorage_GetMonByIndexPair(lastStorage, sBox, sSlot), MON_DATA_SPECIES, NULL);
}
#endif // HACK_TEST

/**
 *  @brief called by the battle code while a wild Pokémon is being caught
 */
void LONG_CALL HackCapture_MarkCaught(void)
{
    sCaughtInBattle = TRUE;
}

/**
 *  @brief called by the PC storage code whenever a Pokémon is put in the first free slot of a box
 */
void LONG_CALL HackCapture_OnStored(PCStorage *storage, u32 box, u32 slot)
{
    if (sCaughtInBattle) {
        sStorage = storage;
        sBox = box;
        sSlot = slot;
        sPromptDelay = CAPTURE_PROMPT_DELAY;
    }
}

/**
 *  @brief swap a party member with the Pokémon that was just sent to the PC
 */
static void HackCapture_Swap(u32 partySlot)
{
    struct Party *party = SaveData_GetPlayerPartyPtr(SaveBlock2_get());
    struct PartyPokemon *partyMon;
    struct BoxPokemon caught, leaving;

    if (sStorage == NULL || partySlot >= (u32)party->count) {
        return;
    }
    partyMon = Party_GetMonByIndex(party, partySlot);
    caught = *PCStorage_GetMonByIndexPair(sStorage, sBox, sSlot);
    leaving = partyMon->box;
    if (GetBoxMonData(&caught, MON_DATA_SPECIES, NULL) == SPECIES_NONE) {
        return; // the slot was emptied in the meantime: nothing to bring back
    }
    PCStorage_PlaceMonInBoxByIndexPair(sStorage, sBox, sSlot, &leaving);
    CopyBoxPokemonToPokemon(&caught, partyMon);
    sStorage = NULL;
}

/**
 *  @brief called once per frame while the player is in the overworld
 */
void LONG_CALL HackCapture_FieldTick(void)
{
    u16 request = GetScriptVar(HACK_VAR_PARTY_SWAP);

    sCaughtInBattle = FALSE;
    if (request != 0) {
        SetScriptVar(HACK_VAR_PARTY_SWAP, 0);
        HackCapture_Swap(request - 1);
    }
    if (sPromptDelay != 0 && --sPromptDelay == 0) {
        EventSet_Script(gFieldSysPtr, SCRIPT_CAPTURE_PROMPT, NULL);
    }
}

#endif // HACK_CAPTURE_PARTY_PROMPT
