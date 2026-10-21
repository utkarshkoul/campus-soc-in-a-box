#!/usr/bin/env python3
"""
Campus SOC-in-a-Box: Safe Attack Simulator
------------------------------------------
Purpose: Safely generates telemetry and triggers the 20 detection rules across:
  - Linux Campus Server (VM 2: 192.168.56.20)
  - Windows Campus Lab PC (VM 3: 192.168.56.30)
"""

import sys
import os
import time
import socket
import subprocess

def test_ssh_bruteforce(target_ip="192.168.56.20", attempts=7):
    """Simulates rapid SSH connection attempts to trigger Rule 100102."""
    print(f"\n[*] [TEST 1] Simulating SSH Brute-Force against {target_ip}:22...")
    for i in range(1, attempts + 1):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.0)
            s.connect((target_ip, 22))
            # Send bogus SSH handshake to register authentication failure
            s.sendall(b"SSH-2.0-CampusTestClient_BogusAuth\r\n")
            s.close()
            print(f"  [+] Attempt {i}/{attempts} sent to port 22.")
        except Exception as e:
            print(f"  [-] Connection {i} failed: {e}")
        time.sleep(0.4)
    print("  ==> Expected Alert: Rule 100102 (SSH Brute Force Detected)")


def test_port_scan(target_ip="192.168.56.20"):
    """Simulates TCP port sweep to trigger Zeek / Wazuh Rule 100101."""
    print(f"\n[*] [TEST 2] Simulating Port Scan against {target_ip}...")
    common_ports = [21, 22, 23, 25, 80, 110, 139, 443, 445, 1433, 3306, 3389, 8080]
    for p in common_ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.2)
            s.connect_ex((target_ip, p))
            s.close()
        except Exception:
            pass
    print("  ==> Expected Alert: Rule 100101 (Port Scan via Zeek conn.log)")


def test_web_path_traversal(target_ip="192.168.56.20"):
    """Sends directory traversal HTTP probes to trigger Rule 100104."""
    print(f"\n[*] [TEST 3] Simulating Directory Traversal on http://{target_ip}...")
    traversal_payload = b"GET /../../../../etc/passwd HTTP/1.1\r\nHost: campus-portal\r\n\r\n"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)
        s.connect((target_ip, 80))
        s.sendall(traversal_payload)
        s.close()
        print("  [+] Sent path traversal payload.")
    except Exception as e:
        print(f"  [-] Web test notice: {e}")
    print("  ==> Expected Alert: Rule 100104 (Web Traversal Probe)")


def print_windows_simulation_commands():
    """Prints copy-pasteable PowerShell commands for testing on VM 3 (Windows Client)."""
    print("""
================================================================================
[*] WINDOWS CLIENT TEST COMMANDS (Run these inside PowerShell on VM 3)
================================================================================
1. Test Rule 100105 (Obfuscated PowerShell Execution):
   powershell.exe -w hidden -nop -enc RwBlAHQALQBEAGEAdABlAA==

2. Test Rule 100106 (Living-off-the-land Certutil download):
   certutil.exe -urlcache -split -f http://192.168.56.20/test.txt C:\\Users\\Public\\test.txt

3. Test Rule 100108 (Scheduled Task Persistence):
   schtasks.exe /create /tn "CampusUpdateCheck" /tr "notepad.exe" /sc daily /st 09:00

4. Test Rule 100119 (Canary Ransomware Simulation):
   mkdir C:\\Campus_Canary -ErrorAction SilentlyContinue
   "This is a canary trap document" | Out-File C:\\Campus_Canary\\budget_2026.docx.locked

5. Test Rule 100111 (Atomic Red Team T1003.001 LSASS Simulation):
   rundll32.exe C:\\windows\\System32\\comsvcs.dll, MiniDump (Get-Process lsass).Id C:\\Temp\\lsass.dmp full
================================================================================
""")


def main():
    print("=" * 80)
    print("🎓 CAMPUS SOC-IN-A-BOX | ATTACK & TELEMETRY SIMULATOR")
    print("=" * 80)
    print("1. Network & Linux Server Tests (from Host / Attacker VM)")
    test_port_scan()
    test_ssh_bruteforce()
    test_web_path_traversal()

    print_windows_simulation_commands()

if __name__ == "__main__":
    main()
