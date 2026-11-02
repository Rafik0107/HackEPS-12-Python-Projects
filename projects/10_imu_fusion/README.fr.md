# IMU Sensor Fusion

[English documentation](README.md)

Estimer un angle de roulis avec gyroscope et accéléromètre.

## Exécution depuis la racine du dépôt

```bash
python -m pip install -r projects/10_imu_fusion/requirements.txt
python projects/10_imu_fusion/main.py
python projects/10_imu_fusion/test_main.py
```

Python 3.10+ ; NumPy est la seule dépendance externe. La démonstration ne nécessite ni téléchargement de données, ni clé API, ni matériel. Sortie JSON : [exemple enregistré](example_output.json).

## Méthode et interface

Filtre complémentaire avec écarts angulaires ramenés à [-pi,pi[. Gyroscope (N,) en rad/s ; accélération (N,3), z positif au roulis nul. Sortie en radians, échantillonnage uniforme.

Depuis le dossier de ce projet :

```python
import numpy as np
from main import *
result = fuse(np.zeros(100), np.tile([0.,0.,1.], (100,1)))
print(result)
```

## Vérification

[test_main.py](test_main.py) vérifie des cas numériques de référence, les cas limites et les entrées invalides. Exécuter la commande ci-dessus ou `python run_tests.py` à la racine.

## Périmètre et limites

Orientation quasi statique sur un axe, pas un AHRS 3D. L’accélération linéaire perturbe la gravité ; sans étalonnage de biais ni cap magnétique.

Implémentation pédagogique réalisée avec assistance IA pour le portfolio de Rafik AMIRI. Nouveau projet d’apprentissage, sans revendication d’expérience professionnelle, de participation à une compétition ou de déploiement en production. Relire et comprendre le code avant de le présenter.
