# Advanced PID Control Simulator

[Documentation française](README.fr.md)

Study a saturated PID controller on a first-order plant.

## Run from the repository root

```bash
python -m pip install -r projects/02_pid_control/requirements.txt
python projects/02_pid_control/main.py
python projects/02_pid_control/test_main.py
```

Python 3.10+; NumPy is the only external dependency. The default demonstration needs no downloads, API keys or hardware. It prints JSON. See [recorded example](example_output.json).

## Method and API

The plant is tau*y' + y = u. Derivative is filtered and applied to measurement; conditional integration reduces windup. Returns time, output and control arrays. Time is in seconds, output/control in normalized units.

From this project's directory:

```python
import numpy as np
from main import *
result = simulate(kp=2., ki=1., kd=.1)
print(result)
```

## Validation

[test_main.py](test_main.py) contains independently checked numerical cases, boundary behavior and invalid-input checks. Run the command above or `python run_tests.py` at repository root.

## Scope and limits

Educational SISO plant; no automatic tuning, stability certificate, transport delay or hardware validation.

AI-assisted educational implementation prepared for Rafik AMIRI's portfolio. This is a new learning project, not a claim of prior employment, competition participation or production deployment. Review and understand the code before presenting it.
