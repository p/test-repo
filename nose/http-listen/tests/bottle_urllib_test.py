import socket
import threading
import time
import unittest
import urllib
import bottle

port = 9313

class ServerThread(threading.Thread):
    def run(self):
        app = bottle.Bottle()
        
        @app.route('/')
        def index():
            return 'success'
        
        bottle.run(app, host='localhost', port=port)

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
        urllib.urlopen('http://127.0.0.1:%d' % port).read()
    
    def test_b(self):
        urllib.urlopen('http://127.0.0.1:%d' % port).read()
    
    def test_c(self):
        urllib.urlopen('http://127.0.0.1:%d' % port).read()

if __name__ == '__main__':
    unittest.main()
