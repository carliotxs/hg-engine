#!/usr/bin/env bash
# Package the build: zipped ROM for playing and, if xdelta3 is installed, a patch for sharing.
# Never share the .nds itself publicly; share the .xdelta patch instead.
set -euo pipefail
cd "$(dirname "$0")/../.."
VERSION="${1:-$(git describe --tags --always --dirty 2>/dev/null || date +%Y%m%d)}"
mkdir -p hack/out
NAME="HeartGold-hack-$VERSION"
cp test.nds "hack/out/$NAME.nds"
(cd hack/out && rm -f "$NAME.zip" && zip -9 -q "$NAME.zip" "$NAME.nds" && rm "$NAME.nds")
echo "hack/out/$NAME.zip"
if command -v xdelta3 >/dev/null; then
    xdelta3 -e -f -s rom.nds test.nds "hack/out/$NAME.xdelta"
    echo "hack/out/$NAME.xdelta"
fi
