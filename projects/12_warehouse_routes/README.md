# Smart Warehouse Route Optimization

[Documentation française](README.fr.md)

Find a minimum closed picking tour through a small obstacle grid.

## Run from the repository root

```bash
python -m pip install -r projects/12_warehouse_routes/requirements.txt
python projects/12_warehouse_routes/main.py
python projects/12_warehouse_routes/test_main.py
```

Python 3.10+; NumPy is the only external dependency. The default demonstration needs no downloads, API keys or hardware. It prints JSON. See [recorded example](example_output.json).

## Method and API

BFS constructs obstacle-aware shortest paths, then Held-Karp dynamic programming optimizes the visit order. Returns order, cell-by-cell path and distance in grid moves. At most 12 picks.

From this project's directory:

```python
import numpy as np
from main import *
result = optimize(np.zeros((5,5)), (0,0), [(1,2),(4,4)])
print(result)
```

## Validation

[test_main.py](test_main.py) contains independently checked numerical cases, boundary behavior and invalid-input checks. Run the command above or `python run_tests.py` at repository root.

## Scope and limits

Exact for this static unit-cost grid model only. Exponential complexity; no capacities, multiple vehicles, time windows or dynamic congestion. May pass another pick en route.

AI-assisted educational implementation prepared for Rafik AMIRI's portfolio. This is a new learning project, not a claim of prior employment, competition participation or production deployment. Review and understand the code before presenting it.
