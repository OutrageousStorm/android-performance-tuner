#!/bin/bash
# performance.sh -- Boost Android performance without root
# Disables animations, reduces motion, optimizes GPU
# Usage: ./performance.sh [--revert]

set -e

if [[ "$1" == "--revert" ]]; then
    echo "⏮️  Reverting to defaults..."
    adb shell settings put global window_animation_scale 1
    adb shell settings put global transition_animation_scale 1
    adb shell settings put global animator_duration_scale 1
    adb shell settings put system haptic_feedback_enabled 1
    adb shell settings put secure touch_exploration_enabled 0
    adb shell settings put global gpu_debug_level 0
    echo "✓ Done"
    exit 0
fi

echo "⚡ Android Performance Tuner"
echo "============================="
echo ""
echo "Applying optimizations..."

# Disable animations
echo "  Animation scales..."
adb shell settings put global window_animation_scale 0
adb shell settings put global transition_animation_scale 0
adb shell settings put global animator_duration_scale 0

# Reduce motion
echo "  Disabling haptic feedback..."
adb shell settings put system haptic_feedback_enabled 0

# GPU acceleration
echo "  GPU rendering..."
adb shell settings put global gpu_debug_level 0
adb shell settings put global debug.force_rtl false

# Window optimizations
echo "  Window manager..."
adb shell settings put global window_manager_boot_animation false

# Disable immersive mode sticky for better performance
adb shell settings put global policy_control immersive.navigation=*

echo ""
echo "✅ Performance tuning complete!"
echo ""
echo "Revert with: ./performance.sh --revert"
