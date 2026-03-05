#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

source .venv/bin/activate

# Clean old outputs
rm -rf build dist *.spec

pyinstaller \
  --noconfirm \
  --clean \
  --windowed \
  --name "AIFX Player" \
  --target-architecture universal2 \
  --add-data "ui/player/assets:ui/player/assets" \
  -p . \
  ui/player/app.py

echo ""
echo "✅ Built: dist/AIFX Player.app"
