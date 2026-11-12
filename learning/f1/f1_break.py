from f1_functions import run_tests


def div(a, b):
    return a / b


div_tests = [
    {"input": [4, 2], "expected": 2},
    {"input": 5, "expected": 1},
]

total, passes = run_tests(div, div_tests)
print(f"DIVISION: {passes}/{total} passed")
