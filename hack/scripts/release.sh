#!/usr/bin/env bash
# Full pipeline: build -> boot test -> new game test -> package.  Usage: hack/scripts/release.sh [base_rom] [version]
set -euo pipefail
cd "$(dirname "$0")/../.."
hack/scripts/build.sh "${1:-}"
.venv/bin/python hack/scripts/verify.py test.nds hack/out/verify
.venv/bin/python hack/scripts/newgame.py test.nds hack/out/newgame
hack/scripts/package.sh "${2:-}"
