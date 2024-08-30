import ctypes
import time
from src.utils import log_event
from src.shutdown import shutdown_system, sleep_system  # Import functions from shutdown.py

def get_idle_duration():
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_ulong)]

    last_input_info = LASTINPUTINFO()
    last_input_info.cbSize = ctypes.sizeof(LASTINPUTINFO)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(last_input_info))
    millis = ctypes.windll.kernel32.GetTickCount() - last_input_info.dwTime
    return millis / 1000.0  # Convert milliseconds to seconds

def monitor_idle_time(idle_time_limit, check_interval, action, log_file):
    is_locked = False
    lock_start_time = None
    shutdown_threshold = idle_time_limit  # 2 minutes (120 seconds) or whatever is set in the config

    while True:
        idle_time = get_idle_duration()
        if idle_time >= 60 and not is_locked:  # Lock detected
            is_locked = True
            lock_start_time = time.time()
            log_event(log_file, "System locked. Timer started.")
            print("System locked. Timer started.")
        elif idle_time < 60 and is_locked:  # Unlock detected
            is_locked = False
            lock_duration = time.time() - lock_start_time
            log_event(log_file, f"System unlocked. Locked for {lock_duration / 60:.2f} minutes.")
            print(f"System unlocked. Locked for {lock_duration / 60:.2f} minutes.")
        elif is_locked:  # Check if shutdown threshold is reached
            lock_duration = time.time() - lock_start_time
            if lock_duration >= shutdown_threshold:
                log_event(log_file, "Lock time exceeded threshold. Executing action...")
                print("Lock time exceeded threshold. Executing action...")

                # Call the appropriate action based on the config
                if action == 'shutdown':
                    shutdown_system(log_file)
                elif action == 'sleep':
                    sleep_system(log_file)

                return True  # Exit after action

        time.sleep(check_interval)
