# 11 — ECG Peak Detection

Analyse pédagogique ECG (pics R, fréquence cardiaque)

**Run / Exécuter :** ``python main.py``.

**Test / Tester :** ``python -m unittest discover -s tests -v``.

**Real features :**
  - A* and Dijkstra search, compared on runtime and path length
  - Unreachable destination detection and path visualisation (ASCII / PNG)
  - Command-line interface, type annotations and error handling

**Technologies :** numpy.

**Installation :**
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
**Outputs :** generated figures and text files sit in the repository root.
**Limits :** educational demonstrator, not a validated autonomous system.