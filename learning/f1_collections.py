def add(a, b):
    return a + b


tests = [
    {"input": [2, 3], "expected": 5},
    {"input": [4, 3], "expected": 9},
    {"input": [11, 1], "expected": 12},
]

passes = 0
total = len(tests)

numberedTests = enumerate(tests, 1)

for i, test in numberedTests:
    a, b = test["input"]
    res = add(a, b)
    if res == test["expected"]:
        print(f"Test {i}: PASS")
        passes += 1
    else:
        print(
            f"Test {i}: FAIL - Input:{', '.join(map(str, test['input']))} | Expected Out:{test['expected']}, Actual Out:{res}"
        )

print(f"{passes}/{total} passed")
