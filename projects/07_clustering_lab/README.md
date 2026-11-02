# Machine Learning Clustering Laboratory

[Documentation française](README.fr.md)

Explore reproducible k-means clustering.

## Run from the repository root

```bash
python -m pip install -r projects/07_clustering_lab/requirements.txt
python projects/07_clustering_lab/main.py
python projects/07_clustering_lab/test_main.py
```

Python 3.10+; NumPy is the only external dependency. The default demonstration needs no downloads, API keys or hardware. It prints JSON. See [recorded example](example_output.json).

## Method and API

K-means++ initialization and Lloyd updates; returns labels, centers and inertia history. Empty centers are retained. Seed controls randomness; max_iter bounds computation.

From this project's directory:

```python
import numpy as np
from main import *
result = kmeans([[-2.,-2.],[-1.9,-2.],[2.,2.],[2.1,2.]], k=2)
print(result)
```

## Validation

[test_main.py](test_main.py) contains independently checked numerical cases, boundary behavior and invalid-input checks. Run the command above or `python run_tests.py` at repository root.

## Scope and limits

Local optimum, Euclidean distance, no automatic scaling or choice of k. Standardize unlike units before fitting.

AI-assisted educational implementation prepared for Rafik AMIRI's portfolio. This is a new learning project, not a claim of prior employment, competition participation or production deployment. Review and understand the code before presenting it.
