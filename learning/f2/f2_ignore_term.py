import signal
from time import sleep


def ignore_sigterm(signum, frame):
    print(f"IGNORED signal {signum}")


signal.signal(signal.SIGTERM, ignore_sigterm)

sleep(300)
