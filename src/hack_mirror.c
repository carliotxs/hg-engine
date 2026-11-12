#include "../include/config.h"
#include "../include/types.h"

#ifdef HACK_MIRROR_SPECIALISTS

/*
 * Species specialists ("mirror match"): a Trainer for every fully evolved or single stage Pokémon
 * that is found in the wild, placed by hack/scripts/gen_specialists.py.  A specialist only battles a
 * player that brings the same species, one on one.
 *
 * The map scripts call common script SCRIPT_MIRROR_SPECIALIST, which talks to this file through the
 * day_care_sanitize_mon command (see ScrCmd_DaycareSanitizeMon): the result var holds one of the
 * HACK_MIRROR_OP_* values on entry.  During the battle the player's party is replaced by the chosen
 * Pokémon alone and the single Pokémon of trainer HACK_TRAINER_MIRROR becomes the requested species
 * and level (see MakeTrainerPokemonParty); afterwards the party is put back.
 */

#include "../include/battle.h"
#include "../include/hack_mirror.h"
#include "../include/pokemon.h"
#include "../include/save.h"
#include "../include/script.h"

// the party as it is in the save: two counters and six Pokémon of 236 bytes.  struct Party of the
// engine headers is bigger than that (alignment), so it must never be copied or indexed directly
#define SAVE_PARTY_SIZE (8 + 6 * 236)
static u8 ALIGN4 sPartyBackup[SAVE_PARTY_SIZE];
static u8 sActive = FALSE;
static u8 sSlot = 0;
static u16 sSpecies = 0;
static u16 sLevel = 0;

/**
 *  @brief party slot of the first healthy Pokémon of the species, 0xFF if there is none
 */
static u32 HackMirror_FindSpecies(struct Party *party, u16 species)
{
    for (s32 i = 0; i < party->count; i++) {
        struct PartyPokemon *pp = Party_GetMonByIndex(party, i);
        if (GetMonData(pp, MON_DATA_SPECIES, NULL) == species && !GetMonData(pp, MON_DATA_IS_EGG, NULL) && GetMonData(pp, MON_DATA_HP, NULL) != 0) {
            return i;
        }
    }
    return 0xFF;
}

u32 LONG_CALL HackMirror_ScriptOp(u16 op, u16 arg)
{
    struct Party *party = SaveData_GetPlayerPartyPtr(SaveBlock2_get());

    switch (op) {
    case HACK_MIRROR_OP_FIND:
        return HackMirror_FindSpecies(party, arg);

    case HACK_MIRROR_OP_BEGIN:
        if (sActive || arg >= (u32)party->count) {
            return 0xFF;
        }
        memcpy(sPartyBackup, party, SAVE_PARTY_SIZE);
        sSlot = arg;
        sSpecies = GetScriptVar(HACK_MIRROR_VAR_SPECIES);
        sLevel = GetScriptVar(HACK_MIRROR_VAR_LEVEL);
        PokeParty_Init(party, 6);
        PokeParty_Add(party, Party_GetMonByIndex((struct Party *)sPartyBackup, sSlot));
        sActive = TRUE;
        return 0;

    case HACK_MIRROR_OP_END:
        if (sActive) {
            // keep what the battle did to the Pokémon (HP, PP, experience) and bring the others back
            PokeCopyPPtoPP(Party_GetMonByIndex(party, 0), Party_GetMonByIndex((struct Party *)sPartyBackup, sSlot));
            memcpy(party, sPartyBackup, SAVE_PARTY_SIZE);
            sActive = FALSE;
        }
        return 0;
    }
    return 0xFF;
}

/**
 *  @brief species and level of the specialist's Pokémon while a mirror match is being set up
 */
BOOL LONG_CALL HackMirror_GetOverride(u16 *species, u16 *level)
{
    if (!sActive) {
        return FALSE;
    }
    *species = sSpecies;
    *level = sLevel;
    return TRUE;
}

#endif // HACK_MIRROR_SPECIALISTS
