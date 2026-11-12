#ifndef HACK_MIRROR_H
#define HACK_MIRROR_H

#include "config.h"
#include "types.h"

// species specialists ("mirror match"), see src/hack_mirror.c
#define HACK_MIRROR_OP_FIND  0x4D30 // arg: species.  result: party slot of that species or 0xFF
#define HACK_MIRROR_OP_BEGIN 0x4D31 // arg: party slot.  the party becomes that Pokémon alone
#define HACK_MIRROR_OP_END   0x4D32 // the party is put back
#define HACK_MIRROR_OP_MASK  0xFFF0
#define HACK_MIRROR_OP_BASE  0x4D30

#define HACK_MIRROR_VAR_SPECIES 0x8004 // VAR_SPECIAL_x8004 in the script
#define HACK_MIRROR_VAR_LEVEL   0x8005 // VAR_SPECIAL_x8005 in the script

u32 LONG_CALL HackMirror_ScriptOp(u16 op, u16 arg);
BOOL LONG_CALL HackMirror_GetOverride(u16 *species, u16 *level);

#endif // HACK_MIRROR_H
