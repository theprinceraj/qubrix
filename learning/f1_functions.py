def run_tests(func, tests):
    passes = 0
    total = len(tests)
    numbered_tests = enumerate(tests, 1)
    for i, test in numbered_tests:
        try:
            a, b = test["input"]
            expected = test["expected"]
        except Exception as e:
            print(f"Test {i}: BAD TEST - {type(e).__name__}: {e}")
            continue
        try:
            res = func(a, b)
        except Exception as e:
            print(f"Test {i}: ERROR - {type(e).__name__}: {e}")
            continue
        if res == expected:
            print(f"Test {i}: PASS")
            passes += 1
        else:
            print(
                f"Test {i}: FAIL - Input:{', '.join(map(str, test['input']))} | Expected Out:{expected}, Actual Out:{res}"
            )
    return total, passes


def add(a, b):
    return a + b


def multiply(a, b):
    return a * b


add_tests = [
    {"input": [2, 3], "expected": 5},
    {"input": [4, 3], "expected": 9},
    {"input": [11, 1], "expected": 12},
]

multiply_tests = [
    {"input": [4, 3], "expected": 12},
    {"input": [3, 9], "expected": 27},
    {"input": [11, 1], "expected": 12},
]

total, passes = run_tests(add, add_tests)
print(f"ADD: {passes}/{total} passed\n")

total, passes = run_tests(multiply, multiply_tests)
print(f"MULTIPLY: {passes}/{total} passed\n")
