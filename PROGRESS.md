# PROGRESS.md — Qubrix learning & build log

Maintained by the agent at the end of every meaningful session (see `AGENTS.md` §4 Step 8 and §9).
Attribution labels (`[SOLO]` `[GUIDED]` `[PAIRED]` `[AGENT]`) and skill levels (0–4) are defined in `AGENTS.md` §0.
**Rule:** skill levels only rise on evidence from the learner's own work. `[AGENT]` work never raises a level.

---

## Current status

| Field | Value |
|---|---|
| Current milestone | **F1 — Python foundations** (M0 setup mostly done) |
| Active task | F1.3 exceptions. F1.3a ✅ F1.3b ✅. Next: F1.3c, count PASS/FAIL/ERROR/BAD TEST separately in the summary |
| Parallel task | none. Ubuntu installed and set as default WSL distro (verified) |
| Last session | 2026-11-02 |
| Open decisions | Product definition (draft below) — learner to confirm; weekly time budget unknown |

## Current assignment

**F1.3 — Exceptions** (Category A, learner implements). The learner asked for **one task at a time**: keep each step small and single.
- Pre-check done by experiment in `learning/f1_break.py`. Learner classified: `"inputs"` typo / `"input": 5` / missing `"expected"` are the test's fault; `div` by 0 is the function's fault. Reads tracebacks bottom-up with guidance.
- **F1.3a ✅ 2026-11-02:** `try` wraps only `func(a, b)`. Prints `Test 1: ERROR - ZeroDivisionError: division by zero`, then `continue`, so later tests still run. Needed hint level 4 for `type(e).__name__` / `{e}`. Nit: uses `e.__str__()` where `{e}` is idiomatic.
- **F1.3b ✅ 2026-11-02:** a second `try` reads `input` and `expected` *before* calling `func`, and prints `BAD TEST - <Type>: <msg>`, then `continue`. Renamed `res` to `expected` (one variable, one meaning). Learned that Python has no block scope (compared it to JS `var` vs `let`). Experiment without `continue` showed a broken test graded with leftover values from the previous test, which gave a false PASS (`2/2 passed`). Learner explained it in their own words: the failed assignment never happened, so the old values stayed.
- **F1.3c (next):** the summary should count ERROR and BAD TEST separately; right now they only lower the pass count. Consider flagging an empty suite.
- Later: count errors separately in the summary; an empty suite should be flagged.

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
| Git | 2.53.0 installed; project not yet a git repo |
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
| F1 | Python foundations: data types, collections, functions, control flow, files, exceptions — all applied to tiny Qubrix-flavoured exercises | Python | **In progress** |
| F2 | Linux foundations in WSL Ubuntu: shell, filesystem, permissions, processes | Linux | Not started |
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
| Processes, subprocesses & concurrency | 0 | Self-report |
| Error handling & logging | 2 | 2026-11-02: F1.3a/b `[GUIDED]`: `try`/`except Exception as e`, `continue`, formatting `type(e).__name__` / `{e}`, telling test errors apart from function errors, why a failed assignment leaves old values behind. No logging yet |
| Packaging & dependency management | 0 | Self-report |
| Testing & debugging | 0 | Self-report |

### 2. Linux & systems engineering
| Skill | Level | Evidence |
|---|---|---|
| Filesystem & permissions | 0 | Ubuntu installed 2026-11-02; not practised yet |
| Processes & signals | 0 | Self-report |
| Memory & resource management | 0 | Self-report |
| Networking & ports | 0 | Self-report |
| SSH | 0 | Self-report |
| Shell commands & Bash scripting | 0 | Self-report |
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
| Process creation & lifecycle | 0 | Self-report |
| Safe execution of untrusted code | 0 | Self-report |
| Execution timeouts | 0 | Self-report |
| Resource limits | 0 | Self-report |
| Output capture | 0 | Self-report |
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
| 2026-11-02 | `learning/f1_collections.py` — F1.1 add() test loop | A | `[GUIDED]` | Correct on first try. Only hint given: index `input` by position. Used `len(tests)` instead of hard-coding 3 |
| 2026-11-02 | `learning/f1_functions.py` — F1.3b validate test data first, BAD TEST status | A | `[GUIDED]` | Correct on first attempt, given the constraint "read both fields before calling func" and the hint "second try + variable" |
| 2026-11-02 | `learning/f1_functions.py` — F1.3a catch function exceptions as ERROR, continue run | A | `[GUIDED]` | Hint level 4 for formatting the exception. First defended `div` against 0 instead of simulating buggy submitted code |
| 2026-11-02 | `learning/f1_functions.py` — F1.2 reusable `run_tests(func, tests)` + `multiply` suite | A | `[GUIDED]` | Hints needed for the set/dict return bug and for the unused `func`. Learner chose the tuple return |

---

## Mistakes corrected

| Date | Area | Mistake | How it was fixed | Hint level needed (1–5) |
|---|---|---|---|---|
| 2026-11-02 | Python / enumerate | Treated an `enumerate` item as the dict and indexed it with `test[i]["input"]`, which gave `TypeError: 'int' object is not subscriptable` | Debugged it with `print(test, type(test))` and switched to `test[1]`. Mental model still wrong: thought the tuple held two test dicts | 3 (pointed to unpacking docs) |
| 2026-11-02 | Python / types | Returned `{total, passes}` (a set, so unordered and duplicates collapse), which printed `3/2 passed`. Then returned `{total: total, passes: passes}` (unquoted keys, so the values became keys), which gave `ValueError` when all tests passed | Ran the experiments, saw the error, switched to a tuple return. Still thought dict unpacking gives values (it gives keys) | 3 |
| 2026-11-02 | Python / exceptions | Printed `e.__doc__` (the generic class docstring), then tried random dunders. One `except` block crashed with `AttributeError`, which killed the run anyway | Hints: a method reference vs a call (`__str__` vs `{e}`), and the name lives on the class (`type(e).__name__`). Learned that the error handler itself must not fail | 4 |
| 2026-11-02 | Tooling | Zed Ctrl+Shift+R reran the old `f1_collections.py`, so the output didn't match the code | Learner noticed it themselves; now runs from the terminal | 1 |
| 2026-11-02 | Design | Kept a manual `i` counter while also using `enumerate`, which duplicates the counter | Learner removed manual `i` and used `for i, test in enumerate(tests, 1)` | 2 |

---

## Remaining gaps / focus areas

- Starting from zero across all five areas; Python fundamentals are the first priority.
- No Linux environment yet — install Ubuntu in WSL2. First attempt ran `wsl` inside a Linux shell (docker-desktop distro) instead of PowerShell; gap: knowing which shell you're in.
- Product purpose not yet understood by learner; revisit the draft definition after F1.

---

## Session log

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
