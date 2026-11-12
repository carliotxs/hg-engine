#!/usr/bin/env bash
# Build the hack.  Usage: hack/scripts/build.sh [path/to/HeartGold_US.nds]
# The base ROM is never committed: pass its path once (or set HG_BASE_ROM) and it is copied to rom.nds.
set -euo pipefail
cd "$(dirname "$0")/../.."

BASE_ROM="${1:-${HG_BASE_ROM:-}}"
if [ -n "$BASE_ROM" ]; then
    cp "$BASE_ROM" rom.nds
fi
if [ ! -f rom.nds ]; then
    echo "error: no rom.nds. Run: hack/scripts/build.sh /path/to/HeartGold_US.nds" >&2
    exit 1
fi

# HeartGold (U) header check: game code IPKE
code=$(dd if=rom.nds bs=1 skip=12 count=4 2>/dev/null)
if [ "$code" != "IPKE" ]; then
    echo "error: rom.nds is not Pokemon HeartGold (U) (game code '$code', expected IPKE)" >&2
    exit 1
fi

JOBS="${JOBS:-$(nproc 2>/dev/null || sysctl -n hw.ncpu)}"
make -j"$JOBS"
echo "built: $(pwd)/test.nds"
