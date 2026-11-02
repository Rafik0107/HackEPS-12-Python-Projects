# HackEPS-12 — 12 Professional Python Projects

12 independent, production-shaped Python projects built for HackEPS and a professional portfolio.
From robotics and control engineering to signal processing, machine learning and industrial automation,
each project is a working demonstrator with tested code, bilingual documentation and automated CI.

> **Rafik AMIRI** — MSc Student, Sorbonne University · Master 1 Automatique et Robotique · Mécatronique

## Repository overview

| # | Project | Domain | Key technologies |
|---|---------|--------|------------------|
| 01 | A* / Dijkstra Robot Navigation | Robotics | Python, NumPy, Matplotlib |
| 02 | PID Temperature Controller | Control | Python, NumPy, Matplotlib |
| 03 | Kalman Sensor Tracking | Robotics / Signal | Python, NumPy, Matplotlib |
| 04 | Two-Link Robotic Arm Kinematics | Robotics | Python, NumPy, Matplotlib |
| 05 | Image Edge Detection | Computer Vision | Python, NumPy, Matplotlib, OpenCV optional |
| 06 | Industrial Anomaly Detection | Data / AI | Python, NumPy, scikit-learn optional |
| 07 | Clustering Laboratory | Machine Learning | Python, NumPy |
| 08 | Vibration Frequency Analysis | Signal / Mechanical | Python, NumPy, Matplotlib |
| 09 | Production Job Scheduler | Operations | Python, standard library |
| 10 | IMU Sensor Fusion | Robotics / Control | Python, NumPy, Matplotlib |
| 11 | ECG Peak Detection | Biomedical Signal | Python, NumPy |
| 12 | Warehouse Route Optimizer | Logistics | Python, NumPy, Matplotlib |

## Requirements

- Python **3.10+**
- Most projects only need NumPy and optionally Matplotlib; the big eight (01, 02, 03, 04, 05, 08, 10, 12)
  use NumPy + Matplotlib, and 05/06 optionally use OpenCV / scikit-learn.

## Run a project

```bash
cd 01_astar_robot_navigation      # or any of the 12 folders
python -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Test everything

```bash
python RUN_ALL_TESTS.py
```

## Continuous integration

The `ci.yml` workflow installs dependencies, formats and lints with Black and Ruff, runs the test
suite, executes each project's `main.py` and produces a validation report.

## Portfolio

Supervised by Sorbonne University — Master 1 Automatique et Robotique, Mécatronique.
This repository is built as a recruiter-ready, professional GitHub presence.
