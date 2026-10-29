import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 widescreen
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Theme Colors
    BG_DARK = RGBColor(15, 23, 42)       # Slate 900
    CARD_BG = RGBColor(30, 41, 59)       # Slate 800
    CARD_BORDER = RGBColor(51, 65, 85)   # Slate 700
    TEXT_LIGHT = RGBColor(248, 250, 252) # Slate 50
    TEXT_MUTED = RGBColor(148, 163, 184) # Slate 400
    ACCENT_CYAN = RGBColor(14, 165, 233) # Sky 500
    ACCENT_TEAL = RGBColor(20, 184, 166) # Teal 500
    ACCENT_RED = RGBColor(239, 68, 68)   # Red 500
    ACCENT_GOLD = RGBColor(234, 179, 8)  # Amber 500

    def add_header(slide, title_text, category_text="CAMPUS SOC-IN-A-BOX | PROJECT 01"):
        # Category / Tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_CYAN

        # Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.8))
        tf_t = t_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(24)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_LIGHT

    def set_slide_background(slide):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = BG_DARK

    def add_card(slide, left, top, width, height, title, body_bullets, accent_color=ACCENT_CYAN, badge=None):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = CARD_BG
        shape.line.color.rgb = CARD_BORDER
        shape.line.width = Pt(1.5)

        tf = shape.text_frame
        tf.vertical_anchor = MSO_ANCHOR.TOP
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.25)
        tf.margin_bottom = Inches(0.25)

        p_title = tf.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(16)
        p_title.font.bold = True
        p_title.font.color.rgb = accent_color
        p_title.space_after = Pt(10)

        for b in body_bullets:
            p = tf.add_paragraph()
            p.text = "• " + b
            p.font.size = Pt(12)
            p.font.color.rgb = TEXT_LIGHT
            p.space_after = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 1: TITLE SLIDE
    # -------------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1)

    # Accent decorative bar
    bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(0.15), Inches(3.8))
    bar.fill.solid()
    bar.fill.fore_color.rgb = ACCENT_CYAN
    bar.line.fill.background()

    # Title box
    tbox = slide1.shapes.add_textbox(Inches(1.2), Inches(1.7), Inches(11.0), Inches(3.8))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "CAMPUS CYBERSECURITY MONITORING"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_CYAN
    p0.space_after = Pt(8)

    p1 = tf1.add_paragraph()
    p1.text = "Campus SOC-in-a-Box for Small Institutions"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_LIGHT
    p1.space_after = Pt(12)

    p2 = tf1.add_paragraph()
    p2.text = "A Lightweight, Zero-Licensing Security Operations Center with Explainable AI Alert Triage"
    p2.font.size = Pt(18)
    p2.font.color.rgb = TEXT_MUTED
    p2.space_after = Pt(30)

    p3 = tf1.add_paragraph()
    p3.text = "Presenter: Utkarsh Koul  |  Multidisciplinary Course (MDC) Project  |  2026"
    p3.font.size = Pt(14)
    p3.font.bold = True
    p3.font.color.rgb = ACCENT_TEAL

    # -------------------------------------------------------------
    # SLIDE 2: THE PROBLEM (WHY SMALL COLLEGES GET HACKED)
    # -------------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_header(slide2, "The Real Problem: Why Small Colleges Suffer Cyber Attacks")

    add_card(slide2, Inches(0.8), Inches(1.7), Inches(3.6), Inches(5.1),
             "1. The $100k Cost Barrier", [
                 "Enterprise security platforms (Splunk, CrowdStrike) cost upwards of $100,000/year.",
                 "Small colleges, polytechnics, and regional institutions have zero budget for commercial tooling.",
                 "Result: Campus servers and student portals run completely unmonitored."
             ], ACCENT_RED)

    add_card(slide2, Inches(4.8), Inches(1.7), Inches(3.6), Inches(5.1),
             "2. No 24x7 Security Staff", [
                 "Cyber attackers don't attack at 2 PM; they strike at 3 AM on weekends when labs are closed.",
                 "Colleges cannot afford round-the-clock specialized cybersecurity engineers.",
                 "Attacks go completely unnoticed for weeks until ransomware strikes or data is leaked."
             ], ACCENT_GOLD)

    add_card(slide2, Inches(8.8), Inches(1.7), Inches(3.6), Inches(5.1),
             "3. The 'Alert Flood' Trap", [
                 "Even if free tools are installed, they generate 10,000+ raw computer logs daily.",
                 "Student interns or junior IT staff face massive 'Alert Fatigue'.",
                 "They have no automated way to separate trivial false alarms from critical campus data breaches."
             ], ACCENT_CYAN)

    # -------------------------------------------------------------
    # SLIDE 3: THE CONCEPT (CCTV ANALOGY FOR NON-TECH TEACHERS)
    # -------------------------------------------------------------
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3)
    add_header(slide3, "The Concept: What is a 'SOC-in-a-Box'?")

    add_card(slide3, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1),
             "The Campus Security Analogy (CCTV)", [
                 "CCTV Cameras everywhere -> In our project, Sysmon & Zeek act as digital cameras monitoring computers and Wi-Fi networks.",
                 "Central Control Room -> Wazuh SIEM acts as the central security room displaying all monitors on one single dashboard.",
                 "Security Guards on Patrol -> Our Python Triage Engine automatically flags the most dangerous events for human review.",
                 "Standard Operating Procedure (SOP) -> Our Incident Triage Runbook tells students exactly what to do when an alarm rings."
             ], ACCENT_CYAN)

    add_card(slide3, Inches(6.8), Inches(1.7), Inches(5.6), Inches(5.1),
             "Why 'In-a-Box'?", [
                 "Packaged into a single, compact, virtualized lab that runs on existing commodity college hardware.",
                 "Hardware Requirement: Runs completely on 8 to 12 GB RAM laptops or existing college lab desktops.",
                 "Zero Software Licensing Cost: 100% powered by open-source, battle-tested security technologies.",
                 "Turnkey Deployment: Can be replicated by any academic department in less than an hour."
             ], ACCENT_TEAL)

    # -------------------------------------------------------------
    # SLIDE 4: SYSTEM ARCHITECTURE (THE 3-MACHINE LAB)
    # -------------------------------------------------------------
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4)
    add_header(slide4, "System Architecture: Our 3-Machine Virtual Lab")

    add_card(slide4, Inches(0.8), Inches(1.7), Inches(3.6), Inches(5.1),
             "VM 1: SOC Command Center", [
                 "Role: Central SIEM & Intelligence Hub",
                 "OS: Ubuntu Server (IP: 192.168.101.134)",
                 "Wazuh Manager: Evaluates 20 custom detection rules in real-time.",
                 "Wazuh Indexer & Dashboard: Stores logs and visualizes threat maps.",
                 "Python Novelty Engine: Scores and ranks alerts for human analysts."
             ], ACCENT_CYAN)

    add_card(slide4, Inches(4.8), Inches(1.7), Inches(3.6), Inches(5.1),
             "VM 2: Campus Linux Server", [
                 "Role: Simulated Student Portal & Sensor",
                 "OS: Ubuntu Server (IP: 192.168.101.135)",
                 "Apache Web Server: Simulates student grades & attendance portal.",
                 "Zeek Network IDS: Sniffs network packets for stealth port scans and password leaks.",
                 "Wazuh Agent: Streams server logs to VM 1."
             ], ACCENT_TEAL)

    add_card(slide4, Inches(8.8), Inches(1.7), Inches(3.6), Inches(5.1),
             "VM 3: Student Lab Workstation", [
                 "Role: Monitored Windows Campus Client",
                 "OS: Windows 10/11 Endpoint",
                 "Microsoft Sysmon: Deep process creation, command line, and memory monitoring.",
                 "SwiftOnSecurity Profile: Filters out normal noise to catch true malware.",
                 "Wazuh Windows Agent: Encrypted log forwarding on TCP port 1514."
             ], ACCENT_GOLD)

    # -------------------------------------------------------------
    # SLIDE 5: THE TECHNOLOGY STACK (EXPLAINED SIMPLY)
    # -------------------------------------------------------------
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5)
    add_header(slide5, "The Technology Stack: Explained in Plain English")

    add_card(slide5, Inches(0.8), Inches(1.7), Inches(5.6), Inches(2.4),
             "1. Wazuh SIEM (The Central Brain)", [
                 "Free, enterprise-grade Security Information & Event Management engine.",
                 "Correlates millions of events across all campus computers and triggers alarms."
             ], ACCENT_CYAN)

    add_card(slide5, Inches(6.8), Inches(1.7), Inches(5.6), Inches(2.4),
             "2. Microsoft Sysmon (The Windows Bodyguard)", [
                 "Monitors deep Windows activities: hidden processes, command line scripts, and RAM.",
                 "Catches stealthy hacker tools that normal free antiviruses completely miss."
             ], ACCENT_TEAL)

    add_card(slide5, Inches(0.8), Inches(4.4), Inches(5.6), Inches(2.4),
             "3. Zeek IDS (The Network Watchdog)", [
                 "Passive network traffic inspector that monitors college Wi-Fi & VLAN packets.",
                 "Detects port scans, DNS tunneling, and plaintext student passwords over HTTP."
             ], ACCENT_GOLD)

    add_card(slide5, Inches(6.8), Inches(4.4), Inches(5.6), Inches(2.4),
             "4. Python 3 (The Intelligence Scorer)", [
                 "Our custom-built Novelty Engine that sits on top of the SIEM.",
                 "Calculates college-specific risk scores and generates an explainable daily queue."
             ], ACCENT_RED)

    # -------------------------------------------------------------
    # SLIDE 6: 20 DETECTION RULES (WHAT THREATS CAN IT CATCH?)
    # -------------------------------------------------------------
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6)
    add_header(slide6, "The 20 Custom Detection Rules: What Can It Catch?")

    add_card(slide6, Inches(0.8), Inches(1.7), Inches(2.7), Inches(5.1),
             "Reconnaissance", [
                 "Rule 1: Stealth Port Scanning across campus VLAN (Zeek).",
                 "Rule 4: Web directory traversal on student portal (trying to view /etc/passwd).",
                 "Rule 15: DNS Tunneling and abnormal query spikes."
             ], ACCENT_CYAN)

    add_card(slide6, Inches(3.7), Inches(1.7), Inches(2.7), Inches(5.1),
             "Brute-Force & Creds", [
                 "Rule 2: SSH password brute-force attack on server.",
                 "Rule 3: Repeated Windows RDP failed logins.",
                 "Rule 11: CRITICAL Mimikatz / LSASS password dumping from memory.",
                 "Rule 20: Plaintext password exposure over HTTP."
             ], ACCENT_GOLD)

    add_card(slide6, Inches(6.6), Inches(1.7), Inches(2.7), Inches(5.1),
             "Execution & LotL", [
                 "Rule 5: Obfuscated, hidden base64 PowerShell scripts.",
                 "Rule 6: Certutil download abuse (Living-off-the-Land).",
                 "Rule 7: Script execution from C:\\Users\\Public or Temp.",
                 "Rule 14: PsExec lateral movement inside the lab."
             ], ACCENT_TEAL)

    add_card(slide6, Inches(9.5), Inches(1.7), Inches(2.7), Inches(5.1),
             "Persistence & Campus", [
                 "Rule 8: Unauthorized scheduled task creation.",
                 "Rule 9: Adding rogue users to Local Administrators.",
                 "Rule 17: Admin login outside lab hours (1 AM - 5 AM).",
                 "Rule 18: Unauthorized USB mass storage plugged into lab PC.",
                 "Rule 19: CRITICAL Canary Ransomware file encryption."
             ], ACCENT_RED)

    # -------------------------------------------------------------
    # SLIDE 7: THE BIG NOVELTY (EXPLAINABLE SCORING & DAILY QUEUE)
    # -------------------------------------------------------------
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7)
    add_header(slide7, "The Project's Big Novelty: Explainable AI Alert Scoring")

    add_card(slide7, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1),
             "Why Standard SOCs Fail Students", [
                 "Commercial SOCs use 'black-box' alert scores with zero explanation of why something is dangerous.",
                 "Student analysts are presented with 5,000 cryptic alarms and don't know where to begin.",
                 "Our Innovation: An automated mathematical formula combining 4 campus factors:",
                 "Score = Base Wazuh Level + Asset Value Multiplier + Off-Hours Penalty + MITRE Impact",
                 "Every alert is classified into 4 actionable priority tiers: P1 (Critical), P2 (High), P3 (Medium), P4 (Low)."
             ], ACCENT_GOLD)

    add_card(slide7, Inches(6.8), Inches(1.7), Inches(5.6), Inches(5.1),
             "Human-Understandable 'Why' Explanations", [
                 "Instead of a raw code number, our engine tells the student analyst in plain English:",
                 "Example Output in our Daily Queue Dashboard:",
                 "'Priority: P1 - CRITICAL | Score: 88/100 | Host: Campus-Portal-Web'",
                 "'Reason: Base severity level 10 yields base score of 50.0 | Asset Campus-Portal-Web is high-value campus database (+40% penalty) | Activity occurred during off-hours outside 08:00-18:00 (+18 pts)'",
                 "Empowers junior student operators to triage incidents in seconds without guessing."
             ], ACCENT_CYAN)

    # -------------------------------------------------------------
    # SLIDE 8: ATTACK SIMULATION (LIVE PROOF IT WORKS)
    # -------------------------------------------------------------
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8)
    add_header(slide8, "Live Attack Simulation: Proving It Works in Practice")

    add_card(slide8, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1),
             "Simulated Attack Execution", [
                 "We created a safe attack simulator script (simulate_attacks.py) to test all defenses live:",
                 "Test 1: Obfuscated PowerShell Execution (MITRE T1059.001) using base64 payload to bypass basic filters.",
                 "Test 2: Living-off-the-Land Certutil payload download (MITRE T1105).",
                 "Test 3: Canary Ransomware Trap (MITRE T1486) simulating malicious encryption on student grade files.",
                 "Test 4: SSH password authentication flood against the campus web server."
             ], ACCENT_CYAN)

    add_card(slide8, Inches(6.8), Inches(1.7), Inches(5.6), Inches(5.1),
             "Real-Time Dashboard Results", [
                 "Telemetry Ingestion: Successfully collected and processed over 2,279 live security events.",
                 "High-Severity Detections: Instantly triggered 3 Level 12+ critical alarms on the dashboard.",
                 "Forensic Evidence: Wazuh recorded the exact PID, parent process, command-line arguments, and timestamp.",
                 "Triage Queue: Alerts were immediately picked up by our Python engine and ranked by priority."
             ], ACCENT_TEAL)

    # -------------------------------------------------------------
    # SLIDE 9: PROJECT DELIVERABLES & IMPACT
    # -------------------------------------------------------------
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9)
    add_header(slide9, "Project Deliverables & Real-World Campus Impact")

    add_card(slide9, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1),
             "Tangible Project Deliverables", [
                 "1. Fully Operational SOC SIEM: Running Wazuh Indexer & Dashboard on VM 1.",
                 "2. 20 Mapped Detection Rules: Cataloged in local_rules.xml with MITRE ATT&CK IDs.",
                 "3. Python Novelty Engine: campus_triage_engine.py with explainable scoring.",
                 "4. Public Web Prototype: Hosted live on GitHub Pages (utkarshkoul.github.io/campus-soc-in-a-box).",
                 "5. Incident Triage Runbook: A 4-phase Standard Operating Procedure (SOP) guiding junior analysts from Detection to Containment."
             ], ACCENT_TEAL)

    add_card(slide9, Inches(6.8), Inches(1.7), Inches(5.6), Inches(5.1),
             "Institutional Impact & Feasibility", [
                 "Zero Software Cost: Saves institutions $100,000+ in enterprise licensing.",
                 "Commodity Hardware: Requires only 8-12 GB RAM on existing college computers.",
                 "Student Training Ground: Provides computer science & IT students hands-on, realistic SOC analyst experience.",
                 "Extensible: New campus departments, Wi-Fi controllers, and lab subnets can be added in minutes."
             ], ACCENT_GOLD)

    # -------------------------------------------------------------
    # SLIDE 10: CONCLUSION & DEMO
    # -------------------------------------------------------------
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10)

    # Accent decorative bar
    bar10 = slide10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(0.15), Inches(3.8))
    bar10.fill.solid()
    bar10.fill.fore_color.rgb = ACCENT_TEAL
    bar10.line.fill.background()

    tbox10 = slide10.shapes.add_textbox(Inches(1.2), Inches(1.7), Inches(11.0), Inches(4.5))
    tf10 = tbox10.text_frame
    tf10.word_wrap = True

    p0 = tf10.paragraphs[0]
    p0.text = "SUMMARY & NEXT STEPS"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_TEAL
    p0.space_after = Pt(8)

    p1 = tf10.add_paragraph()
    p1.text = "Campus SOC-in-a-Box: Ready for Deployment"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_LIGHT
    p1.space_after = Pt(12)

    p2 = tf10.add_paragraph()
    p2.text = "Key Takeaways:\n" \
              "• We successfully proved that small academic colleges can deploy full enterprise-grade SOC monitoring at zero software cost.\n" \
              "• Open-source telemetry (Wazuh + Sysmon + Zeek) gives 100% visibility over campus servers and endpoints.\n" \
              "• Our Explainable AI Alert Scoring eliminates analyst fatigue, making triage effortless for student operators.\n\n" \
              "Live Prototype: https://utkarshkoul.github.io/campus-soc-in-a-box\n" \
              "Source Code: https://github.com/utkarshkoul/campus-soc-in-a-box"
    p2.font.size = Pt(15)
    p2.font.color.rgb = TEXT_MUTED
    p2.space_after = Pt(25)

    p3 = tf10.add_paragraph()
    p3.text = "Thank you! Open for Questions & Live Demonstration."
    p3.font.size = Pt(20)
    p3.font.bold = True
    p3.font.color.rgb = ACCENT_CYAN

    # Save
    output_pptx = r"C:\Users\ACER\.gemini\antigravity\scratch\campus-soc-in-a-box\Campus_SOC_Presentation.pptx"
    prs.save(output_pptx)
    print(f"[+] PowerPoint presentation successfully created: {output_pptx}")

if __name__ == "__main__":
    create_deck()
