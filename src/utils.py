import os
import ctypes
import time

def get_idle_duration():
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_ulong)]

    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
    millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
    return millis / 1000.0  # Convert milliseconds to seconds

def log_event(log_file, message):
    with open(log_file, 'a') as log:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        log.write(f"{timestamp} - {message}\n")

def ensure_log_directory(log_file):
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
