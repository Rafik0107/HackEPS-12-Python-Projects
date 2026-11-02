# 07 — Clustering Laboratory

K-Means et DBSCAN sur données synthétiques

**Exécuter / Run :** ``python main.py``.

**Tester / Test :** ``python -m unittest discover -s tests -v``.

**Fonctionnalités disponibles :**
  - Exploration A* et Dijkstra, comparaison du temps et de la longueur du chemin
  - Détection d'une destination inaccessible, visualisation ASCII / PNG
  - Interface en ligne de commande, annotations de type, gestion des erreurs

**Technologies :** numpy.

**Installation :**
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
**Résultats :** les figures et fichiers texte générés sont dans le dossier racine.
**Documentation anglaise :** voir `README.md`.
**Limites :** démonstrateur pédagogique, pas un système autonome validé.