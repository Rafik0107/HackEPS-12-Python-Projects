# Industrial Production Scheduler

[Documentation française](README.fr.md)

Assign independent jobs to identical parallel machines.

## Run from the repository root

```bash
python -m pip install -r projects/09_production_scheduler/requirements.txt
python projects/09_production_scheduler/main.py
python projects/09_production_scheduler/test_main.py
```

Python 3.10+; NumPy is the only external dependency. The default demonstration needs no downloads, API keys or hardware. It prints JSON. See [recorded example](example_output.json).

## Method and API

Longest Processing Time first (LPT): sort descending duration, then assign to the least-loaded machine. Output includes job intervals, makespan and a simple lower bound. All durations use the same unit.

From this project's directory:

```python
import numpy as np
from main import *
result = schedule({'job_a': 5, 'job_b': 3, 'job_c': 2}, machines=2)
print(result)
```

## Validation

[test_main.py](test_main.py) contains independently checked numerical cases, boundary behavior and invalid-input checks. Run the command above or `python run_tests.py` at repository root.

## Scope and limits

Heuristic, not guaranteed optimal; jobs are independent and non-preemptive. No precedence, release dates, setups, due dates or heterogeneous machines.

AI-assisted educational implementation prepared for Rafik AMIRI's portfolio. This is a new learning project, not a claim of prior employment, competition participation or production deployment. Review and understand the code before presenting it.
