from pathlib import Path

from learning.m1.runner import run_file


def test_crash():
    result = run_file(Path(__file__).parent / "samples" / "crash.py")
    assert result["returncode"] == 1
    assert "Traceback" in result["stderr"]


if __name__ == "__main__":
    test_crash()
