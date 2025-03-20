# -*- coding: utf-8 -*-
# import pwdb.web.webserver
from ligre.core.conf import Conf
import ligre.conf.settings as cfg
import os
import sys
import time
import subprocess
import threading
from http.server import SimpleHTTPRequestHandler
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
# from pwdb.core.session import Session
# from pwdb.core.webserver import WebServer
# from pwdb.core.conf import Conf
# import pwdb.conf 
# import pandas
d1 = {
    "a": {
        "abc": [1, 2, 3]
    },
    "b": 2,
    "c": [1, 2, 3]
}
d2 = {
    "a": {
        "abc": [4, 5, 6],
        "xpto": [4, 5, 6]
    },
    "b": 4,
    "c": [4, 5, 6]
}

# print(d1 | d2)
# print(fn.merge_recursive(d1, d2))
c=Conf('settings.json')
print(c('$.formats'))
quit()

# Conf('dsn.json')
# Conf('config.ini')


class MonitorHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_modified = 0
        self.debounce_timer = None
        self.cont = 0

    def dispatch(self, event):
        """Intercepta o evento antes de repassá-lo para os métodos específicos."""
        self.cont += 1
        print(f"Event({self.cont}): {event.event_type} - {event.src_path}")
        if event.is_directory:
            print(f"Is directory")
            return
        now = time.time()
        if now - self.last_modified < 1:  # Ignora eventos repetidos em menos de 1 segundo
            return
        self.last_modified = now

        # Agora repassa para os métodos padrão
        super().dispatch(event)

    def on_created(self, event):
        print(f"Create({self.cont}): {event.src_path}")

    def on_modified(self, event):
        print(f"Modify({self.cont}): {event.src_path}")
        python = sys.executable
        os.execl(python, python, *sys.argv)
        # subprocess.run(["python3", "script_a_ser_executado.py"])

    def on_deleted(self, event):
        print(f"Remove({self.cont}): {event.src_path}")

    def on_moved(self, event):
        print(
            f"Move({self.cont}): {event.src_path} -> {event.dest_path}")


if __name__ == "__main__":
    # Iniciar servidores com parâmetros
    WebServer.HTTP_PORT = 80
    WebServer.HTTPS_PORT = 443
    WebServer.KEYFILE = "/cer/key.pem"
    WebServer.CERTFILE = "/cer/cert.pem"

    threading.Thread(
        target=WebServer,
        kwargs={"https": True, "handler": HttpHandler},  # HTTPS
        daemon=True
    ).start()
    threading.Thread(
        target=WebServer,
        kwargs={"https": False, "handler": HttpHandler_Redirect},  # HTTP
        daemon=True
    ).start()

    event_handler = MonitorHandler()
    observer = Observer()
    observer.schedule(
        event_handler,
        sys.path[0],  # os.path.dirname(__file__),
        recursive=True
    )

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('Go out observer')
        observer.stop()
    observer.join()


# HTTPS
# linux: openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
