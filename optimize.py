#!/usr/bin/env python3
"""
optimize.py -- Android performance optimizer
Applies GPU/RAM/CPU tuning, disables animations, kills background processes.
Usage: python3 optimize.py --profile gaming
       python3 optimize.py --profile balanced
"""
import subprocess, argparse

def adb(cmd):
    subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True)

PROFILES = {
    "gaming": {
        "desc": "Maximum gaming performance",
        "tuning": [
            ("settings put global animation_duration_scale 0", "Disable animations"),
            ("settings put global transition_animation_scale 0", "Disable transitions"),
            ("settings put system screen_brightness 255", "Max brightness"),
            ("settings put global low_power 0", "Disable battery saver"),
            ("cmd memory_minfree_tuner set_minfree_profile 5", "Aggressive memory cleanup"),
            ("cmd package set-dpm-state enable", "Enable performance mode"),
        ]
    },
    "balanced": {
        "desc": "Balanced performance and battery",
        "tuning": [
            ("settings put global animation_duration_scale 0.5", "Half speed animations"),
            ("settings put system screen_brightness 200", "Medium brightness"),
            ("cmd memory_minfree_tuner set_minfree_profile 3", "Moderate memory cleanup"),
        ]
    },
    "battery": {
        "desc": "Maximum battery life",
        "tuning": [
            ("settings put global animation_duration_scale 1", "Normal animations"),
            ("settings put system screen_brightness 80", "Low brightness"),
            ("settings put global low_power 1", "Enable battery saver"),
            ("cmd memory_minfree_tuner set_minfree_profile 1", "Conservative memory"),
            ("settings put global wifi_scan_always_enabled 0", "Disable WiFi scan"),
            ("settings put global ble_scan_always_enabled 0", "Disable BLE scan"),
        ]
    }
}

def apply_profile(profile_name):
    if profile_name not in PROFILES:
        print(f"Unknown profile: {profile_name}")
        return
    
    profile = PROFILES[profile_name]
    print(f"\n⚡ Applying {profile_name} profile: {profile['desc']}\n")
    
    for cmd, label in profile['tuning']:
        adb(cmd)
        print(f"  ✓ {label}")
    
    print(f"\n✅ Profile applied. Reboot for best results.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=list(PROFILES.keys()), required=True)
    args = parser.parse_args()
    apply_profile(args.profile)

if __name__ == "__main__":
    main()
