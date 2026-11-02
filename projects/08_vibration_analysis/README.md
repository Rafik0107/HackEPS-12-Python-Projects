# Mechanical Vibration Analysis

[Documentation française](README.fr.md)

Simulate free vibrations and estimate the dominant frequency.

## Run from the repository root

```bash
python -m pip install -r projects/08_vibration_analysis/requirements.txt
python projects/08_vibration_analysis/main.py
python projects/08_vibration_analysis/test_main.py
```

Python 3.10+; NumPy is the only external dependency. The default demonstration needs no downloads, API keys or hardware. It prints JSON. See [recorded example](example_output.json).

## Method and API

Mass-spring-damper m*x'' + c*x' + k*x = 0 integrated by RK4. Returns seconds, (displacement, velocity), and energy. SI units: kg, N/m, N*s/m, m. FFT uses a Hann window and excludes DC.

From this project's directory:

```python
import numpy as np
from main import *
result = simulate(mass=1., stiffness=100., damping=.4)
print(result)
```

## Validation

[test_main.py](test_main.py) contains independently checked numerical cases, boundary behavior and invalid-input checks. Run the command above or `python run_tests.py` at repository root.

## Scope and limits

One linear degree of freedom, no forcing or modal structure. FFT resolution is approximately 1/duration; peak may be unreliable for heavily damped responses.

AI-assisted educational implementation prepared for Rafik AMIRI's portfolio. This is a new learning project, not a claim of prior employment, competition participation or production deployment. Review and understand the code before presenting it.
