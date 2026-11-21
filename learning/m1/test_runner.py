import time
from pathlib import Path

from learning.m1.runner import run_file


def test_badbytes_does_not_crash_engine():
    result = run_file(Path(__file__).parent / "samples" / "badbytes.py")
    assert result["timed_out"] == False


def test_badbytes_timeout_does_not_crash_engine():
    result = run_file(Path(__file__).parent / "samples" / "badbytes_loop.py", timeout=1)
    assert result["timed_out"] == True
    assert "\\xff" in result["stdout"]


def test_loop_is_bounded():
    start = time.monotonic()
    result = run_file(Path(__file__).parent / "samples" / "loop.py", timeout=1)
    elapsed = time.monotonic() - start
    assert result["timed_out"] == True
    assert "started" in result["stdout"]
    assert elapsed < 2


if __name__ == "__main__":
    test_badbytes_does_not_crash_engine()
