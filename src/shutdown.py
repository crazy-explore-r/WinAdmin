import os
from src.utils import log_event

def shutdown_system(log_file):
    log_event(log_file, "Shutting down the system...")
    print("Shutting down the system...")
    os.system("shutdown /s /t 1")

def sleep_system(log_file):
    log_event(log_file, "Putting the system to sleep...")
    print("Putting the system to sleep...")
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
