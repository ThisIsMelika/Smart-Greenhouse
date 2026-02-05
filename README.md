# Smart Greenhouse Monitoring System  

Academic/individual prototype implementing core parts of a **smart greenhouse monitoring system** based on a given Software Requirements Specification (SRS).

Focus: sensor data collection → threshold validation → alerting → persistent storage — with clean Persian RTL user interface.

## What this project demonstrates

This project demonstrates:
- Domain-driven design for sensor-based systems
- Threshold-based decision logic
- Alert generation workflow (partial)
- Trade-offs between rapid prototyping and system completeness
- Mapping system behaviour to formal functional requirements (SRS)

## System Scope & Workflow

- Sensor data (manual input)
- Validation & strong typing
- Threshold comparison
- Warning/alert feedback
- Persistent storage (JSON Lines + SQLite)

The current version prioritises correct data flow, architectural clarity, and domain modeling over full system completeness.



### Current Implementation Status (Feb 2026)

| Feature                               | Status       | Coverage of SRS | Comment / Limitation                                      |
|:--------------------------------------|:------------:|:---------------:|-------------------------------------------------------------------|
| Manual sensor data entry + validation | ✓ Complete   | FR-01 (partial) | Full Persian UI, input sanitization, meaningful errors           |
| Threshold (min/max) configuration     | ✓ Complete   | FR-06           | Per-reading thresholds — saved with every record                 |
| Out-of-range warning (popup)          | ✓ Partial    | FR-02           | Immediate messagebox — no persistent alert entity yet            |
| Dual persistence layer                | ✓ Complete   | FR-09 (partial) | Every record → JSON Lines **+** SQLite — queryable & append-only |
| Last N records table (live refresh)   | ✓ Complete   | —               | Shows last 15 entries, auto-updates after each save              |
| Authentication & authorization        | ✗ Not done   | FR-14           | **Critical gap** — everyone has full access right now            |
| Persistent alert list & lifecycle     | ✗ Not done   | FR-10, FR-11, FR-12 | No alert history, no acknowledge/resolve/escalate workflow      |
| Real-time sensor polling / WebSocket  | ✗ Planned    | FR-01           | Tkinter limitation — manual entry only                           |
| Actuator control (pump/fan/heater)    | ✗ Planned    | FR-03, FR-04, FR-05 | No simulation or real control yet                                |
| Notification (Telegram/SMS/email)     | ✗ Planned    | FR-02           | Only local UI popup                                              |

### Key Strengths 

- Clean separation: UI layer ↔ domain model ↔ persistence
- Strong typing & data integrity with `dataclass SensorReading`
- **Dual-write** pattern (JSONL for audit trail + SQLite for querying)
- Full **right-to-left** Persian interface with consistent greenhouse theme
- Input validation + user-friendly error messages in Persian
- Explicit documentation of design gaps and trade-offs (engineering maturity)
- Alert lifecycle design is complete at the domain level (UML), implementation deferred

### Known Gaps & Trade-offs (be ready to explain these)

| Gap / Trade-off                        | Why it happened                              | Realistic next step / learning outcome                     |
|----------------------------------------|----------------------------------------------|------------------------------------------------------------|
| No login & no role-based access        | Time constraint + focused on data flow first | Add simple Flask/FastAPI + JWT in next 1–2 weeks           |
| No persistent Alert entity             | Prioritized data collection & display        | Most important missing “operator workflow” piece           |
| Tkinter instead of web frontend        | Fastest way to build usable UI in short time | Migration path: → FastAPI backend + React/Vue              |
| Manual data entry only                 | No hardware / no time for simulator          | Add background thread + fake sensor generator next         |
| No real notification channel           | Focused on core logic before integrations    | Telegram bot is low-hanging fruit for phase 2              |

### Functional Requirements Coverage Summary

| ID    | Short Description                                      | Priority | Done?     | Level of completion                          |
|-------|--------------------------------------------------------|----------|-----------|----------------------------------------------|
| FR-01 | Display sensor values (temp, hum, CO₂, light)          | Must     | ⚠️ Partial| Manual only – no automatic 5-second polling  |
| FR-02 | Alert when threshold exceeded                          | Must     | ✓ Partial | Local popup – no external notification       |
| FR-06 | Configure & save thresholds                            | Must     | ✓ Yes     | Fully implemented in UI                      |
| FR-09 | Store data & events in database                        | Must     | ✓ Yes     | SQLite + JSONL (MySQL planned later)         |
| FR-03–05 | Irrigation & climate control                        | Must/Could | ✗ Planned | Business logic not started yet               |

## Planned Full-Stack Extension (In Progress)

This project is currently being extended into a full-stack system.

Planned short-term milestones :

•	Backend API using FastAPI (sensor data, thresholds, alerts)
•	Role-based authentication and authorisation (JWT)
•	Persistent alert lifecycle (acknowledge/resolve)
•	Web-based frontend (React or similar)
•	Separation of frontend and backend concerns

The current Tkinter-based UI will serve as a functional prototype, while the full-stack version will focus on scalability, security, and real-world deployment concerns.


### Tech Stack

- Python 3.9–3.11
- Tkinter + ttk (custom theme)
- SQLite (structured storage)
- JSON Lines (immutable log)
- dataclasses + type hints

## How to run
```bash
python greenhouse_monitor_ui.py

No external dependencies required.
Tested on Python 3.10 (Windows / Linux).




python greenhouse_monitor_ui.py
