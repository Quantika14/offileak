import logging
import datetime

# Configurar logger para escribir en un archivo de log
logging.basicConfig(filename='log.txt', level=logging.INFO)

def save_info(mensaje):
    # Registrar mensaje de información en el archivo de log
    hora_actual = datetime.datetime.now().strftime('%H:%M:%S')
    mensaje = hora_actual + ", " + mensaje
    logging.info(mensaje)

def save_error(mensaje):
    # Registrar mensaje de error en el archivo de log
    hora_actual = datetime.datetime.now().strftime('%H:%M:%S')
    mensaje = hora_actual + ", " + mensaje
    logging.error(mensaje)