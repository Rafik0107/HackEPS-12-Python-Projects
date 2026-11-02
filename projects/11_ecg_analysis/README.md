# Biomedical ECG Signal Analysis

[Documentation française](README.fr.md)

Measure peak intervals and heart rate on synthetic ECG-like signals.

## Run from the repository root

```bash
python -m pip install -r projects/11_ecg_analysis/requirements.txt
python projects/11_ecg_analysis/main.py
python projects/11_ecg_analysis/test_main.py
```

Python 3.10+; NumPy is the only external dependency. The default demonstration needs no downloads, API keys or hardware. It prints JSON. See [recorded example](example_output.json).

## Method and API

Generator combines Gaussian P/R/T-like pulses and noise. Detector selects positive local maxima above an absolute threshold, then enforces a refractory interval. Returns peak indices, RR seconds and mean rate; rate is None without two peaks.

From this project's directory:

```python
import numpy as np
from main import *
result = analyze(synthetic_ecg(bpm=72)[1])
print(result)
```

## Validation

[test_main.py](test_main.py) contains independently checked numerical cases, boundary behavior and invalid-input checks. Run the command above or `python run_tests.py` at repository root.

## Scope and limits

Synthetic educational signals only. Not clinically validated, not diagnostic, not a medical device. No arrhythmia interpretation, baseline correction or inverted-QRS support.

AI-assisted educational implementation prepared for Rafik AMIRI's portfolio. This is a new learning project, not a claim of prior employment, competition participation or production deployment. Review and understand the code before presenting it.
