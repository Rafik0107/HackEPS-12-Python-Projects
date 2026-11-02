"""Run every project suite in an isolated subprocess."""
from pathlib import Path
import subprocess
import sys

root = Path(__file__).parent
failed = []
for test in sorted((root / "projects").glob("*/test_main.py")):
    print("\n" + test.parent.name, flush=True)
    if subprocess.run([sys.executable, str(test)]).returncode:
        failed.append(test.parent.name)
print("\n" + ("FAILED: " + ", ".join(failed) if failed else "All 12 project suites passed."))
sys.exit(bool(failed))
