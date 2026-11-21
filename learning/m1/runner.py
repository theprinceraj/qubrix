import os
import signal
import subprocess
import sys
from pathlib import Path

ENGINE_TIMEOUT = 5


def run_file(path, timeout=ENGINE_TIMEOUT):
    with subprocess.Popen(
        [sys.executable, path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        errors="backslashreplace",
        start_new_session=True,
    ) as p:
        try:
            out, err = p.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(p.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            out, err = p.communicate()  # drain pipes+reaps; gives partial output
            return {
                "returncode": 124,
                "stdout": out,
                "stderr": err,
                "timed_out": True,
            }

    return {
        "returncode": p.returncode,
        "stdout": out,
        "stderr": err,
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
