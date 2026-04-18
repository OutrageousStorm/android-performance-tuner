#!/bin/bash
# performance_mode.sh -- One-shot Android performance optimization
# Usage: ./performance_mode.sh [profile: balanced|performance|battery]

PROFILE="${1:-balanced}"
echo "⚡ Android Performance Mode: $PROFILE"

case "$PROFILE" in
    performance)
        echo "  🚀 Max performance settings..."
        adb shell settings put global transition_animation_scale 0.5
        adb shell settings put global window_animation_scale 0.5
        adb shell settings put global animator_duration_scale 0.5
        adb shell settings put secure show_touches 1
        adb shell settings put system screen_brightness 255
        adb shell settings put system screen_brightness_mode 0
        adb shell pm set-idle-state --user 0 com.android.gms false 2>/dev/null || true
        echo "  ✅ Done. Max perf engaged."
        ;;
    battery)
        echo "  🔋 Battery saver mode..."
        adb shell settings put global transition_animation_scale 1.5
        adb shell settings put global window_animation_scale 1.5
        adb shell settings put global animator_duration_scale 1.5
        adb shell settings put system screen_brightness 80
        adb shell settings put system screen_brightness_mode 1  # auto
        adb shell cmd display high_refresh_rate disable
        echo "  ✅ Battery optimization active."
        ;;
    *)  # balanced
        echo "  ⚖️  Balanced mode..."
        adb shell settings put global transition_animation_scale 1.0
        adb shell settings put global window_animation_scale 1.0
        adb shell settings put global animator_duration_scale 1.0
        adb shell settings put system screen_brightness 180
        adb shell settings put system screen_brightness_mode 1
        echo "  ✅ Balanced settings applied."
        ;;
esac
