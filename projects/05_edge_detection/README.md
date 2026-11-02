# Computer Vision Edge Detection

[Documentation française](README.fr.md)

Extract Sobel gradient magnitudes and thresholded edges.

## Run from the repository root

```bash
python -m pip install -r projects/05_edge_detection/requirements.txt
python projects/05_edge_detection/main.py
python projects/05_edge_detection/test_main.py
```

Python 3.10+; NumPy is the only external dependency. The default demonstration needs no downloads, API keys or hardware. It prints JSON. See [recorded example](example_output.json).

## Method and API

3x3 Sobel kernels with replicated boundary pixels. Input: finite grayscale (H,W) array. Output: magnitude and Boolean edge mask. Threshold is a fraction of maximum gradient magnitude.

From this project's directory:

```python
import numpy as np
from main import *
result = sobel(np.eye(10), threshold=.25)
print(result)
```

## Validation

[test_main.py](test_main.py) contains independently checked numerical cases, boundary behavior and invalid-input checks. Run the command above or `python run_tests.py` at repository root.

## Scope and limits

No denoising, non-maximum suppression, Canny hysteresis or image codec support. Uses .npy arrays for custom images.

AI-assisted educational implementation prepared for Rafik AMIRI's portfolio. This is a new learning project, not a claim of prior employment, competition participation or production deployment. Review and understand the code before presenting it.
