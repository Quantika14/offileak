import os, socket

def get_Username():
    return os.getlogin()

def get_computer_name():
    try:
        return socket.gethostname()
    except Exception as e:
        print(f"Error al obtener el nombre del equipo: {str(e)}")
        return None