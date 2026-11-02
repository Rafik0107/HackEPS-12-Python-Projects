# Machine Learning Clustering Laboratory

[English documentation](README.md)

Explorer une classification non supervisée k-means reproductible.

## Exécution depuis la racine du dépôt

```bash
python -m pip install -r projects/07_clustering_lab/requirements.txt
python projects/07_clustering_lab/main.py
python projects/07_clustering_lab/test_main.py
```

Python 3.10+ ; NumPy est la seule dépendance externe. La démonstration ne nécessite ni téléchargement de données, ni clé API, ni matériel. Sortie JSON : [exemple enregistré](example_output.json).

## Méthode et interface

Initialisation k-means++ puis itérations de Lloyd ; renvoie étiquettes, centres et historique d’inertie. Centres vides conservés. Graine reproductible et nombre d’itérations borné.

Depuis le dossier de ce projet :

```python
import numpy as np
from main import *
result = kmeans([[-2.,-2.],[-1.9,-2.],[2.,2.],[2.1,2.]], k=2)
print(result)
```

## Vérification

[test_main.py](test_main.py) vérifie des cas numériques de référence, les cas limites et les entrées invalides. Exécuter la commande ci-dessus ou `python run_tests.py` à la racine.

## Périmètre et limites

Optimum local, distance euclidienne, sans normalisation ni choix automatique de k. Standardiser les unités hétérogènes avant ajustement.

Implémentation pédagogique réalisée avec assistance IA pour le portfolio de Rafik AMIRI. Nouveau projet d’apprentissage, sans revendication d’expérience professionnelle, de participation à une compétition ou de déploiement en production. Relire et comprendre le code avant de le présenter.
