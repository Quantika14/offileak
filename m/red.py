import psutil, time
import m.logger as log
import m.telegram as TL
import subprocess

def get_red():
    interfaces = psutil.net_if_stats()
    for interfaz, valores in interfaces.items():
        if valores.isup:
            addrs = psutil.net_if_addrs()[interfaz]
            for addr in addrs:
                if addr.family == 2:
                    if interfaz.startswith('Ethernet'):
                        log.save_info(f"Connect {interfaz}")
                        return f"Cable a la red {interfaz}"
                    elif interfaz.startswith('Wi-Fi'):
                        log.save_info(f"Connect {interfaz}")
                        return f"WiFi a la red {interfaz}"
    return None



def get_ssid():
    redes = subprocess.run(["netsh", "wlan", "show", "interface"], capture_output=True, text=True).stdout
    for linea in redes.split("\n"):
        if "SSID" in linea:
            ssid = linea.split(":")[1].strip()
            return ssid
    return None

def moniRED(interfaz):


    while True:

        try:
            
            interfaz_now = get_ssid()

            if interfaz == interfaz_now:
                time.sleep(10)
                print (interfaz_now, interfaz)

            else:
                print("BINGO")
                print (interfaz_now, interfaz)
                TL.send_message(f"Red Wi-Fi cambiada a {interfaz_now}")
                time.sleep(10)

        except Exception as e:
            log.save_error(e)


        