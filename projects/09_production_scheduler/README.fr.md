# Industrial Production Scheduler

[English documentation](README.md)

Affecter des tâches indépendantes à des machines parallèles identiques.

## Exécution depuis la racine du dépôt

```bash
python -m pip install -r projects/09_production_scheduler/requirements.txt
python projects/09_production_scheduler/main.py
python projects/09_production_scheduler/test_main.py
```

Python 3.10+ ; NumPy est la seule dépendance externe. La démonstration ne nécessite ni téléchargement de données, ni clé API, ni matériel. Sortie JSON : [exemple enregistré](example_output.json).

## Méthode et interface

LPT : trier les durées décroissantes et affecter à la machine la moins chargée. Sortie : intervalles, durée totale et borne inférieure. Toutes les durées utilisent la même unité.

Depuis le dossier de ce projet :

```python
import numpy as np
from main import *
result = schedule({'job_a': 5, 'job_b': 3, 'job_c': 2}, machines=2)
print(result)
```

## Vérification

[test_main.py](test_main.py) vérifie des cas numériques de référence, les cas limites et les entrées invalides. Exécuter la commande ci-dessus ou `python run_tests.py` à la racine.

## Périmètre et limites

Heuristique sans garantie d’optimalité ; tâches indépendantes non préemptives. Sans précédences, disponibilités, réglages, échéances ni machines hétérogènes.

Implémentation pédagogique réalisée avec assistance IA pour le portfolio de Rafik AMIRI. Nouveau projet d’apprentissage, sans revendication d’expérience professionnelle, de participation à une compétition ou de déploiement en production. Relire et comprendre le code avant de le présenter.
