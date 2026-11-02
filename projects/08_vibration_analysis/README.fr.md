# Mechanical Vibration Analysis

[English documentation](README.md)

Simuler des vibrations libres et estimer la fréquence dominante.

## Exécution depuis la racine du dépôt

```bash
python -m pip install -r projects/08_vibration_analysis/requirements.txt
python projects/08_vibration_analysis/main.py
python projects/08_vibration_analysis/test_main.py
```

Python 3.10+ ; NumPy est la seule dépendance externe. La démonstration ne nécessite ni téléchargement de données, ni clé API, ni matériel. Sortie JSON : [exemple enregistré](example_output.json).

## Méthode et interface

Système masse-ressort-amortisseur m*x'' + c*x' + k*x = 0 intégré par RK4. Renvoie secondes, (déplacement, vitesse), énergie. Unités SI : kg, N/m, N*s/m, m. FFT avec fenêtre de Hann, hors composante continue.

Depuis le dossier de ce projet :

```python
import numpy as np
from main import *
result = simulate(mass=1., stiffness=100., damping=.4)
print(result)
```

## Vérification

[test_main.py](test_main.py) vérifie des cas numériques de référence, les cas limites et les entrées invalides. Exécuter la commande ci-dessus ou `python run_tests.py` à la racine.

## Périmètre et limites

Un degré de liberté linéaire, sans excitation ni structure modale. Résolution FFT environ 1/durée ; pic peu fiable si fortement amorti.

Implémentation pédagogique réalisée avec assistance IA pour le portfolio de Rafik AMIRI. Nouveau projet d’apprentissage, sans revendication d’expérience professionnelle, de participation à une compétition ou de déploiement en production. Relire et comprendre le code avant de le présenter.
