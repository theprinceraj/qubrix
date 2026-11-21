import sys

sys.stdout.buffer.write(b"\xff\xfe")
sys.stdout.flush()

while True:
    pass
