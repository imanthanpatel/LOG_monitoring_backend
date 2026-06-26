# 📡 Lightweight SIEM & Detection Engine

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.x-green.svg)
![MITRE ATT&CK](https://img.shields.io/badge/MITRE-ATT%26CK-red.svg)
![Status](https://img.shields.io/badge/Status-Active-orange.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

---

## 🛡️ Overview

This project is a **Lightweight Security Information and Event Management (SIEM) system** built using **Django**.

It simulates a real-world SOC (Security Operations Center) pipeline by:
- Collecting logs
- Detecting malicious behavior using rules
- Mapping detections to MITRE ATT&CK techniques
- Generating alerts and incidents

> 🎯 Goal: Learn how SIEM systems detect real-world cyber attacks using behavioral rules.

---

## 🏗️ Architecture
📥 Log Sources
          ↓
🚀 Ingestion API (Django REST)
          ↓
🗄️ Log Database
          ↓
🧠 Detection Engine (Rule-Based System)
          ↓
🧩 MITRE ATT&CK Mapping
          ↓
🚨 Alert & Incident System
          ↓
📊 API / Dashboard