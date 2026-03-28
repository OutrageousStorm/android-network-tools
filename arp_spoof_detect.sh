#!/bin/bash
# arp_spoof_detect.sh -- Detect ARP spoofing on local network
# Usage: ./arp_spoof_detect.sh [gateway_ip]
# Watches for ARP table changes that might indicate spoofing
set -e

GW="${1:-192.168.1.1}"  # your gateway IP

echo "🛡️  ARP Spoofing Detector"
echo "Monitoring ARP table for suspicious changes..."
echo "Gateway: $GW\n"

adb shell "
arp -a | while read line; do
    echo \"\$line\"
done
" > /tmp/arp_baseline.txt

echo "Baseline captured. Monitoring for 1 minute..."
sleep 60

adb shell "
arp -a | while read line; do
    echo \"\$line\"
done
" > /tmp/arp_current.txt

diff /tmp/arp_baseline.txt /tmp/arp_current.txt && echo "✅ No changes (clean)" || echo "⚠️  Changes detected — possible spoofing"
