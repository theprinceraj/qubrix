# PROGRESS.md — Qubrix learning & build log

Maintained by the agent at the end of every meaningful session (see `AGENTS.md` §4 Step 8 and §9).
Attribution labels (`[SOLO]` `[GUIDED]` `[PAIRED]` `[AGENT]`) and skill levels (0–4) are defined in `AGENTS.md` §0.
**Rule:** skill levels only rise on evidence from the learner's own work. `[AGENT]` work never raises a level.

---

## Current status

| Field | Value |
|---|---|
| Current milestone | **M1 — Local Python execution engine** (started 2026-11-15). F1 ✅ 2026-11-05, F2 ✅ 2026-11-15, F3 folded into M1 |
| Active task | **M1.3 (TBD, assign next session)** — decide next M1 slice (e.g. missing/unrunnable file behavior as a candidate result, or separating wall-clock timeout concerns). M1.1 ✅, M1.2 ✅ |
| Parallel task | none. Ubuntu installed and set as default WSL distro (verified) |
| Last session | 2026-11-16 |
| Open decisions | Product definition (draft below) — learner to confirm; weekly time budget unknown |

## Current assignment

**Pace change 2026-11-15 (learner request: "increase speed"):** one combined task per step instead of many micro-steps; one prediction block per task (not per command); shorter explanations; F2 closes with this task, F3 (venv, type hints, pytest) is folded into M1 just-in-time. Next after `run.sh`: **M1 — Python runner with `subprocess`**.

**Next (M1.3, not yet assigned):** pick the next M1 slice in the next session. Candidates: define/implement behavior for a missing or non-.py path as a *candidate result* (observe `python3`’s own exit/stderr through the normal path, no pre-check), or introduce basic tests/type hints around `run_file` (F3 folded in). Assign with predictions + acceptance criteria before coding.

**M1.2 ✅ 2026-11-16** `[GUIDED]`: `run_file(path, timeout)` in `learning/m1/runner.py` catches only `subprocess.TimeoutExpired`, returns `returncode/stdout/stderr/timed_out`. Samples added: `learning/m1/samples/loop.py` (`print("started", flush=True); while True: pass`) and `learning/m1/samples/sleep.py`. Timeout path normalizes output to `str` (decodes bytes, empty stream → `""`) so partial stdout (`"started\n"`) is preserved and types match normal runs. `returncode` on timeout set to `124` (engine sentinel, conventional) with `timed_out` as the primary signal. `__main__` runs 5 cases (`crash, ok, three, loop, sleep`) with `timeout=2`; `time` ~4.3s real. Learner implemented; agent reviewed (spec gaps: extra missing-file pre-check, bytes/None on timeout, consistency). Understanding check: broad `except` can hide engine bugs; checking only `returncode==124` can misclassify a program that exits 124. Minor open point: prediction 1 overstated "SIGKILL right away" without a precise doc quote for `subprocess.run` timeout behavior.

**M1.1 ✅ 2026-11-16** `[GUIDED]`: `learning/m1/runner.py` `run_file(path)` → dict `returncode`/`stdout`/`stderr` via `subprocess.run([sys.executable, path], capture_output=True, text=True, check=False)`. Needed the task split into two steps and a clarification that inherited stdout/stderr went straight to the terminal. Predictions (0/3/1, traceback in stderr) all right. First version built the dict in the caller; moved it into `run_file` after the interface argument. Ran the `check=True` experiment (loop dies at `crash.py`, other files never run). "Why" took two prompts: first a general rule ("useful if we want the engine to fail"), then "our engine failed because it didn't check other codes" (the consequence). Agent revealed the rule: the candidate's failure is a result, not an engine error (hint level 5).

**F2 closed 2026-11-15** with `~/f2/run.sh` `[GUIDED]`: usage on stderr + exit 2, `python3 "$1"`, `status=$?`, prints and forwards the status. Predictions for crash (1) and three (3) written before running, both right.

## Assignment history (F1, closed 2026-11-05)

**F1.3 — Exceptions** (Category A, learner implements).
- Pre-check done by experiment in `learning/f1_break.py`. Learner classified: `"inputs"` typo / `"input": 5` / missing `"expected"` are the test's fault; `div` by 0 is the function's fault. Reads tracebacks bottom-up with guidance.
- **F1.3a ✅ 2026-11-02:** `try` wraps only `func(a, b)`. Prints `Test 1: ERROR - ZeroDivisionError: division by zero`, then `continue`, so later tests still run. Needed hint level 4 for `type(e).__name__` / `{e}`. Nit: uses `e.__str__()` where `{e}` is idiomatic.
- **F1.3b ✅ 2026-11-02:** a second `try` reads `input` and `expected` *before* calling `func`, and prints `BAD TEST - <Type>: <msg>`, then `continue`. Renamed `res` to `expected` (one variable, one meaning). Learned that Python has no block scope (compared it to JS `var` vs `let`). Experiment without `continue` showed a broken test graded with leftover values from the previous test, which gave a false PASS (`2/2 passed`). Learner explained it in their own words: the failed assignment never happened, so the old values stayed.
- **F1.3c ✅ 2026-11-04:** `run_tests` counts passes/fails/errors/bad_tests separately and returns a dict. Test data now hits every status (missing key, misspelled key, 3 inputs, string instead of list, crashing `"hello" + 5`). First caller unpacked `.values()` positionally, which threw away the dict's safety; learner explained that reordering keys would silently swap counts ("worse for code that judges code") and switched to key access. Added `assert sum(result.values()) == total`. Learner explained why summing the dict covers future statuses automatically. Deliberate-break test of the assert: learner says it was done; **agent did not see the output**.
- **F1 logging ✅ 2026-11-05** `[GUIDED]`: `logging` replaces `print` in `f1_loop.py` and `f1_functions.py`. Level rule the learner set: INFO = nothing to fix (LOADED, PASS, FAIL, candidate crash); WARNING = run carried on, something looks off (sort signature skip); ERROR = someone must fix the dataset (BAD TEST, broken.json). Learner first put BAD TEST at WARNING, then reversed it after the "does someone need to fix the dataset?" test. Learner's explanation of `__name__` was partly right: it's a string, and loggers without dots are children of the root logger, which `basicConfig` configures. Learner found the per-case lines still used `print` and moved them to the logger. Still open (not required): lazy `%s` formatting in logger calls.
- **F1 control flow ✅ 2026-11-05** `[SOLO]` (prediction without hints; `for`/`else` after `break`, `while`). **F1 data types ✅ 2026-11-05** (after one wrong prediction, `len({1,1,2})` = 2; duplicate dict keys overwrite silently, and a duplicate key inside one test case would go unnoticed by the loader).
- **F1.5b ✅ 2026-11-04** `[GUIDED]`: dataset-to-function mapping derived from the file name (`add_tests.json` → `add`). Chose derivation for this project; explicit mapping (JSON) reserved for outside callers. Learner's checks, in order: name in module → function type → exactly two parameters (via `inspect.signature`), each with a `SKIPPED` line and `continue`. Totals accumulate from `run_tests` results only; cases of skipped files are not counted. Learner found the `getattr`-before-check bug themselves in the process (twice). Limit noted: names split on the first `_`, so `run_tests` can never be reached from a dataset file. `sort_tests.json` kept as a deliberate fixture.
- **F1.5a ✅ 2026-11-04** `[GUIDED]`: `learning/f1_loop.py` loops over `data/*.json` with `Path.glob`, calls `load_tests`, catches the loader's documented exceptions in the loop and prints `SKIPPED <file>: <msg>` / `LOADED <file>: n cases`. Learner's reasoning: the loop owns the skip-or-stop policy; the loader only reports. Learner noticed glob order is alphabetical on Windows and that it doesn't matter since each line names its file. Added `if __name__ == "__main__":` guard in `f1_functions.py` so importing doesn't run the suites. First attempt had `"main"` (missing underscores): the guard silently never fired. Caught by the agent and fixed by the learner. Kept `broken.json` as a deliberate fixture and multiply's inline list as a second, comparable style.
- **F1.4 ✅ 2026-11-04** `[GUIDED]`: `load_tests(path)` loads JSON via `with open(..., encoding="utf-8")` and `json.load`. Path built from `Path(__file__).parent` so it works from any folder. Three failure modes: missing file → `FileNotFoundError` with path; invalid JSON → `ValueError` naming the file, chained `from e` (decoder message has line/column but no filename); wrong shape → `TypeError`. Learner's design: loader raises, caller's loop decides; initially wrapped with a broad `except Exception` + `isinstance`, corrected to specific `except` clauses. Learner's explain-back on the wrapping: the constructor signature is a side issue, the real reason is the missing filename. Fixture-restore error in agent's test harness was caught and fixed (fixture re-synced from git).
- **F1.3d ✅ 2026-11-04:** empty suite raises `ValueError("This test dataset is empty")` at the top of `run_tests`. Learner chose raise-inside over a caller warning; when challenged with "file #37 of 50 is empty", argued that the caller's loop should handle the exception. That's the right principle: the detector reports, the caller sets the policy. Pasted the exact traceback this time. Nit: `if total < 1` → `if not tests` (left as is). Explain-back closed 2026-11-05: validate before the loop because the check guards against wasted setup work (containers, resources in M1–M3) and against an empty dataset that signals a wrong path or broken export, which must not show as a clean run.

**F1.2 — Functions: a reusable `run_tests(func, tests)`** (Category A, learner implements)
- File: `learning/f1_functions.py` (new; keep F1.1 file as a record).
- `run_tests(func, tests)` runs every case, prints the per-case PASS/FAIL line, **returns** the pass count. The caller prints the summary.
- `run_tests` must not mention `add` anywhere. Prove reuse: add `multiply(a, b)` with its own 3 tests (one wrong) and run both through the same `run_tests`.
- snake_case names (PEP 8). No AI-written code. Docs: tutorial "Defining Functions" https://docs.python.org/3/tutorial/controlflow.html#defining-functions
- Pre-check questions: (1) `run_tests(add, tests)` vs `run_tests(add(), tests)`; (2) what does a function without `return` return?
- Acceptance: both suites run, output correct, summaries correct; learner can explain why returning beats printing inside `run_tests`.
- **Status 2026-11-02: ✅ closed.** Code correct. snake_case rename done. Explain-back is good: return lets the caller save to a DB, send to a client or build a report. Learner said a tuple is simpler but a dict is safer against positional mistakes when the return shape changes. Correctly predicted `run_tests(add, [])` → `(0, 0)`. File layout is now definitions, then data, then script code.

**F1.1 — Lists vs dictionaries** ✅ closed 2026-11-02
- File: `learning/f1_collections.py`, run with `python learning/f1_collections.py`
- Store 3 test cases for an `add(a, b)` function as a **list of dicts**, each with keys `"input"` (a list of two numbers) and `"expected"`.
- Write `add(a, b)`. Loop over the test cases, call `add` with each input, print `PASS` or `FAIL` per case, then print a summary like `2/3 passed`.
- Make one test case deliberately wrong so you see a FAIL.
- No AI-written code. Docs: <https://docs.python.org/3/tutorial/datastructures.html> (sections 5.1 and 5.5).
- Acceptance: runs without errors; output shows per-case results and correct summary; learner can explain why each test case is a dict and the collection of them is a list.
- **Status 2026-11-02:** base task done and working (`2/3 passed`).
- **F1.1b follow-up (open):** for each case, print its number, input, expected and actual value (`case 2: FAIL input=[4, 3] expected=9 got=7`). Call `add` only once per case. Docs: `enumerate`, https://docs.python.org/3/library/functions.html#enumerate. Also answer the explain-back questions: (a) a test dict is missing `"expected"`; (b) `"input": [1, 2, 3]`.

---

## Environment (checked 2026-11-01)

| Tool | Status |
|---|---|
| Windows Python | 3.14.7 installed |
| Docker | Docker Desktop 29.2.1 installed |
| Git | 2.53.0 installed; project is a git repo (branch `main`) |
| WSL2 | WSL 2.6.3. **Ubuntu installed 2026-11-02** (user `theprinceraj`). Set as default by learner (verified with `wsl -l -v`) |

---

## Product definition

> **DRAFT — proposed by the agent, learner has not confirmed.**

Qubrix is a sandboxed code-execution and evaluation platform: you submit code (written by a human or an LLM) plus a set of tests; Qubrix runs it safely in isolation with time and memory limits, and reports which tests passed. On top of that it computes benchmark metrics (e.g. pass@k) to compare how well different AI models or coding agents solve programming problems.

---

## Milestone roadmap

> **DRAFT — proposed by the agent, not yet agreed.** Revised 2026-11-01 after baseline: foundations track added before M1.

| # | Milestone | Main learning areas | Status |
|---|---|---|---|
| M0 | Project setup, baseline assessment, product scope | — | Mostly done |
| F1 | Python foundations: data types, collections, functions, control flow, files, exceptions — all applied to tiny Qubrix-flavoured exercises | Python | **Finished 2026-11-05** |
| F2 | Linux foundations in WSL Ubuntu: shell, filesystem, permissions, processes | Linux | In progress |
| F3 | Python for tooling: modules, virtual envs, type hints, first pytest tests | Python, testing | Not started |
| M1 | Local Python execution engine (`subprocess`, timeouts, output capture, exit codes) | Python, processes, signals | Not started |
| M2 | Resource limits & process termination on Linux (rlimits, process groups, kill semantics) | Linux, systems | Not started |
| M3 | Docker-isolated execution (images vs containers, Dockerfile, sandbox flags, no-network, limits) + threat model | Docker, security | Not started |
| M4 | Test runner: execute a solution against test cases, report pass/fail per case | Pytest, testing | Not started |
| M5 | Job queue & worker architecture (async, concurrency, failure handling, retries) | Async, workers, queues | Not started |
| M6 | API & persistence for submissions and results | API, DB (Category B) | Not started |
| M7 | Evaluation pipeline: datasets, LLM-generated code, pass@k | AI evaluation | Not started |
| M8 | Coding-agent benchmarking, observability, deployment | Benchmarks, infra | Not started |

---

## Skill matrix

Levels: `0 Not started` · `1 Introduced` · `2 Practised` · `3 Independent` · `4 Can defend`
Baseline set 2026-11-01 from learner self-report (Session 1).

### 1. Python engineering
| Skill | Level | Evidence |
|---|---|---|
| Fundamentals & advanced concepts | 2 | 2026-11-02: F1.2 functions as values, return vs print, tuple return `[GUIDED]`. Gaps: set vs dict literal, dict unpacking gives keys, `None` (thought "void"). Earlier: wrote F1.1 (list of dicts, loop, counter, f-string) `[GUIDED]`; correctly answered list/dict indexing (`tests[1]["expected"]`) and explained why named keys beat positional lists; not yet practised in code |
| Type hints & clean code | 0 | Self-report |
| Async programming | 0 | Self-report |
| Processes, subprocesses & concurrency | 1 | 2026-11-16 `[GUIDED]`: M1.1/M1.2 used `subprocess.run` with `sys.executable`, `capture_output`, `text`, `check=False`, `timeout`, and handled `TimeoutExpired`. Understood candidate failure vs engine error and why not to catch broadly. Gaps: `Popen`, signals/process groups, async/concurrency not yet touched |
| Error handling & logging | 2 | 2026-11-04: F1.3c `[GUIDED]`: invariant check with `assert` (not yet seen to fire); knows `python -O` strips asserts (told, not practised). 2026-11-02: F1.3a/b `[GUIDED]`: `try`/`except Exception as e`, `continue`, formatting `type(e).__name__` / `{e}`, telling test errors apart from function errors, why a failed assignment leaves old values behind. 2026-11-05 `[GUIDED]`: `logging` replaces `print`; learner set the INFO/WARNING/ERROR rule (see F1 logging in Assignment history). Open: lazy `%s` formatting |
| Packaging & dependency management | 0 | Self-report |
| Testing & debugging | 0 | Self-report |

### 2. Linux & systems engineering
| Skill | Level | Evidence |
|---|---|---|
| Filesystem & permissions | 2 | 2026-11-12 `[GUIDED]`: on a real Linux FS, predicted `644` → no exec → Permission denied before running; saw `/mnt/d` makes every file `777` and that `mv` keeps the mode. Octal vs symbolic `chmod` (octal overwrites all 9 bits). Mixed up `o` (other) with owner again; fixed it after seeing the output. Still needs the chart. 2026-11-05: explained `/mnt/d` as a Windows drive bridge, not a copy; Windows-mounted files show as `777` (not a real isolation boundary). Read `ls -l` and octal modes; `chmod 640` applied and explained (`[GUIDED]`, learner predicted most of it). Umask worked out with hints (`0022`→`644`, `077`→`600`). Gap: `chmod` of `other` at digit level was first described loosely; not yet practised solo |
| Processes & signals | 2 | 2026-11-15: predicted Ctrl+C → SIGINT → 130 with the 128 + 2 reasoning, no hint. 2026-11-07 `[GUIDED]`: found PIDs with `ps -ef`, killed `sleep` with `kill` and `kill -9`, read `$?`. Derived 128 + signal number with a subtraction hint and correctly predicted 137. Classified 0, 1, 137, 143 correctly after being told the below/above 128 rule. Gaps: `$?` is per shell and per last command (ran it in the wrong terminal, and twice without `echo`); catching or ignoring SIGTERM not practised. 2026-11-05: explained SIGTERM (catchable, clean exit) vs SIGKILL (uncatchable) and why a sandbox needs SIGKILL as fallback |
| Streams (stdout/stderr) | 2 | 2026-11-05 `[GUIDED]`: needed three hints and a concrete `ls` demo to separate stdout from stderr; the terminal is the default destination, not a stream. Predicted and verified `out.txt` / `err.txt` contents |
| Memory & resource management | 0 | Self-report |
| Networking & ports | 0 | Self-report |
| SSH | 0 | Self-report |
| Shell commands & Bash scripting | 2 | 2026-11-15 `[GUIDED]`: wrote first script (`~/f2/args.sh`) using `$0`, `$1`, `$#`; predicted all 4 cases correctly beforehand, including `"hello world"` → 1 argument. `chmod u+x` correct (no u/o mix-up). Used `bash -x` (agent-suggested). Gap: why `#!/usr/bin/env` alone loops forever needed a full reveal; `env` runs its argument as a command (learned by experiment). 2026-11-12: shebang, `./` vs `bash`, variables, no spaces around `=`, single vs double quotes (one wrong prediction), `VAR=x cmd` expands before the command runs (explained with a hint). Ran an agent-given 2-line script; has not written a script yet |
| System-level debugging | 0 | Self-report |

### 3. Docker & infrastructure
| Skill | Level | Evidence |
|---|---|---|
| Images & containers | 0 | Has run prebuilt containers; doesn't know image vs container |
| Dockerfiles | 0 | Never written one |
| Volumes & networking | 0 | Self-report |
| Docker Compose | 0 | Self-report |
| Container security | 0 | Self-report |
| Resource restrictions | 0 | Self-report |
| Execution isolation | 0 | Self-report |

### 4. Code execution infrastructure
| Skill | Level | Evidence |
|---|---|---|
| Process creation & lifecycle | 1 | 2026-11-16 `[GUIDED]`: M1.1/M1.2 `run_file` starts a child via `subprocess.run([sys.executable, path], capture_output=True, text=True, check=False, timeout=...)`, reads `returncode`/stdout/stderr, and treats timeout as a separate outcome (`TimeoutExpired` → engine result). Gaps: process groups, SIGTERM→grace→SIGKILL, child outliving parent |
| Safe execution of untrusted code | 1 | 2026-11-12: threat model exercise. Listed 5 threats unprompted (CPU, RAM, disk, outbound network, LAN), found result tampering with a hint, mapped threats to defences, and found the network gap. Explained that non-root protects the other defences. Gaps: wall-clock vs CPU limit, hidden vs read-only tests, in-process tampering (all told, not yet practised) |
| Execution timeouts | 2 | 2026-11-16 `[GUIDED]`: M1.2 added wall-clock `timeout` to `run_file`, caught only `TimeoutExpired`, preserved partial stdout as `str`, returned `timed_out` + sentinel `returncode=124`, verified bounded run (~2×timeout). Explained flush/buffering and `""` vs `None` for captured-empty streams; knows `timed_out` is primary (exit code 124 could be produced by candidate). Gap: exact `subprocess.run` timeout kill mechanism stated imprecisely (needs doc quote); no grace period/SIGTERM sequence yet |
| Resource limits | 0 | Self-report |
| Output capture | 2 | 2026-11-16 `[GUIDED]`: M1.1/M1.2 capture stdout/stderr via pipes (`capture_output=True, text=True`) into result dict; normalized `TimeoutExpired` payloads (bytes/None → `str`) to keep interface consistent. Gap: encoding/errors, large output handling |
| Worker architecture | 0 | Self-report |
| Job queues | 0 | Self-report |
| Failure handling | 0 | Self-report |

### 5. Testing & AI evaluation
| Skill | Level | Evidence |
|---|---|---|
| Pytest | 0 | Self-report |
| Test case generation | 0 | Self-report |
| Functional correctness | 0 | Self-report |
| Benchmark design | 0 | Self-report |
| Evaluation datasets | 0 | Self-report |
| LLM-generated code evaluation | 0 | Self-report |
| Pass@k & related metrics | 0 | Self-report |
| Coding-agent benchmarking | 0 | Self-report |

---

## Implementation ledger

| Date | Item | Category (A/B/C) | Attribution | Notes |
|---|---|---|---|---|
| 2026-11-01 | `AGENTS.md`, `PROGRESS.md`, `CLAUDE.md` | C | `[AGENT]` | Working agreement and progress tracker set up |
| 2026-11-16 | `learning/m1/runner.py` — M1.1 `run_file(path)` with `subprocess.run`, returns dict | A | `[GUIDED]` | Sample files copied by agent (Category C). Learner wrote all runner code; hints: split into 2 steps, where the output went, interface boundary |
| 2026-11-15 | `~/f2/run.sh` (WSL home, not in repo) — runs a .py file, prints and forwards its exit status, usage error on no args | A | `[GUIDED]` | Arg check correct first try. Shebang relative-path bug (`#!usr/bin/bash`, `#!~/bin/bash`) fixed by learner after hint. First version used `exec python3 "$@"` from Google; learner explained why `exec` can't print the status and chose `"$1"` over `"$@"` |
| 2026-11-15 | `~/f2/args.sh` (WSL home, not in repo) — prints `$0`, `$1`, `$#` | A | `[GUIDED]` | Script by learner. First shebang `#!/usr/bin/env` (no interpreter) caused an exec loop; learner fixed it by comparing with the working `hello.sh` |
| 2026-11-07 | `learning/f2/f2_ignore_term.py` — catches SIGTERM with a handler, then sleeps | A | `[GUIDED]` | Agent named the APIs and pointed to docs. Learner chose a custom handler over the suggested `SIG_IGN`. Survived `kill`, died to `kill -9` with status 137 |
| 2026-11-02 | `learning/f1_collections.py` — F1.1 add() test loop | A | `[GUIDED]` | Correct on first try. Only hint given: index `input` by position. Used `len(tests)` instead of hard-coding 3 |
| 2026-11-04 | `learning/f1_functions.py` — F1.3d raise `ValueError` on empty suite | A | `[GUIDED]` | Correct first try given the constraints (top of function, pick a concrete exception type) |
| 2026-11-04 | `learning/f1_functions.py` — F1.3c per-status counts, dict return, total invariant assert | A | `[GUIDED]` | Counting + test data correct first try. Needed a thought-experiment prompt to see the `.values()` unpacking flaw; `sum()` after a docs pointer |
| 2026-11-02 | `learning/f1_functions.py` — F1.3b validate test data first, BAD TEST status | A | `[GUIDED]` | Correct on first attempt, given the constraint "read both fields before calling func" and the hint "second try + variable" |
| 2026-11-02 | `learning/f1_functions.py` — F1.3a catch function exceptions as ERROR, continue run | A | `[GUIDED]` | Hint level 4 for formatting the exception. First defended `div` against 0 instead of simulating buggy submitted code |
| 2026-11-02 | `learning/f1_functions.py` — F1.2 reusable `run_tests(func, tests)` + `multiply` suite | A | `[GUIDED]` | Hints needed for the set/dict return bug and for the unused `func`. Learner chose the tuple return |

---

## Mistakes corrected

| Date | Area | Mistake | How it was fixed | Hint level needed (1–5) |
|---|---|---|---|---|
| 2026-11-02 | Python / enumerate | Treated an `enumerate` item as the dict and indexed it with `test[i]["input"]`, which gave `TypeError: 'int' object is not subscriptable` | Debugged it with `print(test, type(test))` and switched to `test[1]`. Mental model still wrong: thought the tuple held two test dicts | 3 (pointed to unpacking docs) |
| 2026-11-02 | Python / types | Returned `{total, passes}` (a set, so unordered and duplicates collapse), which printed `3/2 passed`. Then returned `{total: total, passes: passes}` (unquoted keys, so the values became keys), which gave `ValueError` when all tests passed | Ran the experiments, saw the error, switched to a tuple return. Still thought dict unpacking gives values (it gives keys) | 3 |
| 2026-11-04 | Design | Returned a dict, then unpacked it with `a, b, ... = result.values()`, which depends on key order again and would silently swap counts | Thought experiment ("what if someone reorders the keys?"); learner explained the silent swap and switched to `result["passes"]` | 2 |
| 2026-11-04 | Precision | Said a missed counter makes `total` too big; actually `total` is `len(tests)` and the counter sum falls short | Corrected by agent | 1 |
| 2026-11-02 | Python / exceptions | Printed `e.__doc__` (the generic class docstring), then tried random dunders. One `except` block crashed with `AttributeError`, which killed the run anyway | Hints: a method reference vs a call (`__str__` vs `{e}`), and the name lives on the class (`type(e).__name__`). Learned that the error handler itself must not fail | 4 |
| 2026-11-02 | Tooling | Zed Ctrl+Shift+R reran the old `f1_collections.py`, so the output didn't match the code | Learner noticed it themselves; now runs from the terminal | 1 |
| 2026-11-15 | Bash / shebang | `#!/usr/bin/env` with no interpreter: the kernel runs `env ./args.sh`, `env` runs `./args.sh` again, forever, with no output. Then `#!/usr/bash` → `bad interpreter` | Fix found by learner (compared with `hello.sh`). The explanation of the loop needed a full reveal; learner still reads `args.sh` as the thing that runs `echo`, not bash | 5 |
| 2026-11-02 | Design | Kept a manual `i` counter while also using `enumerate`, which duplicates the counter | Learner removed manual `i` and used `for i, test in enumerate(tests, 1)` | 2 |

---

## Remaining gaps / focus areas

*Updated 2026-11-15.*
- **Habit:** skips requested predictions and written explanations, or answers "idk" without trying. Answers "why" with a general rule instead of the concrete case. Keep asking for a prediction before every command and a mechanism in every explanation.
- **Linux:** owner/other (`u`/`o`) confusion recurred twice (sessions 6, 8); right in session 9. Needs the octal chart for `chmod`. `$?` is per shell and per last command.
- **Bash:** has written one script (`args.sh`). Not yet: `$?` inside a script, `if`, argument checks, pipes.
- **Threat model leftovers for M3:** wall-clock vs CPU limit, total disk quota, tests invisible to the submission, in-process tampering.
- **Not started:** Docker, testing/pytest, type hints, async, subprocess, AI evaluation.
- **Product purpose:** learner has not confirmed the draft product definition. F1 is done, so this is due.

---

## Session log

### 2026-11-16 — Session 11: M1.2 timeouts
- **Milestone:** M1
- **Implemented:** M1.2 `learning/m1/runner.py` `run_file(path, timeout)` `[GUIDED]` — catches only `TimeoutExpired`, adds `timed_out`, preserves partial stdout as `str`, normalizes empty timeout streams to `""`, `returncode=124` sentinel; `loop.py`/`sleep.py` samples; 5-case run in ~4.3s for `timeout=2`.
- **Concepts:** wall-clock timeout via `subprocess.run(timeout=...)`, `TimeoutExpired` payload/typing, pipe buffering and `flush=True`, consistent result interface (`""` vs `None` for captured-empty), `timed_out` as primary signal vs conventional timeout return code.
- **Predictions/checks:** learner predicted timeout → kill+`TimeoutExpired`, `timed_out=True`, partial stdout, `returncode=124` (reasonable; kill mechanism stated imprecisely). Understanding check passed: avoid broad `except` to not hide engine bugs; `returncode==124` alone can misclassify a candidate that exits 124.
- **Review fixes:** removed extra missing-file pre-check/`timeout.py` case, decoded bytes and normalized `None`→`""` on timeout path.
- **Next:** assign M1.3 (e.g. observe/report missing/unrunnable file via normal path as candidate result, or add basic tests/type hints) with predictions before coding.

### 2026-11-01 — Session 0: Setup
- **Implemented:** `AGENTS.md`, `PROGRESS.md`, `CLAUDE.md` `[AGENT]`

### 2026-11-01 — Session 1: Baseline assessment
- **Milestone:** M0 → F1
- **Findings:** beginner across all areas (see skill matrix). Has WSL2 + Docker Desktop + Python 3.14 on Windows, no Linux distro.
- **Decisions:** added foundations track F1–F3 before M1 (agent-proposed, draft).
- **Concepts introduced:** lists vs dicts (explanation given, not yet practised).
- **Next learning task:** F1.1 lists vs dictionaries; install Ubuntu in WSL.

### 2026-11-02 — Session 2: F1.1 concept check
- **Milestone:** F1
- **Concept check (lists vs dicts):** both answers correct. Learner explained that positional lists hide meaning and are more bug-prone. Agent added: positional data also breaks when fields are added or reordered.
- **Issue:** `wsl --install` failed with `-sh: wsl: not found`. Learner ran it inside a Linux shell, not Windows PowerShell. Explained that `wsl.exe` is a Windows program, and how to tell shells apart by their prompt.
- **Implemented:** F1.1 `learning/f1_collections.py` `[GUIDED]`. It worked first time, with output `PASS / FAIL / PASS / 2/3 passed`.
- **Review:** correct and clean. Weakness: a bare `FAIL` doesn't say which case failed or what `add` actually returned, and an evaluator has to report that. This became the F1.1b follow-up.
- **F1.1b:** done. Uses tuple unpacking with `enumerate(tests, 1)`, has no duplicate counter, calls `add` once, and the FAIL line reports input, expected and actual values.
- **Explain-back:** (1) `test[0]`: roughly right, but the wording was loose ("index of the tuple"); clarified that it's the count from `enumerate`. (a) Predicted JS-style `undefined`; it was actually `KeyError` on the right line. Learner noticed that Python fails loudly where JS stays silent. (b) Correctly predicted FAIL, but couldn't yet say why it's dangerous. Given a guiding question, still pending.
- **Ubuntu:** installed and running, user `theprinceraj`. Learner is at the `/mnt/d/...` prompt.
- **Bonus:** switched to `a, b = test["input"]`. With a 3-element input, this raises `ValueError: too many values to unpack`. Learner's own conclusion: "this version throws and the older one failed wrongly". That's the key evaluator insight: a malformed test must error, not be misjudged as a solution failure (or as a false PASS). Tests restored.
- **Habit to build:** learner paraphrased an error ("can't spread") instead of copying it. Asked them to always copy exact error text.
- **F1.1 closed.**
- **Next:** F1.2 functions: refactor the loop into a reusable `run_tests(func, tests)`. After that, F1.3 exceptions: one broken test shouldn't crash the whole run.

### 2026-11-02 — Session 3: F1.2 functions
- **Milestone:** F1
- **Pre-check:** (1) correct on `add` vs `add()`. Agent added that `add()` fails before `run_tests` is even called. (2) Said "void". Corrected: Python returns `None`, a real object.
- **Implemented:** F1.2 `learning/f1_functions.py` `[GUIDED]`. It took three iterations. First return was the set `{total, passes}`, which printed `3/2 passed`. Second was the dict `{total: total, ...}` with unquoted keys, which raised `ValueError` when every test passed. Final version is a tuple. Also fixed the hard-coded `add` so `func` is used.
- **Tooling:** Zed Ctrl+Shift+R reran the old file. Learner spotted this and now runs scripts from the terminal. Introduced `sys.executable` / `sys.version` for finding which interpreter ran.
- **Key insight:** the dict bug only showed up when every test passed. Evaluators need edge-case tests: all pass, all fail, an empty suite.
- **Explain-back:** good on return-vs-print and the tuple-vs-dict trade-off. Correctly predicted the empty suite returns `(0, 0)`.
- **Next:** F1.3 exceptions: a malformed test or a crashing function gets reported as ERROR, separate from FAIL, and the run carries on.

### 2026-11-02 — Session 3 (cont.): F1.3a/b exceptions
- **Learner request:** one task at a time. Big multi-part assignments overwhelmed them.
- **Pre-check by experiment:** broke `run_tests` in four ways and classified each one as the test's fault or the function's fault. Taught reading tracebacks bottom-up.
- **F1.3a** `[GUIDED]`: function exceptions now report ERROR and the run continues. At first the learner guarded `div` against 0, so the agent explained that the submitted code isn't ours to fix. Struggled with formatting the exception (tried `__doc__` and random dunders), which needed hint level 4. Found by accident that an `except` block that crashes defeats the safety net.
- **F1.3b** `[GUIDED]`: BAD TEST status, test validated before the function runs. Learned that Python has no block scope. The experiment showed how a missing `continue` grades a test with stale inputs and gives a false PASS. Learner reached the insight themselves ("it held values of previous test because this test didn't allot it the new values").
- **Habit gaps:** skipped a requested prediction before running. Gives half-answers to "why" questions, so prompt for the mechanism, not just the effect.
- **Next:** F1.3c counts per status in the summary.

### 2026-11-04 — Session 4: F1.3c per-status counts
- **Milestone:** F1
- **Implemented:** F1.3c `[GUIDED]` (see Current assignment).
- **Concepts:** why an evaluator must separate FAIL/ERROR/BAD TEST (a broken benchmark must not count against the model); invariants and `assert`; `-O` strips asserts, so production guards use `if ...: raise`; `sum()`; don't keep commented-out code.
- **Explain-back:** good on the silent count swap and on why summing the dict covers new statuses.
- **Habit gaps:** skipped the requested "break it on purpose and paste the output" step (said it was done earlier). Ask for failure output of every new guard. Wording about which number goes wrong was imprecise at first.
- **Leftovers in code:** commented-out loop and redundant `, 0` in `sum()`; learner told to remove them.
- **F1.3d** `[GUIDED]`: empty suite raises `ValueError`. Defended the design: the detector raises, the caller's loop decides whether to skip or stop. This links ahead to worker/queue retry policy (M5).
- **Next:** answer "why validate before the loop", then git init, then F1.4 files: load test cases from a JSON file (connects to the "empty file" scenario).

### 2026-11-05 — Session 5: F1 wrap-up
- **Milestone:** F1 → closed.
- **Explain-back (F1.3d):** question 1 was initially answered with a wrong premise (`None`). The function's `return` sits outside the loop, so without the guard an empty suite returns all zeros and the `assert` passes. Learner saw the guard fire (`ValueError`) and then reasoned correctly that an empty dataset can mean a wrong path, so a silent zero result is a false green.
- **Habit gaps:** asked for a concrete reproduction before answering a "what happens" question; the learner needed the task number explained (F1.3c) before engaging with the references.
- **Leftovers (learner decision):** commented-out "Old version" block in `run_tests` and the redundant `, 0` in `sum()` kept as-is at learner's request. Recorded here so it is not treated as an oversight later.
- **Closed:** F1 finished. Next milestone F2 (Linux in WSL Ubuntu).

### 2026-11-05 — Session 6: F2 concept check (Linux foundations)
- **Milestone:** F2 started. No code written; all Category A checks were learner answers.
- **Concepts covered:** `/mnt/d` as a Windows drive bridge; stdout vs stderr with `>` and `2>`; `ls -l` permission strings and octal (`r`=4, `w`=2, `x`=1); `chmod 640`; `umask` as a mask of rights to remove (`0022`→`644`, `077`→`600`); SIGTERM vs SIGKILL; root bypasses file permissions, so untrusted code must not run as root; layered defence (non-root, restricted mounts, resource limits).
- **Results:** learner got stream behaviour and octal decoding after hints; the `/mnt/d` permission trap (`777`) was explained, and the learner accepted it.
- **Learner misconceptions corrected:**
  - Read "logging" as a separate stream in a shell redirect; it's Python's default destination for stderr.
  - Treated `umask 077` as "does nothing" and tried subtracting digits (`6-7 = -1`). Fixed by working with rights (remove r/w/x), not subtraction.
  - Gave the default mode without showing the `umask` calculation; needed the table.
  - Claimed a chmod changed the "group" when it only changed "other" (corrected).
- **Habit gaps:** answers guessed or skipped (`"no idea"`) before attempting predictions; expects to be told answers rather than reasoning from the hint. Keep requiring a prediction before each command.
- **Open for next session:** practise processes (`ps`, `kill`, `kill -9` on a running script, `$?` exit codes) with a prediction first; then the root/mount/isolation threat model for M3.

### 2026-11-07 — Session 7: F2 exit statuses after signals
- **Milestone:** F2. Terminal experiments only, no project code written.
- **Concepts covered:** PID and parent PID in `ps -ef`; `grep` matching itself; `kill` (SIGTERM) gives `Terminated` and 143; `kill -9` (SIGKILL) gives `Killed` and 137; rule of 128 + signal number; the shell prints the death message, not the process; `$?` belongs to the last command in that shell.
- **Results:** predicted 137 before seeing it, after the agent reduced the rule to a subtraction. First two prediction prompts answered "no idea". Filled in the status table once the below/above 128 rule was given.
- **Mistakes corrected:** ran `$?` without `echo` (`0: command not found`, `137: command not found`; the second time was after the explanation, so not yet a habit); read SIGKILL's number 9 as the `$?` result; ran `echo $?` in Terminal B and got `kill`'s own 0.
- **Agent correction:** the first table task assumed the below/above 128 rule without having taught it; the learner said so and the agent explained it. Told that above 128 is a convention, since a program can exit with 137 by itself (not yet tested; revisit with `subprocess` in M1).
- **Explain-back:** treating every non-zero status as "failed its tests" would falsely fail a correct solution killed by a worker restart. Correct on the effect; the learner has not yet said what the evaluator should do instead.
- **Who sent the signal:** learner said a timeout kill and an infrastructure kill must score differently, and that the engine should track who sent the signal. Agent added: the parent can't learn the sender, so the engine records its own kill (`timed_out`), and "the code is correct" overclaims for an outside kill (the OOM killer can be caused by the code), so that result is an infrastructure error.
- **`f2_ignore_term.py`** `[GUIDED]`: predicted handler message on `kill`, and SIGKILL bypassing the handler. First predicted 143 for `kill -9`, then corrected it to 137 using 128 + 9 without a further hint. First run killed PID 326, the parent shell (PPID column), not the program: bash ignored SIGTERM and died to SIGKILL. Rerun used the right PID and matched the predictions. Skipped the second `ps` check; survival shown by the `IGNORED signal 15` line and by `kill -9` still reaching the process.
- **Told, not observed:** the first run's program most likely died from SIGHUP when its terminal closed.
- **Explain-back (timeout design):** SIGTERM alone lets a handler hold resources; immediate SIGKILL denies the program a chance to save state; picked SIGTERM, grace period, then SIGKILL, with sound reasoning. Precision fix: `f2_ignore_term.py` would end by itself after 300 s, so "never ends" only applies to a program that loops. Agent added: the grace period gives untrusted code extra run time, so it must be short and bounded.
- **Explain-back (exit 0 in grace period):** learner reported "time limit exceeded" and said the exit status alone is not reliable, without a hint. Agent added: the status is chosen by untrusted code, so the engine's own `timed_out` record is checked first, and in M4 exit 0 must not count as passing tests.
- **Signals topic closed for F2.** Not yet practised: child processes outliving a killed parent (M2), Python `subprocess` return codes (M1).
- **Next:** threat model for M3: list what a submission could do when run as a normal user with no sandbox.

### 2026-11-12 — Session 8: F2 threat model
- **Milestone:** F2. Thinking exercise only, no code.
- **Learner's threat list (unprompted):** runs forever, eats RAM, fills disk (marked accidental), outbound network/DoS, attacking LAN/other devices. **Missed until hinted:** damage to existing files and result tampering. With the hint "what file decides whether it passed", the learner named result manipulation.
- **Agent added:** `/mnt/d` = real Windows D: drive (`777`), so `rmtree` hits real files; in-process grading (F1 `run_tests`) lets the candidate change `tests` in memory, which is why M1 uses a separate process; real LLM agents have edited tests instead of fixing code.
- **Defence mapping (threats a–g vs non-root / restricted mounts / resource limits):** a–c resource limits ✔; f restricted mounts ✔; g "restricted file visibility" (partly right). For d/e the learner named a **fourth defence (network restrictions)** instead of answering "none of the three". Right conclusion, though the question wasn't answered as asked. **Skipped the question about non-root.**
- **Agent corrections:** a CPU-time limit doesn't stop `time.sleep` forever, so a wall-clock timeout is needed too; a file-size limit ≠ a total disk quota; mounting tests read-only still lets the submission *read* expected values; in-process tampering isn't stopped by mounts.
- **Habit gap:** "who gets hurt" given as one blanket answer, not per item.
- **Non-root:** first answer was "can't edit system files" (correct but shallow; agent added `/etc/shadow`, a backdoor admin account). After a level-3 hint (a normal user can lower a hard rlimit but never raise it; mounts and network rules need root), the learner concluded that root makes the other defences "toothless" because it can change them, and that non-root keeps the process inside the sandbox's defined limits. Correct principle. Skipped the requested one-line-per-defence answer again.
- **Agent added:** defence in depth: each layer protects another one, so non-root is what keeps limits, mounts and network rules in force. In Docker, root inside the container is still dangerous (M3: `--user`).
- **Threat model topic closed for F2.** Carry into M3: map each Docker flag to a threat a–g; tests invisible to the submission; wall-clock timeout + CPU limit; total disk quota.
- **Next:** Bash basics (variables, pipes, `$?` in a script, a first small script). Shell scripting is the last F2 area still at 0.

### 2026-11-12 — Session 8 (cont.): Bash basics, part 1
- **Pre-check:** `lang = python` → error ✔ (reason vague; agent explained that the first word is the command); `echo 'Result: $lang'` predicted `Result: python` ✘ (single quotes are literal; confirmed by experiment); `./hello.sh` without chmod → Permission denied (right for a Linux filesystem, wrong on `/mnt/d`).
- **Discovered by accident:** wrote `lang=python echo "Result: $lang"` on one line and got `Result:`. With the hint "expansion happens before the command runs", the learner explained that `lang` was unset at expansion time. Agent added: `VAR=x cmd` sets the variable only in that command's environment (links to `subprocess` `env=` in M1).
- **hello.sh on `/mnt/d`:** created as `-rwxrwxrwx`, so it ran without `chmod`. **Skipped the requested prediction** (again) and the `chmod` steps; created the file in the repo root instead of `learning/f2/`.
- **Moved to `~`:** `mv` across filesystems kept `777` (now real, so world-writable; agent explained the risk). Forgot the octal chart; given r=4/w=2/x=1 again. Then predicted `644` → `rw-r--r--` and `Permission denied` **before running** ✔ (reason was missing the "owner has no x" mechanism).
- **chmod mistakes:** `rwxr-xr-x` → `755` ✔. "Execute for owner only" answered `chmod 755` ✘, then self-corrected to `744` (right only from 644; agent showed `664` → `744` silently drops group write, which is why symbolic mode exists). Symbolic attempt `chmod o+x` gave `-rw-rw-r-x`: **`o` read as owner** (same owner/other confusion as session 6). The prediction vs. output diff exposed it. Fixed with `chmod o-x` + `chmod u+x` → `-rwxrw-r--` ✔. Bonus (`chmod o-x,u+x` in one command) not tried.
- **Next:** Bash part 2: script arguments (`$1`), `$?` inside a script, a tiny runner script `run.sh <file.py>` that reports the exit status.

### 2026-11-15 — Session 9: Bash part 2, script arguments
- **Milestone:** F2.
- **Concepts covered:** `$0`, `$1`, `$#`; word splitting happens before the script starts, so quotes group words; a missing argument is an empty string, not an error; the kernel's shebang rule (`#!/interp` → `/interp script args`); `env CMD` runs CMD (looked up in `PATH`); `bash -x` traces commands; Ctrl+C = SIGINT → 130.
- **Results:** predicted all four `args.sh` cases before running, all correct. Predicted 130 for Ctrl+C with the reason. Symbolic `chmod u+x` right first time.
- **Bug found:** shebang `#!/usr/bin/env` with nothing after it hung silently (an exec loop). `bash -x` ran it fine because bash treats line 1 as a comment. A second try with `#!/usr/bash` gave `bad interpreter`. Learner fixed it by diffing against the working `hello.sh`.
- **Agent error:** hinted that a silent hang "usually waits for something". That's wrong here (busy loop). Corrected in the next turn; the planned `top` check was never run.
- **Explain-back:** the loop chain needed hint level 5 (revealed). The learner answered with general rules instead of concrete commands, and then named `./args.sh` as the thing that runs `echo`. **Open gap:** a script is a text file that an interpreter (bash) reads; in the broken loop bash never started.
- **Habit gaps:** again skipped requested predictions (the `env` experiments) and the written chain; said "idk" without trying.
- **`#!/bin/cat` experiment ✅:** learner predicted "prints the whole file" ✔. Changed `cat` → `bash` (got `Hello`) and explained: bash interprets the file, cat only prints it. **Shebang gap closed.** (Needed a prompt to give the "why".)
- **Next:** Task 2 `run.sh <file.py>` (assigned): runs `python3 "$1"`, prints `exit status: <n>`; test with `ok.py`, `crash.py`, `three.py` (`sys.exit(3)`) and no argument, predictions first.

### 2026-11-15 — Session 10: run.sh, F2 closed, pace change
- **Pace change (learner request):** bigger combined tasks, one prediction block per task, shorter explanations; F3 folded into M1.
- **run.sh** `[GUIDED]`: see ledger. Concepts: `exec` replaces the process (learner explained it); `"$@"` vs `"$1"` → argument injection (`-c` example, agent-given); kernel doesn't expand `~` in shebangs; `.` isn't in `PATH` (`run.sh: command not found`).
- **Habit:** predictions skipped at first, then written before the crash/three runs (both right). Didn't paste `echo $?` after the final version's runs.
- **Next:** M1.1 `run_file(path)` with `subprocess.run`.
