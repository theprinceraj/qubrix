from pathlib import Path

from f1_functions import load_tests

for file_path in (Path(__file__).parent / "data").glob("*.json"):
    try:
        tests = load_tests(file_path)
        print(f"LOADED {file_path.name}: {len(tests)} cases")
    except (FileNotFoundError, ValueError, TypeError) as e:
        print(f"SKIPPED {file_path.name}: {e}")
