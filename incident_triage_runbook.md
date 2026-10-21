# Incident Triage Runbook: Campus SOC-in-a-Box
**Standard Operating Procedure (SOP) for Student Tier-1 SOC Analysts**  
*Project Deliverable: Campus SOC Incident Response Framework*

---

## 1. Objective & Scope
This runbook provides student and junior SOC analysts with a standardized, explainable procedure to triage, investigate, contain, and remediate alerts generated across the campus network (academic servers, student lab PCs, and network perimeters).

---

## 2. Standard Triage Flowchart (The 4-Step Lifecycle)

```
[ Alert Arrives in Daily Queue ]
                │
                ▼
        [ Phase 1: Verification & Context Check ]
        - Check Explainable Score (P1/P2/P3/P4)
        - Validate Host Role & Operational Hours
        - Correlate with Zeek / Sysmon Event IDs
                │
         Is it True Positive?
        ├── NO  ──► Document as False Positive & Tune Wazuh Rule
        └── YES ──► Proceed to Containment
                │
                ▼
        [ Phase 2: Rapid Containment ]
        - Network Isolation via Wazuh Active Response
        - Terminate Malicious Process Trees
                │
                ▼
        [ Phase 3: Eradication & Recovery ]
        - Delete Artifacts, Scheduled Tasks, or Web Shells
        - Invalidate Compromised Credentials
                │
                ▼
        [ Phase 4: Post-Incident Documentation ]
        - Update Incident Ticket & Campus Baseline
```

---

## 3. High-Priority Playbooks

### Playbook A: Credential Dumping / LSASS Memory Access (Rule 100111 / T1003.001)
* **Severity**: `P1 - CRITICAL` (Score: 85–100)
* **Trigger**: Sysmon Event ID 10 targeting `lsass.exe` with suspicious `GrantedAccess` masks (e.g., `0x1010`, `0x1438`).
* **Step 1: Verification**:
  1. Open Wazuh Dashboard -> Search `rule.id: 100111`.
  2. Inspect `win.eventdata.sourceImage`. Is it legitimate campus IT administrative tooling (e.g., Antivirus scanner) or an unknown binary / `rundll32.exe` / `powershell.exe`?
* **Step 2: Containment**:
  1. Immediately isolate the workstation from the campus VLAN using Wazuh Active Response:
     ```bash
     /var/ossec/bin/agent_control -b <IP_ADDRESS> -u <AGENT_ID>
     ```
  2. Block the host on the switch or hypervisor network.
* **Step 3: Eradication**:
  1. Kill the source PID identified in the alert.
  2. Force a password reset for all domain/local accounts that were logged into that workstation.
  3. Search the system for dumped files (e.g., `*.dmp`, `*.kirbi`, `lsass.dmp`).

---

### Playbook B: SSH / RDP Brute-Force on Campus Server (Rule 100102 / 100103)
* **Severity**: `P2 - HIGH` (Elevates to `P1` if during off-hours or targeting critical servers)
* **Trigger**: Multiple failed authentication attempts within a short timeframe.
* **Step 1: Verification**:
  1. Verify if the source IP belongs to the internal campus DHCP pool, student Wi-Fi, or an external unauthorized IP.
  2. Check if any subsequent **successful** logon (Linux `sshd: Accepted` or Windows Event ID 4624) followed the failures.
* **Step 2: Containment**:
  1. If failures are ongoing: Automatically trigger `firewalld` or `iptables` drop via Wazuh Active Response.
  2. If an authentication succeeded after brute-forcing: Assume account takeover. Lock the target user account immediately:
     ```bash
     sudo passwd -l <username>
     ```
* **Step 3: Remediation**:
  1. Enforce SSH key-only authentication on Linux servers (`PasswordAuthentication no`).
  2. Restrict RDP to administrative subnets or require VPN + MFA.

---

### Playbook C: Living-off-the-Land (LotL) / Obfuscated PowerShell (Rule 100105 / 100106)
* **Severity**: `P2 - HIGH`
* **Trigger**: `powershell.exe` executed with `-enc`, `-w hidden`, or `certutil -urlcache`.
* **Step 1: Verification**:
  1. Decode base64 payload from `win.eventdata.commandLine`:
     ```powershell
     [System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String("ENCODED_STRING"))
     ```
  2. Identify URLs accessed, files created, or child processes spawned.
* **Step 2: Containment & Eradication**:
  1. Kill parent and child processes.
  2. Delete files downloaded into `C:\Users\Public\` or `C:\Temp\`.
  3. Check Windows Task Scheduler (`schtasks /query /fo LIST /v`) for persistence.

---

## 4. Incident Escalation & Triage Matrix

| Score Tier | Action Required | Escalation Window | Responsible Role |
| :--- | :--- | :--- | :--- |
| **P1 (80 - 100)** | Isolate endpoint, notify campus IT lead, begin memory dump. | **< 15 minutes** | Tier-1 Lead + Faculty Admin |
| **P2 (60 - 79)** | Investigate process tree, verify parent/child, check network traffic. | **< 2 hours** | Tier-1 Analyst |
| **P3 (35 - 59)** | Review daily log batch, correlate repeated attempts. | **Daily Queue** | Junior Student Analyst |
| **P4 (1 - 34)** | Informational / Policy anomaly (e.g., student plugged in standard USB). | **Weekly Audit** | Automated Archival |
