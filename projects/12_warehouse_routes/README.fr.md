# Smart Warehouse Route Optimization

[English documentation](README.md)

Trouver une tournée fermée minimale sur une petite grille avec obstacles.

## Exécution depuis la racine du dépôt

```bash
python -m pip install -r projects/12_warehouse_routes/requirements.txt
python projects/12_warehouse_routes/main.py
python projects/12_warehouse_routes/test_main.py
```

Python 3.10+ ; NumPy est la seule dépendance externe. La démonstration ne nécessite ni téléchargement de données, ni clé API, ni matériel. Sortie JSON : [exemple enregistré](example_output.json).

## Méthode et interface

BFS calcule les plus courts chemins avec obstacles, puis Held-Karp optimise l’ordre de visite. Renvoie ordre, chemin cellule par cellule et distance en déplacements. Maximum 12 collectes.

Depuis le dossier de ce projet :

```python
import numpy as np
from main import *
result = optimize(np.zeros((5,5)), (0,0), [(1,2),(4,4)])
print(result)
```

## Vérification

[test_main.py](test_main.py) vérifie des cas numériques de référence, les cas limites et les entrées invalides. Exécuter la commande ci-dessus ou `python run_tests.py` à la racine.

## Périmètre et limites

Exact uniquement pour cette grille statique à coût unitaire. Complexité exponentielle ; sans capacités, véhicules multiples, fenêtres horaires ni congestion. Peut traverser une autre collecte en route.

Implémentation pédagogique réalisée avec assistance IA pour le portfolio de Rafik AMIRI. Nouveau projet d’apprentissage, sans revendication d’expérience professionnelle, de participation à une compétition ou de déploiement en production. Relire et comprendre le code avant de le présenter.
