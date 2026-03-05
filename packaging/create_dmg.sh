#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

APP_NAME="AIFX Player"
APP_BUNDLE="dist/${APP_NAME}.app"
DMG_DIR="dist"
DMG_RW="${DMG_DIR}/${APP_NAME}-temp.dmg"
DMG_FINAL="${DMG_DIR}/${APP_NAME}.dmg"
VOL_NAME="${APP_NAME}"
ICON_PATH="assets/icon/AIFX_Player.icns"
BG_PRIMARY="assets/dmg/background.png"
BG_FALLBACK="assets/dmg/background_resized.png"

if [[ ! -d "$APP_BUNDLE" ]]; then
  echo "Missing app bundle: $APP_BUNDLE" >&2
  exit 1
fi

if [[ ! -f "$ICON_PATH" ]]; then
  echo "Missing icon: $ICON_PATH" >&2
  exit 1
fi

BG_PATH="$BG_PRIMARY"
if [[ ! -f "$BG_PATH" ]]; then
  BG_PATH="$BG_FALLBACK"
fi
if [[ ! -f "$BG_PATH" ]]; then
  echo "Missing DMG background (tried $BG_PRIMARY and $BG_FALLBACK)" >&2
  exit 1
fi

mkdir -p "$DMG_DIR"
rm -f "$DMG_RW" "$DMG_FINAL"

TMP_STAGE="$(mktemp -d)"
cleanup() {
  rm -rf "$TMP_STAGE"
}
trap cleanup EXIT

cp -R "$APP_BUNDLE" "$TMP_STAGE/"
ln -s /Applications "$TMP_STAGE/Applications"
mkdir -p "$TMP_STAGE/.background"
cp "$BG_PATH" "$TMP_STAGE/.background/background.png"
cp "$ICON_PATH" "$TMP_STAGE/.VolumeIcon.icns"

hdiutil create \
  -srcfolder "$TMP_STAGE" \
  -volname "$VOL_NAME" \
  -fs HFS+ \
  -format UDRW \
  "$DMG_RW"

ATTACH_PLIST="$(mktemp)"
hdiutil attach "$DMG_RW" -noverify -nobrowse -plist > "$ATTACH_PLIST"

MOUNT_POINT="$(
python3 - "$ATTACH_PLIST" <<'PY'
import plistlib
import sys

with open(sys.argv[1], "rb") as f:
    data = plistlib.load(f)

for entity in data.get("system-entities", []):
    mount = entity.get("mount-point")
    if mount:
        print(mount)
        break
PY
)"
rm -f "$ATTACH_PLIST"

if [[ -z "${MOUNT_POINT:-}" ]]; then
  echo "Failed to determine mounted DMG path." >&2
  hdiutil detach "$DMG_RW" -force >/dev/null 2>&1 || true
  exit 1
fi

if command -v SetFile >/dev/null 2>&1; then
  SetFile -c icnC "$MOUNT_POINT/.VolumeIcon.icns" || true
  SetFile -a C "$MOUNT_POINT" || true
fi

osascript <<APPLESCRIPT
tell application "Finder"
  tell disk "${VOL_NAME}"
    open
    set current view of container window to icon view
    set toolbar visible of container window to false
    set statusbar visible of container window to false
    set the bounds of container window to {120, 120, 980, 620}
    set viewOptions to the icon view options of container window
    set arrangement of viewOptions to not arranged
    set icon size of viewOptions to 128
    set text size of viewOptions to 12
    set background picture of viewOptions to file ".background:background.png"
    set position of item "${APP_NAME}.app" of container window to {220, 260}
    set position of item "Applications" of container window to {640, 260}
    close
    open
    update without registering applications
    delay 1
  end tell
end tell
APPLESCRIPT

hdiutil detach "$MOUNT_POINT"

hdiutil convert "$DMG_RW" -format UDZO -imagekey zlib-level=9 -o "$DMG_FINAL"
rm -f "$DMG_RW"

echo "Created DMG: $DMG_FINAL"
