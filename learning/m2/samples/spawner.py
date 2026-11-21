import subprocess
import sys
import time

MARKER = "/tmp/qubrix_orphan_marker"

subprocess.Popen(
    [
        sys.executable,
        "-c",
        f"import time, pathlib; time.sleep(2); pathlib.Path({MARKER!r}).write_text('alive')",
    ]
)
print("spawned", flush=True)
while True:
    time.sleep(1)
