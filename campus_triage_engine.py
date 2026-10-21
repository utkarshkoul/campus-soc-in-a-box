#!/usr/bin/env python3
"""
Campus SOC-in-a-Box: Novelty Engine
-----------------------------------
Component: Campus-Specific Baseline + Explainable Alert Scoring + Daily Analyst Queue
Author: Campus SOC Team
Tech Stack: Python 3, OpenSearch / Wazuh alerts.json parser, Rich/HTML reporting

This module implements the core novelty of the project:
1. Baselines alerts against college operating hours and critical campus assets.
2. Generates an explainable risk score (0-100) detailing exactly why an alert is prioritized.
3. Groups incidents into a ready-to-triage Daily Analyst Queue (CLI & HTML).
"""

import json
import os
import sys
import datetime
from typing import List, Dict, Any

# ==============================================================================
# 1. CAMPUS CONTEXT CONFIGURATION & BASELINE
# ==============================================================================
CAMPUS_CONFIG = {
    # Working hours for standard lab operations (24-hour clock)
    "LAB_HOURS_START": 8,   # 08:00 AM
    "LAB_HOURS_END": 18,    # 06:00 PM

    # Criticality multiplier based on campus asset role
    "ASSET_CRITICALITY": {
        "192.168.56.10": {"role": "SOC-SIEM-Server", "multiplier": 1.5},
        "192.168.56.20": {"role": "Campus-Portal-Web-DB", "multiplier": 1.4},
        "192.168.56.30": {"role": "Lab-Student-PC-01", "multiplier": 1.0},
        "default": {"role": "General-Lab-Endpoint", "multiplier": 1.0}
    },

    # High-risk MITRE techniques that warrant automatic score elevation
    "CRITICAL_MITRE_TECHNIQUES": ["T1003.001", "T1486", "T1059.001", "T1098"]
}


class ExplainableScorer:
    """Calculates risk score and provides natural-language justifications."""

    def __init__(self, config: Dict[str, Any] = CAMPUS_CONFIG):
        self.config = config

    def score_alert(self, alert: Dict[str, Any]) -> Dict[str, Any]:
        """
        Takes raw Wazuh alert, applies campus baseline, and outputs explainable score.
        """
        explanations = []
        raw_level = alert.get("rule", {}).get("level", 5)
        base_score = min(raw_level * 5.0, 50.0)
        explanations.append(f"Base Wazuh severity level {raw_level} yields base score of {base_score:.1f}")

        # 1. Asset Criticality Multiplier
        agent_ip = alert.get("agent", {}).get("ip", "default")
        asset_info = self.config["ASSET_CRITICALITY"].get(agent_ip, self.config["ASSET_CRITICALITY"]["default"])
        multiplier = asset_info["multiplier"]
        adjusted_score = base_score * multiplier
        if multiplier > 1.0:
            explanations.append(f"Asset '{asset_info['role']}' ({agent_ip}) is high-value campus infra (+{(multiplier - 1.0)*100:.0f}% penalty)")

        # 2. Campus Operational Hours Baseline
        timestamp_str = alert.get("timestamp")
        is_off_hours = False
        try:
            if timestamp_str:
                # Handle ISO timestamps
                dt = datetime.datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                hour = dt.hour
                if hour < self.config["LAB_HOURS_START"] or hour >= self.config["LAB_HOURS_END"]:
                    is_off_hours = True
        except Exception:
            # Fallback to current time if unparseable
            hour = datetime.datetime.now().hour
            is_off_hours = hour < self.config["LAB_HOURS_START"] or hour >= self.config["LAB_HOURS_END"]

        if is_off_hours:
            adjusted_score += 18.0
            explanations.append(f"Activity occurred during off-hours (outside {self.config['LAB_HOURS_START']:02d}:00-{self.config['LAB_HOURS_END']:02d}:00) (+18 pts)")

        # 3. MITRE Technique Risk Elevation
        mitre_ids = alert.get("rule", {}).get("mitre", {}).get("id", [])
        if isinstance(mitre_ids, str):
            mitre_ids = [mitre_ids]

        matched_critical = [m for m in mitre_ids if m in self.config["CRITICAL_MITRE_TECHNIQUES"]]
        if matched_critical:
            adjusted_score += 20.0
            explanations.append(f"High-impact attack pattern matched: {', '.join(matched_critical)} (Credential Dump/Ransomware/PrivEsc) (+20 pts)")

        # Final normalization (Cap at 100)
        final_score = int(min(100, max(1, round(adjusted_score))))

        # Triage priority bucket
        if final_score >= 80:
            tier = "P1 - CRITICAL (Immediate Action)"
        elif final_score >= 60:
            tier = "P2 - HIGH (Investigate < 2 hrs)"
        elif final_score >= 35:
            tier = "P3 - MEDIUM (Daily Review)"
        else:
            tier = "P4 - LOW / Informational"

        return {
            "alert_id": alert.get("id", "N/A"),
            "timestamp": alert.get("timestamp", datetime.datetime.now().isoformat()),
            "rule_id": alert.get("rule", {}).get("id"),
            "description": alert.get("rule", {}).get("description", "Security Event"),
            "agent_name": alert.get("agent", {}).get("name", "Unknown-Host"),
            "agent_ip": agent_ip,
            "final_score": final_score,
            "tier": tier,
            "explainable_reason": " | ".join(explanations)
        }


# ==============================================================================
# 2. SYNTHETIC & LIVE LOG INGESTION
# ==============================================================================
def get_sample_alerts() -> List[Dict[str, Any]]:
    """Returns realistic campus alerts for demonstration when live SIEM is offline."""
    now = datetime.datetime.now()
    off_hours = (now.replace(hour=2, minute=30)).isoformat()
    work_hours = (now.replace(hour=11, minute=15)).isoformat()

    return [
        {
            "id": "1001",
            "timestamp": off_hours,
            "rule": {"id": 100111, "level": 14, "description": "CRITICAL: Potential LSASS process memory dump detected", "mitre": {"id": ["T1003.001"]}},
            "agent": {"name": "Campus-Lab-PC-01", "ip": "192.168.56.30"}
        },
        {
            "id": "1002",
            "timestamp": off_hours,
            "rule": {"id": 100102, "level": 10, "description": "Campus Server: SSH brute force attack detected", "mitre": {"id": ["T1110.001"]}},
            "agent": {"name": "Campus-Portal-Web", "ip": "192.168.56.20"}
        },
        {
            "id": "1003",
            "timestamp": work_hours,
            "rule": {"id": 100105, "level": 12, "description": "Campus Endpoint: Obfuscated PowerShell execution detected", "mitre": {"id": ["T1059.001"]}},
            "agent": {"name": "Campus-Lab-PC-01", "ip": "192.168.56.30"}
        },
        {
            "id": "1004",
            "timestamp": work_hours,
            "rule": {"id": 100118, "level": 8, "description": "Campus Lab Policy: Removable USB Mass Storage device plugged into lab workstation", "mitre": {"id": ["T1091"]}},
            "agent": {"name": "Campus-Lab-PC-01", "ip": "192.168.56.30"}
        },
        {
            "id": "1005",
            "timestamp": work_hours,
            "rule": {"id": 100101, "level": 8, "description": "Campus Recon: Port scanning activity detected across VLAN", "mitre": {"id": ["T1046"]}},
            "agent": {"name": "Campus-Portal-Web", "ip": "192.168.56.20"}
        }
    ]


def load_alerts(source_file: str = "/var/ossec/logs/alerts/alerts.json") -> List[Dict[str, Any]]:
    """Reads live alerts from Wazuh alerts.json if present; else loads synthetic sample alerts."""
    if os.path.exists(source_file):
        alerts = []
        with open(source_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        alerts.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        if alerts:
            return alerts
    return get_sample_alerts()


# Configure UTF-8 on Windows consoles if supported
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# ==============================================================================
# 3. DAILY ANALYST QUEUE GENERATOR (CLI & HTML)
# ==============================================================================
def render_cli_queue(scored_queue: List[Dict[str, Any]]):
    """Outputs a formatted CLI table for terminal review."""
    print("\n" + "="*95)
    print("[*] CAMPUS SOC-IN-A-BOX | DAILY ANALYST TRIAGE QUEUE (EXPLAINABLE SCORING)")
    print("="*95)
    print(f"{'PRIORITY':<28} | {'SCORE':<5} | {'HOST':<18} | {'ALERT DESCRIPTION':<36}")
    print("-" * 95)
    for item in scored_queue:
        print(f"{item['tier']:<28} | {item['final_score']:<5} | {item['agent_name']:<18} | {item['description'][:36]:<36}")
        print(f"  |-- Reason: {item['explainable_reason']}")
        print("-" * 95)


def generate_html_queue(scored_queue: List[Dict[str, Any]], output_path: str = "analyst_queue.html"):
    """Generates an analyst-ready web dashboard view."""
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Campus SOC - Daily Analyst Triage Queue</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #f8fafc; margin: 20px; }}
        h1 {{ color: #38bdf8; margin-bottom: 5px; }}
        .subtitle {{ color: #94a3b8; margin-bottom: 25px; }}
        table {{ width: 100%; border-collapse: collapse; background: #1e293b; border-radius: 8px; overflow: hidden; }}
        th, td {{ padding: 12px 16px; text-align: left; }}
        th {{ background: #334155; color: #cbd5e1; text-transform: uppercase; font-size: 12px; letter-spacing: 0.05em; }}
        tr:nth-child(even) {{ background: #1a2234; }}
        tr:hover {{ background: #2e3c54; }}
        .badge {{ padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 11px; }}
        .p1 {{ background: #ef4444; color: white; }}
        .p2 {{ background: #f97316; color: white; }}
        .p3 {{ background: #eab308; color: black; }}
        .p4 {{ background: #3b82f6; color: white; }}
        .score {{ font-weight: bold; font-size: 16px; }}
        .reason {{ color: #cbd5e1; font-size: 12px; margin-top: 4px; }}
    </style>
</head>
<body>
    <h1>Campus SOC-in-a-Box</h1>
    <div class="subtitle">Daily Analyst Queue with Explainable Alert Scoring & Campus Baselining • Generated {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>
    <table>
        <thead>
            <tr>
                <th>Severity Tier</th>
                <th>Score</th>
                <th>Endpoint</th>
                <th>Alert & Explainable Reason</th>
                <th>Timestamp</th>
            </tr>
        </thead>
        <tbody>
    """
    for item in scored_queue:
        tier_class = "p1" if "P1" in item["tier"] else ("p2" if "P2" in item["tier"] else ("p3" if "P3" in item["tier"] else "p4"))
        html_content += f"""
            <tr>
                <td><span class="badge {tier_class}">{item["tier"]}</span></td>
                <td class="score">{item["final_score"]}/100</td>
                <td><strong>{item["agent_name"]}</strong><br><small style="color:#64748b;">{item["agent_ip"]}</small></td>
                <td>
                    <strong>{item["description"]}</strong>
                    <div class="reason">💡 <em>{item["explainable_reason"]}</em></div>
                </td>
                <td style="color:#94a3b8; font-size:12px;">{item["timestamp"][:19]}</td>
            </tr>
        """
    html_content += """
        </tbody>
    </table>
</body>
</html>
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"\n[+] Interactive Web Dashboard generated: {os.path.abspath(output_path)}")


def main():
    scorer = ExplainableScorer()
    raw_alerts = load_alerts()
    scored_queue = [scorer.score_alert(a) for a in raw_alerts]

    # Sort descending by final risk score
    scored_queue.sort(key=lambda x: x["final_score"], reverse=True)

    # Render outputs
    render_cli_queue(scored_queue)
    generate_html_queue(scored_queue, output_path="analyst_queue.html")


if __name__ == "__main__":
    main()
