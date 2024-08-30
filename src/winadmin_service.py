# import sys
# import win32serviceutil
# import win32service
# import win32event
# import threading
# import servicemanager
# from src.main import main
# from src.utils import log_event, ensure_log_directory

# class WinAdminService(win32serviceutil.ServiceFramework):
#     _svc_name_ = "WinAdminService"
#     _svc_display_name_ = "WinAdmin Idle Monitor Service"
#     _svc_description_ = "Monitors system idle time after lock and shuts down or sleeps the system."
    
#     log_file = "log/winadmin.log"

#     def __init__(self, args):
#         win32serviceutil.ServiceFramework.__init__(self, args)
#         self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

#     def SvcDoRun(self):
#         try:
#             self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
#             servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
#                                   servicemanager.PYS_SERVICE_STARTED,
#                                   (self._svc_name_, ''))
#             log_event(self.log_file, "WinAdminService is starting.")
            
#             # Start the main logic in a separate thread
#             threading.Thread(target=self.run_main).start()
#         except Exception as e:
#             log_event(self.log_file, f"Error in SvcDoRun: {e}")
#             self.SvcStop()

#     def run_main(self):
#         try:
#             # Notify that the service is running
#             self.ReportServiceStatus(win32service.SERVICE_RUNNING)
#             log_event(self.log_file, "WinAdminService is now running.")
#             main()
#         except Exception as e:
#             log_event(self.log_file, f"Error in run_main: {e}")
#             self.SvcStop()

#     def SvcStop(self):
#         try:
#             self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
#             win32event.SetEvent(self.hWaitStop)
#             self.ReportServiceStatus(win32service.SERVICE_STOPPED)
#             servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
#                                   servicemanager.PYS_SERVICE_STOPPED,
#                                   (self._svc_name_, ''))
#             log_event(self.log_file, "WinAdminService has stopped.")
#         except Exception as e:
#             log_event(self.log_file, f"Error in SvcStop: {e}")
    
# if __name__ == '__main__':
#     ensure_log_directory(WinAdminService.log_file)
#     if '--debug' in sys.argv:
#         log_event(WinAdminService.log_file, "WinAdminService is running in debug mode.")
#         try:
#             main()  # Run the main logic directly
#         except Exception as e:
#             log_event(WinAdminService.log_file, f"Error in debug mode: {e}")
#     else:
#         try:
#             log_event(WinAdminService.log_file, f"Service command received: {sys.argv[1]}")
#             win32serviceutil.HandleCommandLine(WinAdminService)
#         except Exception as e:
#             log_event(WinAdminService.log_file, f"Error in service command: {e}")


import sys
import win32serviceutil
import win32service
import win32event
import servicemanager
import os
from src.utils import log_event, ensure_log_directory

class WinAdminService(win32serviceutil.ServiceFramework):
    _svc_name_ = "WinAdminService"
    _svc_display_name_ = "WinAdmin Minimal Service"
    _svc_description_ = "A minimal service to test Windows service setup."
    
    log_file = "log/winadmin.log"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        log_event(self.log_file, "WinAdminService is starting (minimal setup).")
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
        log_event(self.log_file, "WinAdminService is running (minimal setup).")

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        log_event(self.log_file, "WinAdminService has stopped (minimal setup).")

if __name__ == '__main__':
    ensure_log_directory(WinAdminService.log_file)
    win32serviceutil.HandleCommandLine(WinAdminService)
