#!/usr/bin/env python3
"""
tune.py -- Real-time Android performance tuning via ADB
Adjusts CPU governor, I/O scheduler, thermal throttling, and more.
Usage: python3 tune.py --profile gaming
       python3 tune.py --cpu powersave --io noop --thermal aggressive
"""
import subprocess, argparse, sys

def adb(cmd):
    r = subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True, text=True)
    return r.stdout.strip()

PROFILES = {
    "gaming": {
        "cpu_gov": "schedutil",
        "io_sched": "deadline",
        "gpu_boost": True,
        "thermal": "aggressive",
        "desc": "Max FPS + responsiveness"
    },
    "balanced": {
        "cpu_gov": "schedutil",
        "io_sched": "cfq",
        "gpu_boost": False,
        "thermal": "normal",
        "desc": "Default balanced mode"
    },
    "battery": {
        "cpu_gov": "powersave",
        "io_sched": "noop",
        "gpu_boost": False,
        "thermal": "conservative",
        "desc": "Maximum battery life"
    }
}

def set_governor(gov):
    cpus = adb("ls -d /sys/devices/system/cpu/cpu*/ | grep -o 'cpu[0-9]*'")
    for cpu in cpus.strip().split():
        path = f"/sys/devices/system/cpu/{cpu}/cpufreq/scaling_governor"
        adb(f"echo {gov} > {path} 2>/dev/null || true")
    print(f"  ✓ CPU governor: {gov}")

def set_io_scheduler(sched):
    adb(f"echo {sched} > /sys/block/sda/queue/scheduler 2>/dev/null || true")
    print(f"  ✓ I/O scheduler: {sched}")

def set_thermal(mode):
    if mode == "aggressive":
        adb("settings put global thermal_shutdown_temp 80 2>/dev/null || true")
    elif mode == "conservative":
        adb("settings put global thermal_shutdown_temp 90 2>/dev/null || true")
    print(f"  ✓ Thermal mode: {mode}")

def apply_profile(profile):
    if profile not in PROFILES:
        print(f"Unknown profile: {profile}")
        return False
    p = PROFILES[profile]
    print(f"\n📊 Applying profile: {profile} ({p['desc']})")
    set_governor(p["cpu_gov"])
    set_io_scheduler(p["io_sched"])
    set_thermal(p["thermal"])
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=list(PROFILES.keys()))
    parser.add_argument("--cpu", help="CPU governor (schedutil/powersave/performance)")
    parser.add_argument("--io", help="I/O scheduler (noop/deadline/cfq)")
    parser.add_argument("--thermal", choices=["aggressive","normal","conservative"])
    args = parser.parse_args()

    if args.profile:
        apply_profile(args.profile)
    elif args.cpu or args.io or args.thermal:
        print("\n🎛️  Custom tuning")
        if args.cpu: set_governor(args.cpu)
        if args.io: set_io_scheduler(args.io)
        if args.thermal: set_thermal(args.thermal)
    else:
        print("Available profiles:")
        for name, p in PROFILES.items():
            print(f"  {name}: {p['desc']}")

if __name__ == "__main__":
    main()
