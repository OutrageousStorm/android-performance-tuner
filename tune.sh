#!/bin/bash
# tune.sh -- Performance profile switcher
set -e
PROFILE="${1:-balanced}"
adb devices | grep -q device || { echo "No device"; exit 1; }
case "$PROFILE" in
  gaming)
    echo "🎮 Gaming mode"
    adb shell settings put global screen_brightness 255
    adb shell settings put system screen_timeout 600000
    adb shell cmd netpolicy restrict-background com.facebook.katana
    echo "  ✓ Max brightness, long timeout, ads restricted"
    ;;
  battery)
    echo "🔋 Battery saver"
    adb shell settings put system screen_brightness 80
    adb shell settings put system screen_timeout 60000
    adb shell dumpsys deviceidle step deep
    adb shell cmd netpolicy restrict-background enable
    echo "  ✓ Aggressive doze, dim screen"
    ;;
  *)
    echo "⚖️  Balanced"
    adb shell settings put system screen_brightness 180
    adb shell settings put system screen_timeout 180000
    ;;
esac
echo "✅ Profile applied"
