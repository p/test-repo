import socket
import threading
import time
import unittest

port = 9311

class ServerThread(threading.Thread):
    def run(self):
        # Having an import here prevents the app from listening.
        # Any import will do, it does not have to be network-related.
        # The module could have been imported already or not,
        # makes no difference.
        import time
        
        s = socket.socket()
        s.bind(('127.0.0.1', port))
        s.listen(1)
        
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
