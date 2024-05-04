import signal
import sys
import time


def handle_exit(sig, frame):
    print("Worker 1 received signal to terminate.")
    sys.exit(0)


signal.signal(signal.SIGTERM, handle_exit)

try:
    while True:
        print("Worker 1 is processing...")
        sys.stdout.flush()  # Принудительно записываем лог
        time.sleep(5)  # Имитация длительной работы
except Exception as e:
    print(f"Worker 1 encountered an error: {e}")
    sys.stdout.flush()  # Принудительно записываем лог
    sys.exit(1)
