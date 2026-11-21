import os

size_in_bytes = 10 * 1024 * 1024  # 10 MB

with open("random_10mb.bin", "wb") as f:
    f.write(os.urandom(size_in_bytes))
