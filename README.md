# Greenhouse Control System (UML Modeling Project)

## Overview
This project presents the analysis and UML modeling of a Greenhouse Control System. The system focuses on sensor monitoring, alert management, and irrigation control. All diagrams are provided as PlantUML sources and exported images for documentation.

## Scope
- Manage Sensors
- Manage Alerts
- Irrigation Control (Plan / Auto / Manual)
- Generate Reports
- Manage Users

## Actors
- Operation Manager: views sensor status, sets limits/thresholds, acknowledges alerts, generates reports
- Technician: calibrates sensors, handles and resolves alerts, performs maintenance

## Included UML Diagrams
- Use Case Diagrams:
  - Manage Sensors
  - Manage Alerts
  - Irrigation Control
- Activity Diagrams:
  - Manage Sensors
  - Manage Alerts
- Sequence Diagrams:
  - Sensor Management scenario
  - Alert Handling scenario

## Tools
- PlantUML for code-based diagram generation
- Visual Paradigm  for manual drawing/presentation
- Export formats: PNG / SVG

## How to Generate Diagrams (PlantUML)
1) Open the `.puml` files using the PlantUML online server or a VS Code plugin.
2) Render the diagrams.
3) Export as PNG or SVG.
4) Include exports in the final report.

## Suggested Project Structure
- `diagrams/usecase/`
- `diagrams/activity/`
- `diagrams/sequence/`
- `exports/`
- `docs/`

## Notes
- Actor and use-case naming is consistent across all diagrams.
- `<<include>>` and `<<extend>>` relationships reflect the system’s behavioral scenarios.

## Author
- Name: Melika Bagheri
- Course/University: (optional)
- Date: (optional)
