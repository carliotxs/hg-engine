#!/usr/bin/env bash
# Play the debug ROM from a chapter (a point of the story with its flags, badges and party).
# Usage: hack/scripts/play.sh <chapter>      hack/scripts/play.sh --list
# Uses the debug ROM of the last hack/scripts/test.sh run (hack/out/test-debug.nds); run test.sh
# first after changing the code.  Chapters are defined in hack/scripts/gen_chapters.py.
set -euo pipefail
cd "$(dirname "$0")/../.."
if [ ! -f hack/out/test-debug.nds ]; then
    echo "error: no debug ROM yet, run hack/scripts/test.sh first" >&2
    exit 1
fi
if [ "${1:---list}" = "--list" ]; then
    exec .venv/bin/python hack/scripts/ingame_tests.py --list
fi
# play a private copy: test.sh rebuilds and replaces test-debug.nds, and the emulator reads the ROM
# from disk while it runs, so a rebuild in the middle of a session would break the game being played
mkdir -p hack/out/play
cp hack/out/test-debug.nds hack/out/play/play.nds
exec .venv/bin/python hack/scripts/ingame_tests.py --rom hack/out/play/play.nds --sav "${HG_TEST_SAV:-hack/out/test.sav}" --play "$1"
