# Robotic Arm Kinematics Simulator

[Documentation française](README.fr.md)

Compute forward/inverse kinematics and a Jacobian for a planar arm.

## Run from the repository root

```bash
python -m pip install -r projects/04_arm_kinematics/requirements.txt
python projects/04_arm_kinematics/main.py
python projects/04_arm_kinematics/test_main.py
```

Python 3.10+; NumPy is the only external dependency. The default demonstration needs no downloads, API keys or hardware. It prints JSON. See [recorded example](example_output.json).

## Method and API

Two revolute links; inverse returns both elbow configurations in radians. Link lengths and Cartesian targets share the same length unit. At the folded origin, returns one representative solution.

From this project's directory:

```python
import numpy as np
from main import *
result = inverse(1.2, .6, l1=1., l2=1.)
print(result)
```

## Validation

[test_main.py](test_main.py) contains independently checked numerical cases, boundary behavior and invalid-input checks. Run the command above or `python run_tests.py` at repository root.

## Scope and limits

No joint limits, collisions, dynamics, trajectory controller or 3D geometry. Singular configurations are not avoided.

AI-assisted educational implementation prepared for Rafik AMIRI's portfolio. This is a new learning project, not a claim of prior employment, competition participation or production deployment. Review and understand the code before presenting it.
