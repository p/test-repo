import socket
import threading
import time

port = 9310

class ServerThread(threading.Thread):
    def run(self):
        # Having import here prevents the app from listening.
        # Note that socket is also imported globally.
        import time
        
        s = socket.socket()
        s.bind(('127.0.0.1', port))
        print(s.listen(1))
        
        print("Listening on port %d..." % port)
        
        while True:
            conn, addr = s.accept()
            conn.close()

def start_server():
    server_thread = ServerThread()
    server_thread.daemon = True
    server_thread.start()

def wait_for_server():
    ok = False
    for i in range(10):
        try:
            conn = socket.create_connection(('127.0.0.1', port), 0.1)
            ok = True
            conn.close()
            break
        except socket.error as e:
            time.sleep(0.1)
    if not ok:
        import warnings
        warnings.warn('Server did not start after 1 second')

start_server()
wait_for_server()
