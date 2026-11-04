import json
from json.decoder import JSONDecodeError
from pathlib import Path


def run_tests(func, tests):
    total = len(tests)
    if total < 1:
        raise ValueError("This test dataset is empty")

    passes = fails = errors = bad_tests = 0

    numbered_tests = enumerate(tests, 1)
    for i, test in numbered_tests:
        try:
            a, b = test["input"]
            expected = test["expected"]
        except Exception as e:
            print(f"Test {i}: BAD TEST - {type(e).__name__}: {e}")
            bad_tests += 1
            continue

        try:
            res = func(a, b)
        except Exception as e:
            print(f"Test {i}: ERROR - {type(e).__name__}: {e}")
            errors += 1
            continue

        if res == expected:
            print(f"Test {i}: PASS")
            passes += 1
        else:
            print(
                f"Test {i}: FAIL - Input:{', '.join(map(str, test['input']))} | Expected Out:{expected}, Actual Out:{res}"
            )
            fails += 1

    result = {
        "passes": passes,
        "fails": fails,
        "errors": errors,
        "bad_tests": bad_tests,
    }

    # Old version, kept for learning: a manual loop. Replaced by the built-in
    # sum() below. Same result, less code, and no loop variable to name.
    # deferred_total = 0
    # for i in result.values():
    #     deferred_total += i
    deferred_total = sum(result.values(), 0)

    assert deferred_total == total, (
        f"ERROR: Expected total({total}) and actual total({deferred_total}) are unequal"
    )
    return {**result, "total": total}


def load_tests(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Test dataset not found at '{path}'") from e
    except JSONDecodeError as e:
        raise ValueError(
            f"Provided dataset '{Path(path).name}' is not a valid JSON file"
        ) from e

    if not isinstance(data, list):
        raise TypeError(f"Provided dataset in '{Path(path).name}' is not a list")

    return data


def add(a, b):
    return a + b


def multiply(a, b):
    return a * b


if __name__ == "__main__":
    add_tests = load_tests(Path(__file__).parent / "data" / "add_tests.json")

    multiply_tests = [
        {"input": [4, 3], "expected": 12},
        {"input": [3, 9], "expected": 27},
        {"input": [11, 1], "expected": 12},
        {"input": ["hello", "bro"], "expected": 12},
        {"input": "hello", "expected": 12},
        {"input": [1, 2, 3], "expected": 6},
        {"input": [1, 2]},
    ]
    results = run_tests(add, add_tests)
    print(
        f"ADD: {results['passes']} passed, {results['fails']} failed, {results['errors']} errored, {results['bad_tests']} bad tests out of total {results['total']}\n"
    )

    results = run_tests(multiply, multiply_tests)
    print(
        f"MULTIPLY: {results['passes']} passed, {results['fails']} failed, {results['errors']} errored, {results['bad_tests']} bad tests out of total {results['total']}\n"
    )

    # run_tests(add, []) # Intentional Failure
