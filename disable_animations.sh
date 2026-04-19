#!/bin/bash
adb shell settings put global window_animation_scale 0
adb shell settings put global transition_animation_scale 0
echo 'Animations disabled'
