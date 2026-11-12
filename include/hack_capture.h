#ifndef HACK_CAPTURE_H
#define HACK_CAPTURE_H

#include "config.h"
#include "types.h"

// "add to party?" prompt after a capture with a full party, see src/hack_capture.c
struct PokemonStorageSystem;

void LONG_CALL HackCapture_MarkCaught(void);
void LONG_CALL HackCapture_OnStored(struct PokemonStorageSystem *storage, u32 box, u32 slot);
void LONG_CALL HackCapture_FieldTick(void);
BOOL LONG_CALL HackCapture_Swap(u32 partySlot);

#endif // HACK_CAPTURE_H
