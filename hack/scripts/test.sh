#!/usr/bin/env bash
# In-game tests of the hack features: builds a debug ROM (make HACK_TEST=Y) and runs
# hack/scripts/ingame_tests.py on it.  Usage: hack/scripts/test.sh [scenario ...]
# The debug ROM goes to hack/out/test-debug.nds; test.nds is NOT a release ROM after this script,
# so the sources are touched at the end and the next build.sh/release.sh rebuilds the real one.
set -euo pipefail
cd "$(dirname "$0")/../.."

# files whose output depends on HACK_TEST: everything that includes config.h, and common script 2073
touch_flag_dependent() {
    touch include/config.h data/scr_seq/scr_seq_00003_commonscript.s
}

# any save that continues in the overworld works; by default the public hg-engine test save is used
SAV="${HG_TEST_SAV:-hack/out/test.sav}"
if [ ! -f "$SAV" ]; then
    mkdir -p "$(dirname "$SAV")"
    curl -sfL -o "$SAV" https://github.com/BluRosie/hg-engine/raw/workflows/assets/test.sav
fi

touch_flag_dependent
trap touch_flag_dependent EXIT
HACK_TEST=Y hack/scripts/build.sh "${HG_BASE_ROM:-}"
mkdir -p hack/out
cp test.nds hack/out/test-debug.nds
.venv/bin/python hack/scripts/ingame_tests.py --rom hack/out/test-debug.nds --sav "$SAV" --out hack/out/tests "$@"
