# Kalman Filter Sensor Tracking

[English documentation](README.md)

Estimer position et vitesse à partir de mesures scalaires bruitées.

## Exécution depuis la racine du dépôt

```bash
python -m pip install -r projects/03_kalman_tracking/requirements.txt
python projects/03_kalman_tracking/main.py
python projects/03_kalman_tracking/test_main.py
```

Python 3.10+ ; NumPy est la seule dépendance externe. La démonstration ne nécessite ni téléchargement de données, ni clé API, ni matériel. Sortie JSON : [exemple enregistré](example_output.json).

## Méthode et interface

Modèle à vitesse constante avec accélération aléatoire discrète ; mise à jour de Joseph. NaN saute la correction. Renvoie estimations (N,2) et covariances (N,2,2). dt en secondes ; variances exprimées dans des unités cohérentes.

Depuis le dossier de ce projet :

```python
import numpy as np
from main import *
result = track([0., 1.1, 1.9, 3.2])
print(result)
```

## Vérification

[test_main.py](test_main.py) vérifie des cas numériques de référence, les cas limites et les entrées invalides. Exécuter la commande ci-dessus ou `python run_tests.py` à la racine.

## Périmètre et limites

Mouvement linéaire à une dimension et bruits spécifiés ; sans rejet des valeurs aberrantes ni suivi non linéaire.

Implémentation pédagogique réalisée avec assistance IA pour le portfolio de Rafik AMIRI. Nouveau projet d’apprentissage, sans revendication d’expérience professionnelle, de participation à une compétition ou de déploiement en production. Relire et comprendre le code avant de le présenter.
