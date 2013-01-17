import socket
import threading
import time
import unittest
from wsgiref.simple_server import make_server, demo_app

port = 9312

class ServerThread(threading.Thread):
    def run(self):
        httpd = make_server('', port, demo_app)
        print("Serving HTTP on port %d..." % port)

        # Respond to requests until process is killed
        httpd.serve_forever()

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
            break
        except socket.error as e:
            time.sleep(0.1)
    if not ok:
        import warnings
        warnings.warn('Server did not start after 1 second')

start_server()
wait_for_server()

class FailingTest(unittest.TestCase):
    def test_a(self):
        socket.create_connection(('127.0.0.1', port), 1)
    
    def test_b(self):
        socket.create_connection(('127.0.0.1', port), 1)

if __name__ == '__main__':
    unittest.main()
