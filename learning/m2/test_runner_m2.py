import time
from pathlib import Path

from learning.m1.runner import run_file

MARKER = Path("/tmp/qubrix_orphan_marker")


def test_no_orphan_after_timeout():
    MARKER.unlink(missing_ok=True)
    result = run_file(Path(__file__).parent / "samples" / "spawner.py", timeout=1)
    assert result["timed_out"] == True
    time.sleep(3)
    assert not MARKER.exists()


def test_no_cpu_burn():
    result = run_file(Path(__file__).parent / "samples" / "cpu_burn.py")
    assert result["returncode"] == -24
    assert result["timed_out"] == False


def test_handle_memory_hog_safely():
    result = run_file(Path(__file__).parent / "samples" / "memory_hog.py")
    assert result["returncode"] == 1
    assert "MemoryError" in result["stderr"]


def test_handle_unauthorized_big_creation():
    result = run_file(Path(__file__).parent / "samples" / "big_file.py")
    assert result["returncode"] == 1
    assert "File too large" in result["stderr"]
