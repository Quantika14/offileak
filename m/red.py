import psutil
import m.logger as logger

def get_red():
    interfaces = psutil.net_if_stats()
    for interfaz, valores in interfaces.items():
        if valores.isup:
            addrs = psutil.net_if_addrs()[interfaz]
            for addr in addrs:
                if addr.family == 2:
                    if interfaz.startswith('Ethernet'):
                        logger.save_info(f"Connect {interfaz}")
                        return f"Cable a la red {interfaz}"
                    elif interfaz.startswith('Wi-Fi'):
                        logger.save_info(f"Connect {interfaz}")
                        return f"WiFi a la red {interfaz}"
    return None
