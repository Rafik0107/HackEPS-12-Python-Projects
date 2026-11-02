# Robotic Arm Kinematics Simulator

[English documentation](README.md)

Calculer les cinématiques directe/inverse et le Jacobien d’un bras planaire.

## Exécution depuis la racine du dépôt

```bash
python -m pip install -r projects/04_arm_kinematics/requirements.txt
python projects/04_arm_kinematics/main.py
python projects/04_arm_kinematics/test_main.py
```

Python 3.10+ ; NumPy est la seule dépendance externe. La démonstration ne nécessite ni téléchargement de données, ni clé API, ni matériel. Sortie JSON : [exemple enregistré](example_output.json).

## Méthode et interface

Deux articulations rotatives ; l’inverse renvoie les deux configurations en radians. Longueurs et cibles partagent la même unité. À l’origine repliée, une solution représentative est renvoyée.

Depuis le dossier de ce projet :

```python
import numpy as np
from main import *
result = inverse(1.2, .6, l1=1., l2=1.)
print(result)
```

## Vérification

[test_main.py](test_main.py) vérifie des cas numériques de référence, les cas limites et les entrées invalides. Exécuter la commande ci-dessus ou `python run_tests.py` à la racine.

## Périmètre et limites

Sans limites articulaires, collisions, dynamique, commande de trajectoire ni géométrie 3D. Les singularités ne sont pas évitées.

Implémentation pédagogique réalisée avec assistance IA pour le portfolio de Rafik AMIRI. Nouveau projet d’apprentissage, sans revendication d’expérience professionnelle, de participation à une compétition ou de déploiement en production. Relire et comprendre le code avant de le présenter.
