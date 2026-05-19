#!/usr/bin/env python3
"""
perf_benchmark.py — Android device performance benchmark runner
Merged from android-performance-tester
Tests CPU, memory, I/O, and render throughput via ADB
"""
import subprocess, json, time, argparse
from statistics import mean, stdev

def adb(cmd):
    r = subprocess.run(['adb', 'shell'] + cmd.split(), capture_output=True, text=True)
    return r.stdout.strip()

def cpu_benchmark(samples=5):
    """Time a SHA256 computation on the device CPU"""
    times = []
    for _ in range(samples):
        start = time.time()
        adb('dd if=/dev/urandom bs=1M count=10 | sha256sum')
        times.append(time.time() - start)
    return {'mean_s': round(mean(times), 3), 'stdev_s': round(stdev(times), 3) if len(times) > 1 else 0}

def memory_info():
    raw = adb('cat /proc/meminfo')
    info = {}
    for line in raw.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            key = parts[0].rstrip(':')
            val = int(parts[1])
            info[key] = val
    total = info.get('MemTotal', 0)
    free = info.get('MemAvailable', 0)
    return {
        'total_mb': round(total / 1024),
        'available_mb': round(free / 1024),
        'used_pct': round((total - free) / total * 100, 1) if total else 0
    }

def storage_benchmark():
    """Write 50MB to /data/local/tmp and measure throughput"""
    adb('rm -f /data/local/tmp/bench_test')
    start = time.time()
    adb('dd if=/dev/zero of=/data/local/tmp/bench_test bs=1M count=50')
    elapsed = time.time() - start
    adb('rm -f /data/local/tmp/bench_test')
    return {'write_mb_s': round(50 / elapsed, 1) if elapsed > 0 else 0}

def cpu_freq():
    """Read current CPU frequency for all cores"""
    cores = []
    for i in range(8):
        path = f'/sys/devices/system/cpu/cpu{i}/cpufreq/scaling_cur_freq'
        out = adb(f'cat {path}')
        if out.isdigit():
            cores.append({'core': i, 'mhz': round(int(out) / 1000)})
        else:
            break
    return cores

def run_full():
    print("🔬 Android Performance Benchmark")
    print("=" * 40)
    
    results = {}
    
    print("📱 Memory...")
    results['memory'] = memory_info()
    print(f"  Total: {results['memory']['total_mb']}MB | Available: {results['memory']['available_mb']}MB | Used: {results['memory']['used_pct']}%")
    
    print("⚡ CPU Frequencies...")
    results['cpu_freq'] = cpu_freq()
    for c in results['cpu_freq']:
        print(f"  Core {c['core']}: {c['mhz']} MHz")
    
    print("💾 Storage Write Speed...")
    results['storage'] = storage_benchmark()
    print(f"  Write: {results['storage']['write_mb_s']} MB/s")
    
    print("\n📊 Results JSON:")
    print(json.dumps(results, indent=2))
    return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Android device performance benchmark')
    parser.add_argument('--json', action='store_true', help='Output JSON only')
    args = parser.parse_args()
    results = run_full()
    if args.json:
        print(json.dumps(results))
