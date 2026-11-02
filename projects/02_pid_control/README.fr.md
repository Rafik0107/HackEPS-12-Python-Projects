# Advanced PID Control Simulator

[English documentation](README.md)

Étudier une commande PID saturée sur un système du premier ordre.

## Exécution depuis la racine du dépôt

```bash
python -m pip install -r projects/02_pid_control/requirements.txt
python projects/02_pid_control/main.py
python projects/02_pid_control/test_main.py
```

Python 3.10+ ; NumPy est la seule dépendance externe. La démonstration ne nécessite ni téléchargement de données, ni clé API, ni matériel. Sortie JSON : [exemple enregistré](example_output.json).

## Méthode et interface

Le système vérifie tau*y' + y = u. La dérivée filtrée porte sur la mesure ; une intégration conditionnelle réduit le windup. Renvoie temps, sortie et commande. Temps en secondes, sortie/commande en unités normalisées.

Depuis le dossier de ce projet :

```python
import numpy as np
from main import *
result = simulate(kp=2., ki=1., kd=.1)
print(result)
```

## Vérification

[test_main.py](test_main.py) vérifie des cas numériques de référence, les cas limites et les entrées invalides. Exécuter la commande ci-dessus ou `python run_tests.py` à la racine.

## Périmètre et limites

Système SISO pédagogique ; sans réglage automatique, preuve de stabilité, retard de transport ni validation matérielle.

Implémentation pédagogique réalisée avec assistance IA pour le portfolio de Rafik AMIRI. Nouveau projet d’apprentissage, sans revendication d’expérience professionnelle, de participation à une compétition ou de déploiement en production. Relire et comprendre le code avant de le présenter.
