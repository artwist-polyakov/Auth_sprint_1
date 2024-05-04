import signal
import sys
import time

def handle_exit(sig, frame):
    print("Worker 2 received signal to terminate.")
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_exit)

try:
    while True:
        print("Worker 2 is processing...")
        time.sleep(5)  # Имитация длительной работы
except Exception as e:
    print(f"Worker 2 encountered an error: {e}")
    sys.exit(1)
