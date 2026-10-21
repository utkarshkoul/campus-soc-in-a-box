# Project 01: Campus SOC-in-a-Box for Small Institutions
> **SOC • Monitoring & Incident Response Prototype**  
> *Multidisciplinary Course (MDC) Project*

---

## 📌 Executive Summary
Small academic institutions and colleges often lack the budget for 24x7 enterprise commercial SOC solutions (like Splunk or CrowdStrike Falcon), which cost upwards of \$100,000 annually. 

**Campus SOC-in-a-Box** delivers a lightweight, production-grade security operations center utilizing open-source telemetry and correlation rules:
* **Central SIEM**: Wazuh Manager, Indexer (OpenSearch), and Web Dashboard.
* **Endpoint Telemetry**: Microsoft Sysmon (System Monitor) with SwiftOnSecurity profile.
* **Network Telemetry**: Zeek Network Security Monitor for packet metadata inspection.
* **Core Novelty**: A Python-based **Explainable Alert Scoring Engine** and **Daily Analyst Triage Queue** tailored to campus operational baselines.

---

## 🧠 The Project Novelty: Explainable AI Alert Scoring
Traditional SIEM solutions inundate student/junior analysts with thousands of uncontextualized raw alerts. This prototype introduces a custom scoring heuristic:

$$\text{Final Score} = \min\Big(100, (\text{Wazuh Level} \times 5) \times \text{Asset Multiplier} + \text{Off-Hours Penalty} + \text{MITRE Elevation}\Big)$$

### Explainability Output Sample:
```text
Priority: P1 - CRITICAL (Score: 88/100)
Host: Campus-Lab-PC-01 (192.168.56.30)
Alert: Potential LSASS process memory dump detected (MITRE T1003.001)
Explainable Reason: Base Wazuh severity level 14 yields base score of 50.0 | Activity occurred during off-hours (outside 08:00-18:00) (+18 pts) | High-impact attack pattern matched: T1003.001 (+20 pts)
```

---

## 🛠️ Architecture & Components
1. **VM 1: SOC SIEM Server (Ubuntu Server)**
   * Wazuh All-in-One Manager, Indexer, and Dashboard.
   * Host IP: `192.168.101.134` (Port 443 / Port 1514).
2. **VM 2: Campus Linux Web Server & Network Sensor (Ubuntu Server)**
   * Hosts student portal on Apache2 (Port 80) and SSH (Port 22).
   * Runs Zeek IDS capturing `conn.log`, `dns.log`, and `http.log`.
3. **VM 3: Campus Windows Client (Windows 10/11 Endpoint)**
   * Runs Microsoft Sysmon capturing process creation (Event 1), network connections (Event 3), and LSASS memory access (Event 10).
   * Wazuh Agent forwarding telemetry to VM 1.

---

## 📂 Repository Contents
* [`campus_triage_engine.py`](campus_triage_engine.py): The Python explainable scoring engine.
* [`index.html`](index.html) / [`analyst_queue.html`](analyst_queue.html): Interactive Daily Analyst Triage Queue dashboard.
* [`local_rules.xml`](local_rules.xml): 20 custom detection rules mapped to MITRE ATT&CK.
* [`simulate_attacks.py`](simulate_attacks.py): Automated attack simulation script for safe testing.
* [`incident_triage_runbook.md`](incident_triage_runbook.md): Standard Operating Procedure (SOP) for Tier-1 analysts.

---

## 🚀 Live Demo & Web Prototype
Open [`index.html`](index.html) directly in any web browser to view the interactive prototype and analyst queue.
