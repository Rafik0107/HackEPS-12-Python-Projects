# Kalman Filter Sensor Tracking

[Documentation française](README.fr.md)

Estimate position and velocity from noisy scalar position measurements.

## Run from the repository root

```bash
python -m pip install -r projects/03_kalman_tracking/requirements.txt
python projects/03_kalman_tracking/main.py
python projects/03_kalman_tracking/test_main.py
```

Python 3.10+; NumPy is the only external dependency. The default demonstration needs no downloads, API keys or hardware. It prints JSON. See [recorded example](example_output.json).

## Method and API

Constant-velocity state model with discrete random acceleration; Joseph covariance update. NaN skips measurement correction. Returns estimates (N,2) and covariances (N,2,2). dt is in seconds; noise variances must use consistent units.

From this project's directory:

```python
import numpy as np
from main import *
result = track([0., 1.1, 1.9, 3.2])
print(result)
```

## Validation

[test_main.py](test_main.py) contains independently checked numerical cases, boundary behavior and invalid-input checks. Run the command above or `python run_tests.py` at repository root.

## Scope and limits

Linear one-dimensional motion and specified noise statistics; no outlier rejection or nonlinear tracking.

AI-assisted educational implementation prepared for Rafik AMIRI's portfolio. This is a new learning project, not a claim of prior employment, competition participation or production deployment. Review and understand the code before presenting it.
