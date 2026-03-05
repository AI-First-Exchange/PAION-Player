#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

APP_NAME="AIFX Player"
APP_ENTRY="ui/player/app.py"
ICON_PATH="assets/icon/AIFX_Player.icns"
APP_PATH="dist/${APP_NAME}.app"
APP_BIN="${APP_PATH}/Contents/MacOS/${APP_NAME}"

if [[ ! -f "$APP_ENTRY" ]]; then
  echo "Missing app entry: $APP_ENTRY" >&2
  exit 1
fi

if [[ ! -f "$ICON_PATH" ]]; then
  echo "Missing icon: $ICON_PATH" >&2
  exit 1
fi

rm -rf build dist *.spec

pyinstaller \
  --noconfirm \
  --clean \
  --windowed \
  --name "$APP_NAME" \
  --icon "$ICON_PATH" \
  --target-architecture universal2 \
  --add-data "assets:assets" \
  -p . \
  "$APP_ENTRY"

if [[ ! -f "$APP_BIN" ]]; then
  echo "Build finished but app binary not found: $APP_BIN" >&2
  exit 1
fi

echo ""
echo "Universal binary verification:"
file "$APP_BIN"
lipo -archs "$APP_BIN"

echo ""
echo "Built app: $APP_PATH"
