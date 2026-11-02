# Biomedical ECG Signal Analysis

[English documentation](README.md)

Mesurer intervalles entre pics et fréquence sur des signaux ECG synthétiques.

## Exécution depuis la racine du dépôt

```bash
python -m pip install -r projects/11_ecg_analysis/requirements.txt
python projects/11_ecg_analysis/main.py
python projects/11_ecg_analysis/test_main.py
```

Python 3.10+ ; NumPy est la seule dépendance externe. La démonstration ne nécessite ni téléchargement de données, ni clé API, ni matériel. Sortie JSON : [exemple enregistré](example_output.json).

## Méthode et interface

Générateur : impulsions gaussiennes de type P/R/T et bruit. Détecteur : maxima positifs au-dessus d’un seuil absolu, puis période réfractaire. Renvoie indices, RR en secondes et fréquence moyenne ; None sans deux pics.

Depuis le dossier de ce projet :

```python
import numpy as np
from main import *
result = analyze(synthetic_ecg(bpm=72)[1])
print(result)
```

## Vérification

[test_main.py](test_main.py) vérifie des cas numériques de référence, les cas limites et les entrées invalides. Exécuter la commande ci-dessus ou `python run_tests.py` à la racine.

## Périmètre et limites

Signaux synthétiques pédagogiques uniquement. Sans validation clinique, diagnostic ni dispositif médical. Sans interprétation des arythmies, correction de ligne de base ni QRS inversé.

Implémentation pédagogique réalisée avec assistance IA pour le portfolio de Rafik AMIRI. Nouveau projet d’apprentissage, sans revendication d’expérience professionnelle, de participation à une compétition ou de déploiement en production. Relire et comprendre le code avant de le présenter.
