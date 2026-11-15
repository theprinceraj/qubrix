import subprocess
import sys
from pathlib import Path


def run_file(path):
    obj = subprocess.run(
        [sys.executable, path], check=False, capture_output=True, text=True
    )

    return {"returncode": obj.returncode, "stdout": obj.stdout, "stderr": obj.stderr}


if __name__ == "__main__":
    for file_name in ("crash.py", "ok.py", "three.py"):
        print(run_file(Path(__file__).parent / "samples" / file_name))
