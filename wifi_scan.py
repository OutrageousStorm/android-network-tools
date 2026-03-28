#!/usr/bin/env python3
"""
wifi_scan.py -- Scan and monitor Wi-Fi from connected Android device
Shows SSID, BSSID, signal, frequency for all visible networks.
Usage: python3 wifi_scan.py [--watch]
"""
import subprocess, re, argparse, time, os

def adb(cmd):
    return subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True, text=True).stdout

def scan():
    raw = adb("dumpsys wifi | grep 'SSID\\|BSSID\\|level\\|freq'")
    networks = []
    current = {}
    for line in raw.splitlines():
        line = line.strip()
        ssid_m = re.search(r'SSID: "?([^",\n]+)"?', line)
        bssid_m = re.search(r'BSSID: ([\da-f:]{17})', line, re.IGNORECASE)
        level_m = re.search(r'level: (-\d+)', line)
        freq_m  = re.search(r'frequency: (\d+)', line)

        if ssid_m and ssid_m.group(1).strip():
            if current: networks.append(dict(current))
            current = {'ssid': ssid_m.group(1).strip()}
        if bssid_m: current['bssid'] = bssid_m.group(1)
        if level_m: current['level'] = int(level_m.group(1))
        if freq_m:  current['freq'] = int(freq_m.group(1))

    if current: networks.append(current)
    return [n for n in networks if n.get('ssid') and n.get('bssid')]

def signal_bar(level):
    if level >= -50: return "████ Excellent"
    if level >= -60: return "███░ Good"
    if level >= -70: return "██░░ Fair"
    return "█░░░ Weak"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--watch", action="store_true", help="Refresh continuously")
    args = parser.parse_args()

    def show():
        if args.watch:
            os.system("clear")
        nets = scan()
        print(f"📶 Wi-Fi Networks ({len(nets)} visible)\n")
        print(f"{'SSID':<30} {'BSSID':<20} {'dBm':<6} {'GHz':<6} Signal")
        print("─" * 80)
        for n in sorted(nets, key=lambda x: x.get('level', -100), reverse=True):
            ghz = f"{n.get('freq',0)/1000:.1f}" if n.get('freq') else "?"
            print(f"{n.get('ssid','?'):<30} {n.get('bssid','?'):<20} "
                  f"{n.get('level','?'):<6} {ghz:<6} {signal_bar(n.get('level',-100))}")

    if args.watch:
        print("Watching Wi-Fi networks (Ctrl+C to stop)...")
        try:
            while True:
                show()
                time.sleep(5)
        except KeyboardInterrupt:
            pass
    else:
        show()

if __name__ == "__main__":
    main()
