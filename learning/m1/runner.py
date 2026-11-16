import subprocess
import sys
from pathlib import Path

ENGINE_TIMEOUT = 5


def run_file(path, timeout=ENGINE_TIMEOUT):
    try:
        obj = subprocess.run(
            [sys.executable, path],
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as e:
        return {
            "returncode": 124,
            "stdout": e.stdout.decode("utf-8") if e.stdout is not None else "",
            "stderr": e.stderr.decode("utf-8") if e.stderr is not None else "",
            "timed_out": True,
        }

    return {
        "returncode": obj.returncode,
        "stdout": obj.stdout,
        "stderr": obj.stderr,
        "timed_out": False,
    }


if __name__ == "__main__":
    for file_name in (
        "crash.py",
        "ok.py",
        "three.py",
        "loop.py",
        "sleep.py",
    ):
        print(run_file(Path(__file__).parent / "samples" / file_name, 2), "\n")
