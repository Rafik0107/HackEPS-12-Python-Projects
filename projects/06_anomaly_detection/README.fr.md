# Industrial Anomaly Detection

[English documentation](README.md)

Détecter les valeurs inhabituelles à partir d’une référence normale robuste.

## Exécution depuis la racine du dépôt

```bash
python -m pip install -r projects/06_anomaly_detection/requirements.txt
python projects/06_anomaly_detection/main.py
python projects/06_anomaly_detection/test_main.py
```

Python 3.10+ ; NumPy est la seule dépendance externe. La démonstration ne nécessite ni téléchargement de données, ni clé API, ni matériel. Sortie JSON : [exemple enregistré](example_output.json).

## Méthode et interface

Ajuster médiane et 1,4826*MAD uniquement sur des données normales. Score : maximum des écarts standardisés absolus. Échelle minimale : 1e-9. Forme : (échantillons, variables).

Depuis le dossier de ce projet :

```python
import numpy as np
from main import *
result = RobustDetector().fit([[-1.],[0.],[1.]]).predict([[0.],[10.]])
print(result)
```

## Vérification

[test_main.py](test_main.py) vérifie des cas numériques de référence, les cas limites et les entrées invalides. Exécuter la commande ci-dessus ou `python run_tests.py` à la racine.

## Périmètre et limites

Règle par variable ; ignore corrélations et dérive. Le seuil n’est pas une probabilité calibrée. Forte sensibilité des variables constantes. Évaluation synthétique uniquement.

Implémentation pédagogique réalisée avec assistance IA pour le portfolio de Rafik AMIRI. Nouveau projet d’apprentissage, sans revendication d’expérience professionnelle, de participation à une compétition ou de déploiement en production. Relire et comprendre le code avant de le présenter.
