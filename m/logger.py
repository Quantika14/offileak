import logging

# Configurar logger para escribir en un archivo de log
logging.basicConfig(filename='log.txt', level=logging.INFO)

def guardar_informacion(mensaje):
    # Registrar mensaje de información en el archivo de log
    logging.info(mensaje)

def guardar_error(mensaje):
    # Registrar mensaje de error en el archivo de log
    logging.error(mensaje)