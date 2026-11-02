# Computer Vision Edge Detection

[English documentation](README.md)

Extraire les gradients de Sobel et des contours seuillés.

## Exécution depuis la racine du dépôt

```bash
python -m pip install -r projects/05_edge_detection/requirements.txt
python projects/05_edge_detection/main.py
python projects/05_edge_detection/test_main.py
```

Python 3.10+ ; NumPy est la seule dépendance externe. La démonstration ne nécessite ni téléchargement de données, ni clé API, ni matériel. Sortie JSON : [exemple enregistré](example_output.json).

## Méthode et interface

Noyaux de Sobel 3x3 avec réplication des bords. Entrée : matrice grise finie (H,W). Sortie : amplitude et masque booléen. Seuil relatif au maximum du gradient.

Depuis le dossier de ce projet :

```python
import numpy as np
from main import *
result = sobel(np.eye(10), threshold=.25)
print(result)
```

## Vérification

[test_main.py](test_main.py) vérifie des cas numériques de référence, les cas limites et les entrées invalides. Exécuter la commande ci-dessus ou `python run_tests.py` à la racine.

## Périmètre et limites

Sans débruitage, suppression des non-maxima, hystérésis Canny ni codecs image. Images personnalisées au format .npy.

Implémentation pédagogique réalisée avec assistance IA pour le portfolio de Rafik AMIRI. Nouveau projet d’apprentissage, sans revendication d’expérience professionnelle, de participation à une compétition ou de déploiement en production. Relire et comprendre le code avant de le présenter.
