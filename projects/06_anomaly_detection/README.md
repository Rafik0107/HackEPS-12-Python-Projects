# Industrial Anomaly Detection

[Documentation française](README.fr.md)

Flag unusual feature values using a robust normal-data baseline.

## Run from the repository root

```bash
python -m pip install -r projects/06_anomaly_detection/requirements.txt
python projects/06_anomaly_detection/main.py
python projects/06_anomaly_detection/test_main.py
```

Python 3.10+; NumPy is the only external dependency. The default demonstration needs no downloads, API keys or hardware. It prints JSON. See [recorded example](example_output.json).

## Method and API

Fit median and 1.4826*MAD on normal training samples only. Score is the maximum absolute standardized deviation. Constant-feature scale is floored at 1e-9. Input shape: (samples, features).

From this project's directory:

```python
import numpy as np
from main import *
result = RobustDetector().fit([[-1.],[0.],[1.]]).predict([[0.],[10.]])
print(result)
```

## Validation

[test_main.py](test_main.py) contains independently checked numerical cases, boundary behavior and invalid-input checks. Run the command above or `python run_tests.py` at repository root.

## Scope and limits

Independent-feature rule; ignores correlations and drift. Threshold is not a calibrated probability. Constant features are highly sensitive to changes. Synthetic evaluation only.

AI-assisted educational implementation prepared for Rafik AMIRI's portfolio. This is a new learning project, not a claim of prior employment, competition participation or production deployment. Review and understand the code before presenting it.
