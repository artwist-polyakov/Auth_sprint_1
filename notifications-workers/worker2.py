import os
import signal
import sys
import time

worker_id = os.getenv("WORKER_ID", "worker_unknown")


def handle_exit(sig, frame):
    print(f"{worker_id} received signal to terminate.")
    sys.exit(0)


signal.signal(signal.SIGTERM, handle_exit)

try:
    while True:
        print(f"{worker_id} is processing...")
        sys.stdout.flush()  # Принудительно записываем лог
        time.sleep(5)  # Имитация длительной работы
except Exception as e:
    print(f"{worker_id} encountered an error: {e}")
    sys.stdout.flush()  # Принудительно записываем лог
    sys.exit(1)
