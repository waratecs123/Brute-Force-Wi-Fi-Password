# WiFi BruteForce Tool  

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)  
![License](https://img.shields.io/badge/License-MIT-green)  
![Platform](https://img.shields.io/badge/Platform-Windows%2FLinux-lightgrey)  

A Python-based WiFi brute-force tool designed for educational purposes and penetration testing. This application attempts to connect to a target WiFi network by generating and testing random passwords of a specified length.  

**Disclaimer:** This tool is intended for legal security testing and ethical hacking only. Unauthorized access to networks is illegal. Use responsibly and only on networks you own or have permission to test.  

---

## Features  

- **Random password generation** using customizable character sets (letters, numbers, symbols).  
- **Real-time statistics** including attempts, speed (attempts/sec), and current password.  
- **Interactive GUI** built with Tkinter for easy control and monitoring.  
- **Multi-platform support** (Windows/Linux, requires `pywifi` compatibility).  
- **Logging system** to track progress and results.  

---

## Installation  

### Prerequisites  
- Python 3.x  
- `pywifi` library  
- Tkinter (usually included with Python)  

### Steps  
1. Clone the repository:  
   ```bash
   git clone https://github.com/yourusername/wifi-bruteforce-tool.git
   cd wifi-bruteforce-tool
