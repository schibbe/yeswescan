# Network Device Scanner

A user-friendly network scanner built with Python and Streamlit. Detects devices on your local network via ARP or ping, identifies vendors using a local OUI database, and compares scan results over time.

# Features

- ARP (with root) or ping-based scan fallback
- Device info: IP, MAC, hostname, vendor, device type
- Vendor detection using a local IEEE OUI database
- Heuristics-based type detection 
- Scan statistics & historical comparison
- Minimal logging with JSON output

# Project Structure

network-scanner/
├── app.py 
├── scanner.py
├── data/
│ └── oui.txt 
├── logo.png 
├── requirements.txt
└── README.md

# Requirements

Python 3.8+ and the following packages are required
-streamlit
-scapy
-pandas
-scikit-learn

Install dependencies:

```bash
pip install -r requirements.txt

# Usage 

Start the web app:

streamlit run app.py

Run the scanner manually (optional):

python scanner/scanner.py

On Linux/macOS, root privileges enable more precise ARP scanning:

sudo streamlit run app.py

# Output Sample

[
  {
    "ip": "192.168.0.12",
    "mac": "12:34:56:78:90:AB",
    "hostname": "raspberrypi.local",
    "last_seen": "2025-04-28 21:32:01"
  }
]


# Author

Built with curiosity for learning and showcasing security projects.
