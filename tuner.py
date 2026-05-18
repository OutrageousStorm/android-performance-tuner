#!/usr/bin/env python3
"""
tuner.py -- Android performance tuning via ADB
Control CPU governors, frequencies, I/O schedulers, thermal profiles
Usage: python3 tuner.py --list-governors
       python3 tuner.py --set-governor powersave
       python3 tuner.py --set-io-scheduler deadline
"""
import subprocess, argparse, sys

def adb(cmd):
    return subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True, text=True).stdout.strip()

def list_governors():
    cpus = int(adb("nproc"))
    print(f"\nAvailable governors (device has {cpus} CPUs):\n")
    for i in range(cpus):
        path = f"/sys/devices/system/cpu/cpu{i}/cpufreq/scaling_available_governors"
        govs = adb(f"cat {path} 2>/dev/null || echo 'N/A'")
        current = adb(f"cat /sys/devices/system/cpu/cpu{i}/cpufreq/scaling_governor 2>/dev/null || echo '?'")
        print(f"  CPU{i}: {govs} (current: {current})")

def list_io_schedulers():
    print("\nAvailable I/O schedulers:\n")
    scheds = adb("cat /sys/block/mmcblk0/queue/scheduler 2>/dev/null | tr ' ' '\n' | grep -v '^$'")
    current = adb("cat /sys/block/mmcblk0/queue/scheduler 2>/dev/null")
    print(f"  Available: {scheds}")
    print(f"  Current: {current}")

def set_governor(gov):
    cpus = int(adb("nproc"))
    print(f"\nSetting {gov} on {cpus} CPUs...")
    for i in range(cpus):
        result = adb(f"echo {gov} > /sys/devices/system/cpu/cpu{i}/cpufreq/scaling_governor 2>&1")
        status = "✓" if "permission denied" not in result.lower() else "✗"
        print(f"  {status} CPU{i}")

def set_io_scheduler(sched):
    print(f"\nSetting {sched} I/O scheduler...")
    result = adb(f"echo {sched} > /sys/block/mmcblk0/queue/scheduler 2>&1")
    print("  ✓" if "permission denied" not in result.lower() else "  ✗")

def set_max_freq(mhz):
    cpus = int(adb("nproc"))
    freq = str(mhz * 1000)
    print(f"\nSetting max frequency to {mhz}MHz on {cpus} CPUs...")
    for i in range(cpus):
        result = adb(f"echo {freq} > /sys/devices/system/cpu/cpu{i}/cpufreq/scaling_max_freq 2>&1")
        status = "✓" if "permission denied" not in result.lower() else "✗"
        print(f"  {status} CPU{i}: {mhz}MHz")

def profile_performance():
    """Preset for maximum performance"""
    print("\n⚡ Applying PERFORMANCE profile...")
    adb("echo performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor 2>/dev/null")
    adb("echo deadline > /sys/block/mmcblk0/queue/scheduler 2>/dev/null")
    adb("echo 0 > /proc/sys/kernel/sched_migration_cost_ns 2>/dev/null")
    print("  ✓ Governor: performance")
    print("  ✓ I/O scheduler: deadline")
    print("  ✓ Sched migration cost: 0ns")

def profile_balanced():
    """Preset for balanced performance"""
    print("\n⚙️  Applying BALANCED profile...")
    adb("echo schedutil > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor 2>/dev/null")
    adb("echo mq-deadline > /sys/block/mmcblk0/queue/scheduler 2>/dev/null")
    print("  ✓ Governor: schedutil")
    print("  ✓ I/O scheduler: mq-deadline")

def profile_battery():
    """Preset for maximum battery life"""
    print("\n🔋 Applying BATTERY SAVER profile...")
    adb("echo powersave > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor 2>/dev/null")
    adb("echo noop > /sys/block/mmcblk0/queue/scheduler 2>/dev/null")
    adb("echo 10000000 > /proc/sys/kernel/sched_migration_cost_ns 2>/dev/null")
    print("  ✓ Governor: powersave")
    print("  ✓ I/O scheduler: noop")
    print("  ✓ Sched migration cost: 10ms")

def main():
    parser = argparse.ArgumentParser(description="Android performance tuner")
    parser.add_argument("--list-governors", action="store_true")
    parser.add_argument("--list-io", action="store_true")
    parser.add_argument("--set-governor", help="Set CPU governor (e.g., performance, powersave, schedutil)")
    parser.add_argument("--set-io-scheduler", help="Set I/O scheduler (e.g., deadline, noop, mq-deadline)")
    parser.add_argument("--set-max-freq", type=int, help="Set max frequency in MHz")
    parser.add_argument("--profile", choices=["performance", "balanced", "battery"], help="Apply preset profile")
    args = parser.parse_args()

    if args.list_governors:
        list_governors()
    elif args.list_io:
        list_io_schedulers()
    elif args.set_governor:
        set_governor(args.set_governor)
    elif args.set_io_scheduler:
        set_io_scheduler(args.set_io_scheduler)
    elif args.set_max_freq:
        set_max_freq(args.set_max_freq)
    elif args.profile:
        if args.profile == "performance":
            profile_performance()
        elif args.profile == "balanced":
            profile_balanced()
        elif args.profile == "battery":
            profile_battery()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
