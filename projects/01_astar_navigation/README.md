# A* Autonomous Robot Navigation

[Documentation française](README.fr.md)

Plan a shortest collision-free path on a binary occupancy grid.

## Run from the repository root

```bash
python -m pip install -r projects/01_astar_navigation/requirements.txt
python projects/01_astar_navigation/main.py
python projects/01_astar_navigation/test_main.py
```

Python 3.10+; NumPy is the only external dependency. The default demonstration needs no downloads, API keys or hardware. It prints JSON. See [recorded example](example_output.json).

## Method and API

A* uses Manhattan distance, unit edge costs and four-connected neighbors. Returns a list of (row, column) cells, or [] if unreachable.

From this project's directory:

```python
import numpy as np
from main import *
result = astar([[0,0],[1,0]], (0,0), (1,1))
print(result)
```

## Validation

[test_main.py](test_main.py) contains independently checked numerical cases, boundary behavior and invalid-input checks. Run the command above or `python run_tests.py` at repository root.

## Scope and limits

Static grid only; no robot dynamics, localization, footprint inflation or moving obstacles.

AI-assisted educational implementation prepared for Rafik AMIRI's portfolio. This is a new learning project, not a claim of prior employment, competition participation or production deployment. Review and understand the code before presenting it.
