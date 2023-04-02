import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import m.telegram as TL

class MonitorDirectory(FileSystemEventHandler):
    def on_modified(self, event):
        #print(f"Se ha modificado el archivo: {event.src_path}")
        TL.send_message(f"File has been modified: {event.src_path}")

    def on_created(self, event):
        #print(f"Se ha creado el archivo o carpeta: {event.src_path}")
        TL.send_message(f"The file or folder has been created: {event.src_path}")

    def on_deleted(self, event):
        #print(f"Se ha eliminado el archivo o carpeta: {event.src_path}")
        TL.send_message(f"The file or folder has been deleted: {event.src_path}")

def moniDirectory(path):
    event_handler = MonitorDirectory()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

