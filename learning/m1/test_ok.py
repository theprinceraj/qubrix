from pathlib import Path

from learning.m1.runner import run_file


def test_returncode_zero():
    result = run_file(Path(__file__).parent / "samples" / "ok.py")
    assert result["returncode"] == 0
    assert result["timed_out"] == False


if __name__ == "__main__":
    test_returncode_zero()
