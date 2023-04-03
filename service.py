import os
import sys
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import agent as agent

#********************************************************************************************************************************
#       COMANDOS PARA CORRECTO FUNCIONAMIENTO DEL SERVICIO
#       python my_service.py install
#       python my_service.py start
#       python my_service.py stop
#       python my_service.py remove


class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'OFFICELEAK AGENT'
    _svc_display_name_ = 'Agent Windows Service - OFFICELEAK'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.is_alive = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_alive = False

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        # Aquí va el código de tu script de Python
        while self.is_alive:
            # Reemplaza la siguiente línea con tu lógica
            agent.main()
            print("El servicio está funcionando")

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(MyService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(MyService)