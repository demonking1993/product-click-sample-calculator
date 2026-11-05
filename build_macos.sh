#!/bin/zsh
set -euo pipefail

cd "$(dirname "$0")"

PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR=".venv-macos-build"

if [[ ! -x "$VENV_DIR/bin/python" ]]; then
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

"$VENV_DIR/bin/python" -m pip install --upgrade pip wheel
"$VENV_DIR/bin/python" -m pip install --upgrade "pyinstaller==6.21.0"

rm -rf app.iconset
mkdir app.iconset
sips -z 16 16 app_1024.png --out app.iconset/icon_16x16.png >/dev/null
sips -z 32 32 app_1024.png --out app.iconset/icon_16x16@2x.png >/dev/null
sips -z 32 32 app_1024.png --out app.iconset/icon_32x32.png >/dev/null
sips -z 64 64 app_1024.png --out app.iconset/icon_32x32@2x.png >/dev/null
sips -z 128 128 app_1024.png --out app.iconset/icon_128x128.png >/dev/null
sips -z 256 256 app_1024.png --out app.iconset/icon_128x128@2x.png >/dev/null
sips -z 256 256 app_1024.png --out app.iconset/icon_256x256.png >/dev/null
sips -z 512 512 app_1024.png --out app.iconset/icon_256x256@2x.png >/dev/null
sips -z 512 512 app_1024.png --out app.iconset/icon_512x512.png >/dev/null
cp app_1024.png app.iconset/icon_512x512@2x.png
iconutil -c icns app.iconset -o app.icns

rm -rf build dist
"$VENV_DIR/bin/pyinstaller" \
  --noconfirm \
  --clean \
  --windowed \
  --onedir \
  --name "测款神器" \
  --icon app.icns \
  --osx-bundle-identifier "com.cekuan.shenqi" \
  --target-arch universal2 \
  app.py

PLIST="dist/测款神器.app/Contents/Info.plist"
plist_string() {
  /usr/libexec/PlistBuddy -c "Set :$1 $2" "$PLIST" 2>/dev/null || \
    /usr/libexec/PlistBuddy -c "Add :$1 string $2" "$PLIST"
}

plist_string CFBundleDisplayName "测款神器"
plist_string CFBundleShortVersionString "1.0.0"
plist_string CFBundleVersion "1"
/usr/libexec/PlistBuddy -c "Set :NSHighResolutionCapable true" "$PLIST" 2>/dev/null || \
  /usr/libexec/PlistBuddy -c "Add :NSHighResolutionCapable bool true" "$PLIST"

codesign --force --deep --sign - "dist/测款神器.app"
codesign --verify --deep --strict --verbose=2 "dist/测款神器.app"

rm -f "dist/测款神器-Mac-universal.zip"
ditto -c -k --sequesterRsrc --keepParent "dist/测款神器.app" "dist/测款神器-Mac-universal.zip"

echo "Mac build complete: $PWD/dist/测款神器-Mac-universal.zip"
