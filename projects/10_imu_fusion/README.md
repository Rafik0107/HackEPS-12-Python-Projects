# IMU Sensor Fusion

[Documentation française](README.fr.md)

Estimate one roll angle by combining gyroscope and accelerometer.

## Run from the repository root

```bash
python -m pip install -r projects/10_imu_fusion/requirements.txt
python projects/10_imu_fusion/main.py
python projects/10_imu_fusion/test_main.py
```

Python 3.10+; NumPy is the only external dependency. The default demonstration needs no downloads, API keys or hardware. It prints JSON. See [recorded example](example_output.json).

## Method and API

Complementary filter with wrapped angular innovations. Gyro input shape (N,) is rad/s; acceleration shape (N,3) uses a consistent unit with positive z at zero roll. Returns radians. Sampling is uniform.

From this project's directory:

```python
import numpy as np
from main import *
result = fuse(np.zeros(100), np.tile([0.,0.,1.], (100,1)))
print(result)
```

## Validation

[test_main.py](test_main.py) contains independently checked numerical cases, boundary behavior and invalid-input checks. Run the command above or `python run_tests.py` at repository root.

## Scope and limits

Single-axis quasi-static orientation only, not a full 3D AHRS. Linear acceleration corrupts the gravity estimate; no bias calibration or magnetic heading.

AI-assisted educational implementation prepared for Rafik AMIRI's portfolio. This is a new learning project, not a claim of prior employment, competition participation or production deployment. Review and understand the code before presenting it.
