# A* Autonomous Robot Navigation

[English documentation](README.md)

Calculer un plus court chemin sans collision sur une grille binaire.

## Exécution depuis la racine du dépôt

```bash
python -m pip install -r projects/01_astar_navigation/requirements.txt
python projects/01_astar_navigation/main.py
python projects/01_astar_navigation/test_main.py
```

Python 3.10+ ; NumPy est la seule dépendance externe. La démonstration ne nécessite ni téléchargement de données, ni clé API, ni matériel. Sortie JSON : [exemple enregistré](example_output.json).

## Méthode et interface

A* utilise la distance de Manhattan, des coûts unitaires et quatre voisins. Renvoie une liste de cellules (ligne, colonne), ou [] si la cible est inaccessible.

Depuis le dossier de ce projet :

```python
import numpy as np
from main import *
result = astar([[0,0],[1,0]], (0,0), (1,1))
print(result)
```

## Vérification

[test_main.py](test_main.py) vérifie des cas numériques de référence, les cas limites et les entrées invalides. Exécuter la commande ci-dessus ou `python run_tests.py` à la racine.

## Périmètre et limites

Grille statique uniquement ; sans dynamique, localisation, inflation des obstacles ni obstacles mobiles.

Implémentation pédagogique réalisée avec assistance IA pour le portfolio de Rafik AMIRI. Nouveau projet d’apprentissage, sans revendication d’expérience professionnelle, de participation à une compétition ou de déploiement en production. Relire et comprendre le code avant de le présenter.
