import inspect
import logging
import sys
from pathlib import Path
from types import FunctionType

import f1_functions

file_handler = logging.FileHandler(
    Path(__file__).parent / "run.log", mode="a", encoding="utf-8"
)
stdout_handler = logging.StreamHandler(sys.stdout)

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    handlers=[file_handler, stdout_handler],
)

net_total = net_passes = net_fails = net_errors = net_bad_tests = net_skips = 0

for file_path in (Path(__file__).parent / "data").glob("*.json"):
    try:
        tests = f1_functions.load_tests(file_path)

        file_name = file_path.name
        fn_name = file_name.split("_")[0]

        if fn_name not in f1_functions.__dict__:
            logger.warning(
                f"SKIPPED {file_path.name}: No function named {fn_name} found"
            )
            net_skips += 1
            continue

        fn = getattr(f1_functions, fn_name)
        if not isinstance(fn, FunctionType):
            logger.warning(
                f"SKIPPED {file_path.name}: '{fn_name}' not a valid function name"
            )
            net_skips += 1
            continue
        # Because we are deriving fn names from file names, it is required to ensure that no unintention functions are run and hence the following check
        if len(inspect.signature(fn).parameters.values()) != 2:
            logger.warning(
                f"SKIPPED {file_path.name}: '{fn_name}' function has invalid signature, expected only 2 arguments"
            )
            net_skips += 1
            continue

        logger.info(f"LOADED {file_path.name}: {len(tests)} cases")

        net_total += len(tests)

        result = f1_functions.run_tests(fn, tests)
        net_passes += result["passes"]
        net_fails += result["fails"]
        net_errors += result["errors"]
        net_bad_tests += result["bad_tests"]

    except (FileNotFoundError, ValueError, TypeError) as e:
        logger.error(f"SKIPPED {file_path.name}: {e}")
        net_skips += 1

print(
    f"NET RESULTS:\n PASS: {net_passes}, FAILS: {net_fails}, ERRORS: {net_errors}, BAD TESTS: {net_bad_tests}, NET SKIPS: {net_skips}\n TOTAL: {net_total}"
)
