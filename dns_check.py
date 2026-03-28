#!/usr/bin/env python3
"""
dns_check.py -- Detect DNS hijacking and test resolution
Usage: python3 dns_check.py
Shows: device DNS servers, test resolution, detects hijacking
"""
import subprocess, re, socket

def adb(cmd):
    r = subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True, text=True)
    return r.stdout.strip()

def get_dns_servers():
    out = adb("getprop net.dns1 && getprop net.dns2 && getprop net.dns3")
    return [l for l in out.splitlines() if l]

def test_resolution(domain):
    out = adb(f"nslookup {domain} 8.8.8.8 2>/dev/null | grep 'Address'")
    ips = re.findall(r'(\d+\.\d+\.\d+\.\d+)', out)
    return ips

def check_hijacking():
    print("\n🔍 DNS Hijacking Check")
    print("=" * 50)
    
    # Query known domains that should NOT resolve
    tests = [
        ("nonexistent.test", None),  # should fail
        ("google.com", ["142.250"]),  # should return Google IP
        ("cloudflare.com", ["104.16"]),  # should return CF IP
    ]
    
    suspicious = False
    for domain, expected_prefixes in tests:
        ips = test_resolution(domain)
        if not expected_prefixes:
            if ips:
                print(f"  ⚠️  {domain} resolved when it shouldn't: {ips}")
                suspicious = True
        else:
            if not ips:
                print(f"  ⚠️  {domain} didn't resolve")
                suspicious = True
            elif not any(ip.startswith(p) for ip in ips for p in expected_prefixes):
                print(f"  ⚠️  {domain} resolved to unexpected IP: {ips}")
                suspicious = True
    
    if suspicious:
        print("\n  ⚠️  DNS HIJACKING DETECTED")
    else:
        print("\n  ✅ DNS looks clean")

def main():
    print("📡 Android DNS Checker")
    print("=" * 50)
    
    dns = get_dns_servers()
    print(f"\nDNS servers on device:")
    for i, d in enumerate(dns, 1):
        print(f"  {i}. {d}")
    
    check_hijacking()

if __name__ == "__main__":
    main()
