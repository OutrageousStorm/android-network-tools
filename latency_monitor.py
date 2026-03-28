#!/usr/bin/env python3
"""
latency_monitor.py -- Real-time latency monitor via adb ping
Usage: python3 latency_monitor.py [--targets 8.8.8.8,1.1.1.1] [--interval 2]
"""
import subprocess, time, argparse, statistics
from collections import defaultdict

def adb_ping(host, count=4):
    """Ping from device and return latencies in ms"""
    out = subprocess.run(
        f"adb shell ping -c {count} {host} 2>/dev/null | grep 'time='",
        shell=True, capture_output=True, text=True
    ).stdout
    lats = []
    for line in out.splitlines():
        m = re.search(r'time=(\d+\.?\d*)', line)
        if m: lats.append(float(m.group(1)))
    return lats

def main():
    import re
    parser = argparse.ArgumentParser()
    parser.add_argument("--targets", default="8.8.8.8,1.1.1.1,208.67.222.222")
    parser.add_argument("--interval", type=int, default=5)
    parser.add_argument("--count", type=int, default=5)
    args = parser.parse_args()

    targets = args.targets.split(",")
    stats = defaultdict(list)

    print(f"\n📊 Latency Monitor (ping every {args.interval}s)")
    print("Press Ctrl+C to stop\n")
    print(f"{'Target':<15} {'Min':<8} {'Avg':<8} {'Max':<8} {'Jitter'}")
    print("─" * 50)

    try:
        while True:
            for target in targets:
                lats = adb_ping(target, args.count)
                if lats:
                    stats[target].extend(lats)
                    min_l = min(lats)
                    avg_l = statistics.mean(lats)
                    max_l = max(lats)
                    jitter = max_l - min_l
                    print(f"{target:<15} {min_l:<8.1f} {avg_l:<8.1f} {max_l:<8.1f} {jitter:.1f}ms")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    main()
