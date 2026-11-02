# Python Engineering Portfolio — Rafik AMIRI

MSc Year 1 student in Automation & Robotics, Mechatronics Design for Health, Sorbonne Université, Paris.

Twelve runnable educational projects exploring robotics, control, signal processing, computer vision and optimization. Prepared with AI assistance in October 2026. Each project includes working code, dependency declarations, automated tests, an executable demonstration and documentation in English and French.

The repository name refers to preparation for HackEPS; it does **not** imply acceptance, participation, endorsement or an award. These are scoped learning implementations, not production systems or previously completed professional work.

## Quick start

Python 3.10 or newer:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS / Linux:
# source .venv/bin/activate
python -m pip install -r requirements.txt
python run_tests.py
python projects/01_astar_navigation/main.py
```

If PowerShell activation is disabled, use `.venv\Scripts\python.exe -m pip install -r requirements.txt` and `.venv\Scripts\python.exe run_tests.py` directly.

## Projects

| # | English documentation | Français |
|---|---|---|
| 01 | [A* Autonomous Robot Navigation](projects/01_astar_navigation/README.md) | [FR](projects/01_astar_navigation/README.fr.md) |
| 02 | [Advanced PID Control Simulator](projects/02_pid_control/README.md) | [FR](projects/02_pid_control/README.fr.md) |
| 03 | [Kalman Filter Sensor Tracking](projects/03_kalman_tracking/README.md) | [FR](projects/03_kalman_tracking/README.fr.md) |
| 04 | [Robotic Arm Kinematics Simulator](projects/04_arm_kinematics/README.md) | [FR](projects/04_arm_kinematics/README.fr.md) |
| 05 | [Computer Vision Edge Detection](projects/05_edge_detection/README.md) | [FR](projects/05_edge_detection/README.fr.md) |
| 06 | [Industrial Anomaly Detection](projects/06_anomaly_detection/README.md) | [FR](projects/06_anomaly_detection/README.fr.md) |
| 07 | [Machine Learning Clustering Laboratory](projects/07_clustering_lab/README.md) | [FR](projects/07_clustering_lab/README.fr.md) |
| 08 | [Mechanical Vibration Analysis](projects/08_vibration_analysis/README.md) | [FR](projects/08_vibration_analysis/README.fr.md) |
| 09 | [Industrial Production Scheduler](projects/09_production_scheduler/README.md) | [FR](projects/09_production_scheduler/README.fr.md) |
| 10 | [IMU Sensor Fusion](projects/10_imu_fusion/README.md) | [FR](projects/10_imu_fusion/README.fr.md) |
| 11 | [Biomedical ECG Signal Analysis](projects/11_ecg_analysis/README.md) | [FR](projects/11_ecg_analysis/README.fr.md) |
| 12 | [Smart Warehouse Route Optimization](projects/12_warehouse_routes/README.md) | [FR](projects/12_warehouse_routes/README.fr.md) |

## Validation and reproducibility

41 test methods across 12 isolated suites passed locally on 3.12.14 with NumPy 2.3.5. All 12 default demos ran successfully. Re-run on 2 November 2026 with Python 3.15.1 and NumPy 2.5.4 on Windows: same result (41/41). Test count includes parameterized loops within individual methods. See [validation details](VALIDATION.md) and [test log](validation/test-results.txt). CI is configured but is not claimed to have run until GitHub reports it.

Tests verify the stated model and specific cases; they do not establish general industrial or clinical readiness. Input arrays and parameters should be of ordinary engineering magnitudes; extreme floating-point overflow is outside the validated scope.

## Français

Portfolio pédagogique de 12 projets Python : code exécutable, dépendances, tests et documentation bilingue. Les données de démonstration sont synthétiques. Les limites de chaque modèle sont décrites dans son README français. Ces projets ne constituent pas une certification industrielle ou médicale, et ne prouvent pas une participation à HackEPS.

Lancer `python run_tests.py` pour les tests ou `python projects/<dossier>/main.py` pour une démonstration. Les API permettent de fournir ses propres paramètres ; le projet Sobel accepte aussi `--input image.npy --output edges.npy`.

## Earlier draft

A first draft of these projects (commit `f92186b`, 27 October 2026) is preserved unchanged in [archive/first-draft-2026-10-27](archive/first-draft-2026-10-27/). It is superseded by the versions above; its README wording and its CI workflow (disabled, failing) are kept only for history.

## Attribution

Prepared for Rafik AMIRI with AI coding assistance. Human review and understanding are required before describing these projects in applications or interviews. No third-party datasets or copied project repositories are included.
