import scapy.all as scapy
import subprocess
import platform
import os
import json
import time
import socket

IP_RANGE = "192.168.0.0/24"
OUTPUT_FILE = "scanner/scanner_output.json"
STATISTICS_FILE = "scanner/statistics.json"

def has_root_privileges():
    return os.geteuid() == 0

def arp_scan(ip_range):
    arp_request = scapy.ARP(pdst=ip_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    devices = []
    for element in answered_list:
        ip = element[1].psrc
        mac = element[1].hwsrc
        devices.append({
            "ip": ip,
            "mac": mac,
            "last_seen": time.strftime("%Y-%m-%d %H:%M:%S"),
            "hostname": get_hostname(ip)
        })
    return devices

def ping_scan(ip_range):
    devices = []
    prefix = ".".join(ip_range.split(".")[:3])
    for i in range(1, 255):
        ip = f"{prefix}.{i}"
        param = "-n" if platform.system().lower() == "windows" else "-c"
        result = subprocess.run(['ping', param, '1', '-W', '1', ip], stdout=subprocess.DEVNULL)
        if result.returncode == 0:
            devices.append({
                "ip": ip,
                "mac": "unknown",
                "last_seen": time.strftime("%Y-%m-%d %H:%M:%S"),
                "hostname": get_hostname(ip)
            })
    return devices

def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return "unbekannt"

def scan(ip_range):
    if has_root_privileges():
        print("Root rights detected: ARP scan is used.")
        return arp_scan(ip_range)
    else:
        print("No root rights: Ping Scan is used.")
        return ping_scan(ip_range)

def save_devices(devices):
    with open(OUTPUT_FILE, "w") as f:
        json.dump(devices, f, indent=4)

def update_statistics(devices):
    if os.path.exists(STATISTICS_FILE):
        with open(STATISTICS_FILE, "r") as f:
            stats = json.load(f)
    else:
        stats = {"total_scans": 0, "total_devices": 0}

    stats["total_scans"] += 1
    stats["total_devices"] += len(devices)

    with open(STATISTICS_FILE, "w") as f:
        json.dump(stats, f, indent=4)

if __name__ == "__main__":
    try:
        devices = scan(IP_RANGE)
        save_devices(devices)
        update_statistics(devices)
    except Exception as e:
        print(f"Scan error: {e}")
