import os
import resource
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

ENGINE_TIMEOUT = 5


def run_file(path, timeout=ENGINE_TIMEOUT):
    def set_child_limits():
        resource.setrlimit(resource.RLIMIT_CPU, (1, 2))
        resource.setrlimit(resource.RLIMIT_AS, (256 * 1024 * 1024, 256 * 1024 * 1024))
        resource.setrlimit(resource.RLIMIT_FSIZE, (1024 * 1024, 1024 * 1024))

    resolved_path = Path.resolve(path)

    with (
        tempfile.TemporaryDirectory() as tmpdir,
        subprocess.Popen(
            [sys.executable, resolved_path],
            cwd=tmpdir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            errors="backslashreplace",
            start_new_session=True,
            preexec_fn=set_child_limits,
        ) as p,
    ):
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
