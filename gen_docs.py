# -*- coding: utf-8 -*-
import os

PROJECTS = [
    ("01_astar_robot_navigation", "01 — Autonomous Robot Navigation", "A* / Dijkstra exploration 2D", ["numpy", "matplotlib"]),
    ("02_pid_temperature_controller", "02 — PID Temperature Controller", "Régulateur P / PI / PID thermique", ["numpy", "matplotlib"]),
    ("03_kalman_sensor_tracking", "03 — Kalman Sensor Tracking", "Filtre de Kalman 1D (position + vitesse)", ["numpy", "matplotlib"]),
    ("04_robot_arm_kinematics", "04 — Two-Link Robotic Arm", "Cinématique directe et inverse", ["numpy", "matplotlib"]),
    ("05_pgm_image_edge_detection", "05 — Image Edge Detection", "Pipeline PGM (Sobel, Canny, morphologie)", ["numpy", "matplotlib"]),
    ("06_anomaly_detection", "06 — Industrial Anomaly Detection", "Détection d'anomalies sur capteurs", ["numpy"]),
    ("07_kmeans_clustering", "07 — Clustering Laboratory", "K-Means et DBSCAN sur données synthétiques", ["numpy"]),
    ("08_vibration_frequency_analysis", "08 — Vibration Frequency Analysis", "Analyse spectrale et RMS des vibrations", ["numpy", "matplotlib"]),
    ("09_production_job_scheduler", "09 — Production Job Scheduler", "Ordonnancement FCFP / SPT, makespan", []),
    ("10_imu_sensor_fusion", "10 — IMU Sensor Fusion", "Filtre complémentaire pour orientation IMU", ["numpy", "matplotlib"]),
    ("11_ecg_peak_detection", "11 — ECG Peak Detection", "Analyse pédagogique ECG (pics R, fréquence cardiaque)", ["numpy"]),
    ("12_warehouse_route_optimizer", "12 — Warehouse Route Optimizer", "Optimisation de tournée en entrepôt", ["numpy", "matplotlib"]),
]
PYTHON = ">=3.10"

def en_readme(title, desc, deps):
    feats = ["A* and Dijkstra search, compared on runtime and path length", "Unreachable destination detection and path visualisation (ASCII / PNG)", "Command-line interface, type annotations and error handling"]
    deps_line = ", ".join(deps) if deps else "standard library only"
    return f"""# {title}

{desc}

**Run / Exécuter :** ``python main.py``.

**Test / Tester :** ``python -m unittest discover -s tests -v``.

**Real features :**
{chr(10).join('  - ' + f for f in feats)}

**Technologies :** {', '.join(deps) if deps else 'standard library only'}.

**Installation :**
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
**Outputs :** generated figures and text files sit in the repository root.
**Limits :** educational demonstrator, not a validated autonomous system."""

def fr_readme(title, desc, deps):
    feats = ["Exploration A* et Dijkstra, comparaison du temps et de la longueur du chemin", "Détection d'une destination inaccessible, visualisation ASCII / PNG", "Interface en ligne de commande, annotations de type, gestion des erreurs"]
    deps_line = ", ".join(deps) if deps else "librairies standard uniquement"
    return f"""# {title}

{desc}

**Exécuter / Run :** ``python main.py``.

**Tester / Test :** ``python -m unittest discover -s tests -v``.

**Fonctionnalités disponibles :**
{chr(10).join('  - ' + f for f in feats)}

**Technologies :** {', '.join(deps) if deps else 'librairies standard uniquement'}.

**Installation :**
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
**Résultats :** les figures et fichiers texte générés sont dans le dossier racine.
**Documentation anglaise :** voir `README.md`.
**Limites :** démonstrateur pédagogique, pas un système autonome validé."""

def pyproject(deps):
    deps_line = ", ".join(f'"{d}"' for d in deps) if deps else '"numpy>=1.24"'
    return f"""[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "project"
version = "0.1.0"
description = "Professional Python project for the HackEPS-12 portfolio."
requires-python = "{PYTHON}"
dependencies = [{deps_line}]

[tool.setuptools]
packages = []

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
"""

def requirements(deps):
    lines = ["# Python 3.10+", ""]
    if deps:
        lines.append("# Dependances compatibles (NumPy à jour).")
        lines.extend(deps)
    else:
        lines.append("# Standard library only.")
    return "\n".join(lines) + "\n"

def write_docs():
    cwd = os.getcwd()
    for folder, title, desc, deps in PROJECTS:
        os.chdir(os.path.join(cwd, folder))
        for fname, content in [("README.md", en_readme(title, desc, deps)), ("README_FR.md", fr_readme(title, desc, deps)), ("pyproject.toml", pyproject(deps)), ("requirements.txt", requirements(deps))]:
            with open(fname, "w", encoding="utf-8") as fh:
                fh.write(content)
            print("wrote", fname)
        os.chdir(cwd)
    print("done")

if __name__ == "__main__":
    write_docs()
