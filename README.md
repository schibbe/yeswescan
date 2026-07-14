A lightweight network scanning tool to detect and identify devices on your local network.

# Motivation

I built this project to better understand how network discovery works in practice — how devices announce themselves on a local network and how that information can be used defensively, e.g. to spot unknown or unexpected devices.

# Demo

<img width="1440" height="900" alt="Bild12" src="https://github.com/user-attachments/assets/04fbe8f6-428e-4f76-9ffa-a025f3dfa205" />
*Scan your local network and see connected devices at a glance*

<img width="2880" height="1800" alt="Bild11" src="https://github.com/user-attachments/assets/dbb5b123-808e-4c6a-b3e9-502e9b87e288" />
*Detected devices with vendor and type identification*

# Features

- ARP (with root) or ping-based scan fallback
- Device info: IP, MAC, hostname, vendor, device type
- Vendor detection using a local IEEE OUI database
- Heuristics-based type detection 
- Scan statistics & historical comparison
- Minimal logging with JSON output

# Built With

Python 3.8+, Streamlit, Scapy, Pandas, Scikit-Learn

# Getting Started

Clone the repository and install the dependencies:
```
git clone https://github.com/schibbe/yeswescan.git
cd yeswescan
pip install -r requirements.txt
streamlit run app.py

On Linux/macOS, root privileges enable more precise ARP scanning:
sudo streamlit run app.py
```

# Project Structure

```
yeswescan/
├── app.py 
├── scanner.py
├── data/
│ └── oui.txt 
├── scanner/
│ └── keep.txt 
├── logo.png 
├── requirements.txt
└── README.md
```

# Output Sample

[
  {
    "ip": "192.168.0.12",
    "mac": "12:34:56:78:90:AB",
    "hostname": "raspberrypi.local",
    "last_seen": "2025-04-28 21:32:01"
  }
]

# What I Learned

- How ARP and ping-based network discovery work at a practical level
- Vendor identification via IEEE OUI databases
- Building a heuristics-based classification system
- Structuring a Python project for readability and reuse

# Disclaimer

This project is intended for use on networks you own or have explicit permission to scan. It is provided for demonstration and educational purposes only.

# About

Developed by Simon as part of a series of small projects exploring networking and security fundamentals.
