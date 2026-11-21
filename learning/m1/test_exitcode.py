from pathlib import Path

from learning.m1.runner import run_file


def test_exitcode():
    result = run_file(Path(__file__).parent / "samples" / "three.py")
    assert result["returncode"] == 3


if __name__ == "__main__":
    test_exitcode()
