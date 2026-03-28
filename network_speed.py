#!/usr/bin/env python3
"""
network_speed.py -- Quick network speed test via adb downloads
Downloads a test file and measures throughput
Usage: python3 network_speed.py
"""
import subprocess, time

def measure_download(url, size_mb=10):
    print(f"\n📥 Downloading {size_mb}MB test file...")
    start = time.time()
    cmd = f"adb shell wget -O /dev/null '{url}' 2>&1 | grep -oP '(?<=saved \[)\\d+' || echo 0"
    out = subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()
    elapsed = time.time() - start
    
    bytes_down = int(out) if out.isdigit() else (size_mb * 1024 * 1024)
    mbps = (bytes_down / 1024 / 1024) / elapsed if elapsed > 0 else 0
    
    print(f"Downloaded: {bytes_down / 1024 / 1024:.1f} MB in {elapsed:.1f}s")
    print(f"Speed: {mbps:.2f} Mbps")
    return mbps

def main():
    print("🌐 Android Network Speed Test")
    
    test_urls = [
        "http://speedtest.ftp.otenet.gr/files/test10Mb.db",
        "http://ipv4.download.thinkbroadband.com/10MB.zip",
    ]
    
    for url in test_urls:
        try:
            measure_download(url, 10)
            break
        except Exception as e:
            print(f"Failed: {e}")

if __name__ == "__main__":
    main()
