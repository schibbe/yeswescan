import streamlit as st
import json
import os
import time
import socket
import subprocess
import re

def is_localhost():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip.startswith("127.") or local_ip.startswith("192.168.") or "local" in hostname

LOGO_PATH = "logo.png"  
OUI_PATH = "data/oui.txt"

def load_scanner_data():
    if os.path.exists('scanner/scanner_output.json'):
        with open('scanner/scanner_output.json') as f:
            return json.load(f)
    else:
        return []

def load_statistics():
    if os.path.exists('scanner/statistics.json'):
        with open('scanner/statistics.json') as f:
            return json.load(f)
    else:
        return {"total_scans": 0, "total_devices": 0}

def load_oui_data(filepath=OUI_PATH):
    oui_map = {}
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                match = re.match(r"^([0-9A-Fa-f]{6})\s+\(base 16\)\s+(.+)$", line.strip())
                if match:
                    prefix, vendor = match.groups()
                    oui_map[prefix.upper()] = vendor.strip()
    return oui_map

def lookup_vendor(mac, oui_data=None):
    if mac == "unknown" or not mac:
        return "unknown"
    if oui_data is None:
        oui_data = load_oui_data()
    mac_prefix = mac.upper().replace(":", "")[:6]
    return oui_data.get(mac_prefix, "unknown")

def get_device_type(mac, hostname):
    if not mac:
        return "unknown"
    mac = mac.upper().replace(":", "")
    hostname = hostname.lower()

    if "iphone" in hostname or mac.startswith("FCA667") or mac.startswith("00163E"):
        return "Smartphone"
    elif "ipad" in hostname:
        return "Tablet"
    elif "android" in hostname or "galaxy" in hostname:
        return "Smartphone"
    elif "macbook" in hostname or mac.startswith("F4F5DB"):
        return "Laptop"
    elif "desktop" in hostname or "win" in hostname or mac.startswith("D8CB8A"):
        return "PC"
    elif "echo" in hostname or "googlehome" in hostname:
        return "Smart Speaker"
    elif "tv" in hostname or "chromecast" in hostname:
        return "Smart TV"
    elif "raspberry" in hostname or mac.startswith("B827EB"):
        return "IoT / Raspberry Pi"
    else:
        return "unknown"

def resolve_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return "Unbekannt"

def run_scan():
    subprocess.run(["python3", "scanner/scanner.py"])

def compare_with_previous(devices):
    if os.path.exists("scanner/last_devices.json"):
        with open("scanner/last_devices.json") as f:
            old = json.load(f)
        old_ips = {d["ip"] for d in old}
        new_ips = {d["ip"] for d in devices}
        added = new_ips - old_ips
        removed = old_ips - new_ips
        if added:
            st.warning(f"new devices detected: {', '.join(added)}")
        if removed:
            st.error(f"Devices no longer visible: {', '.join(removed)}")
    with open("scanner/last_devices.json", "w") as f:
        json.dump(devices, f, indent=4)

def main():
    st.set_page_config(page_title="Your Trusty Network Scanner", layout="wide")

    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=200)

    st.title("Your Trusty Network Scanner")
    st.info("Note: MAC addresses may not be visible without root rights.")

    if is_localhost():
        if st.button("Yes We Scan!"):
            with st.spinner('running...'):
                run_scan()
                time.sleep(2)
            st.success('Done!')
    else:
        st.warning("Scanning is disabled in hosted/cloud environments.")

    devices = load_scanner_data()
    stats = load_statistics()
    oui_data = load_oui_data()

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Total scans", value=stats.get("total_scans", 0))
    with col2:
        st.metric(label="Detected devices", value=len(devices))

    compare_with_previous(devices)

    st.divider()

    st.subheader("Detected devices")
    if devices:
        for device in devices:
            ip = device.get("ip", "unknown")
            mac = device.get("mac", "unknown")
            hostname = device.get("hostname") or resolve_hostname(ip)
            vendor = lookup_vendor(mac, oui_data)
            last_seen = device.get("last_seen", "unbekannt")
            device_type = device.get("device_type") or get_device_type(mac, hostname)

            st.write(f"• IP: `{ip}`, MAC: `{mac}`, vendor: `{vendor}`, name: `{hostname}`, device type: `{device_type}`, last seen: `{last_seen}`")
    else:
        st.info("No devices detected yet.")

if __name__ == "__main__":
    main()
