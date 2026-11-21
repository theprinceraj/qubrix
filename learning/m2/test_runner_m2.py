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
