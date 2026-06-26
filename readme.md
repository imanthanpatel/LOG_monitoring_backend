# 🛡️ SentinelSIEM — Lightweight Security Information & Event Monitoring Engine

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.x-green.svg)
![DRF](https://img.shields.io/badge/DRF-Enabled-red.svg)
![MITRE ATT&CK](https://img.shields.io/badge/MITRE-ATT%26CK-purple.svg)
![Status](https://img.shields.io/badge/Status-Active%20Development-orange.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

---

## 📌 Overview

**SentinelSIEM** is a lightweight, modular **Security Information and Event Management (SIEM)** system built using Django.

It is designed to simulate **real-world SOC detection pipelines**, where logs are ingested, analyzed using behavioral rules, and mapped to **MITRE ATT&CK techniques** to generate actionable security alerts.

This project demonstrates how enterprise SIEM systems like Splunk or Elastic SIEM work internally — but in a simplified, customizable architecture.

---

## 🎯 Objectives

- Simulate real-world SOC detection workflows
- Build a rule-based security detection engine
- Map attacks to MITRE ATT&CK framework
- Perform time-window based log correlation
- Generate structured alerts & incidents
- Enable cybersecurity learning & experimentation

---

## 🏗️ System Architecture
                ┌────────────────────────┐
                │   Log Sources          │
                │ (Windows / Apps / API) │
                └──────────┬─────────────┘
                           │
                           ▼
                ┌────────────────────────┐
                │  Ingestion Layer       │
                │  Django REST API       │
                └──────────┬─────────────┘
                           │
                           ▼
                ┌────────────────────────┐
                │   Log Storage DB       │
                │ (SQLite / PostgreSQL)   │
                └──────────┬─────────────┘
                           │
                           ▼
                ┌────────────────────────┐
                │ Detection Engine       │
                │ (Rule-Based System)    │
                └──────────┬─────────────┘
                           │
                           ▼
                ┌────────────────────────┐
                │ MITRE ATT&CK Mapper    │
                └──────────┬─────────────┘
                           │
                           ▼
                ┌────────────────────────┐
                │ Alert & Incident Layer │
                └──────────┬─────────────┘
                           │
                           ▼
                ┌────────────────────────┐
                │ API / Dashboard Layer  │
                └────────────────────────┘
                
---

## ⚙️ Core Features

### 📥 Log Ingestion
- REST API-based log collection
- Supports Windows Event-like structured logs
- Flexible JSON ingestion format

### 🧠 Detection Engine
- Rule-based security detection system
- Time-window correlation (5–10 min behavioral tracking)
- Stateful detection using `DetectionState`

### 🚨 Alert System
- Deduplication of alerts
- Severity classification (Low / Medium / High / Critical)
- Incident creation pipeline

### 🧩 MITRE ATT&CK Mapping
- Automatic mapping of detections to ATT&CK IDs
- Supports tactic + technique alignment
- Enhances threat context understanding

---

## 🧠 Detection Coverage

### 🔐 Authentication Attacks
| Technique | MITRE ID |
|-----------|----------|
| Brute Force Detection | T1110 |
| Brute Force Success | T1110.001 |
| RDP Login | T1021.001 |
| Off-hours Login | T1078 |

---

### 💻 Execution Attacks
| Technique | MITRE ID |
|-----------|----------|
| PowerShell Execution | T1059.001 |
| Suspicious PowerShell | T1059.001 |
| Suspicious Process Creation | T1059 |

---

### 🛠 Persistence & Privilege Abuse
| Technique | MITRE ID |
|-----------|----------|
| Scheduled Task Creation | T1053.005 |
| Service Installation | T1543 |
| New User Creation | T1136 |
| User Deletion | T1531 |

---

## 🔄 Detection Flow

1. Logs are ingested via `/api/ingest/`
2. Stored in structured database
3. Detection engine scans only new logs
4. Rule engine applies behavioral logic
5. Matching patterns trigger alerts
6. MITRE ATT&CK mapping enriches alerts
7. Alerts are exposed via `/api/alerts/`

---

## 🧪 Installation & Setup

### 1️⃣ Clone Repository
```bash
git clone https://github.com/yourusername/sentinelsiem.git
cd sentinelsiem
```
### 2️⃣ Create Virtual Environment
```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
### 3️⃣ Install Dependencies
```
pip install -r requirements.txt
```
### 4️⃣ Run Migrations
```
python manage.py migrate
```
### 5️⃣ Start Server
```
python manage.py runserver
```
### 6️⃣ Run Detection Engine
```
python manage.py run_detection
```
### 🧪 Testing Attack Simulation(This project includes a built-in attack simulator.)
```
python test\test_siem.py

This script simulates:

Brute force attacks
PowerShell exploitation
Suspicious process execution
Privilege escalation attempts
Persistence mechanisms
```


### 📊 Example Alert Output
```
{
  "id": 24,
  "rule_name": "Brute Force Detection",
  "severity": "High",
  "description": "12 failed logins in 5 minutes. Targets: admin",
  "mitre_technique": {
    "technique_id": "T1110",
    "name": "Brute Force"
  },
  "timestamp": "2026-06-26T10:00:00Z"
}
```
### 🧰 Tech Stac
```
| Layer          | Technology                  |
| -------------- | --------------------------- |
| Backend        | Django                      |
| API Layer      | Django REST Framework       |
| Database       | SQLite / PostgreSQL         |
| Language       | Python                      |
| Security Model | MITRE ATT&CK Framework      |
| Architecture   | Rule-based Detection Engine |

```
### 🎯Real-World Use Cases
```
SOC analyst training simulation
Cybersecurity lab environment
MITRE ATT&CK learning platform
SIEM architecture education
Blue-team detection engineering practice

```
### 🚀 Future Roadmap
```
🔴 Real-time streaming detection (Kafka/WebSockets)
🤖 AI-based anomaly detection engine
📊 SOC dashboard (React / Next.js)
🔗 Attack chain correlation (Kill-chain analysis)
🌐 Threat intelligence feed integration
📡 ELK stack integration

```
### 👨‍💻 Author
```
Manthan Patel

```
### ⭐ Support This Project
```
If you find this project useful:

⭐ Star the repository
🍴 Fork it
🧠 Contribute new detection rules
🚀 Improve MITRE coverage

```
### ⚠️ Disclaimer
```
This project is built for educational and research purposes only.

It is NOT intended for production enterprise security monitoring.
```












