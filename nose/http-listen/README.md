These tests create an HTTP server on a daemon thread
and attempt to connect to it via a socket.

The first test uses wsgiref, the second test uses bottle.

wsgiref test works when running a test directly and via nose.
bottle test works when running it directly, but when run via nose
the server does not begin to listen.

It does not matter how long the code waits for the server to start.

Interestingly, when running the entire suite via nosetests
the code that waits for the server to start fails but by the time
tests are executed the server is operational.

python wsgiref:

<pre>
pie@reactor http-listen % python tests/wsgiref_test.py
Serving HTTP on port 9312...
..
----------------------------------------------------------------------
Ran 2 tests in 0.001s

OK
</pre>

python bottle:

<pre>
pie@reactor http-listen % python tests/bottle_test.py
Bottle v0.11.4 server starting up (using WSGIRefServer())...
Listening on http://localhost:9312/
Hit Ctrl-C to quit.

..
----------------------------------------------------------------------
Ran 2 tests in 0.001s

OK
</pre>

nosetests wsgiref:

<pre>
pie@reactor http-listen % nosetests tests/wsgiref_test.py
..
----------------------------------------------------------------------
Ran 2 tests in 0.001s

OK
</pre>

nosetests bottle:

<pre>
pie@reactor http-listen % nosetests tests/bottle_test.py
Bottle v0.11.4 server starting up (using WSGIRefServer())...
Listening on http://localhost:9312/
Hit Ctrl-C to quit.

/home/pie/apps/test-repo/nose/http-listen/tests/bottle_test.py:35: UserWarning: Server did not start after 1 second
  warnings.warn('Server did not start after 1 second')
EE
======================================================================
ERROR: test_a (tests.bottle_test.FailingTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/pie/apps/test-repo/nose/http-listen/tests/bottle_test.py", line 42, in test_a
    socket.create_connection(('127.0.0.1', port), 1)
  File "/usr/local/lib/python2.7/socket.py", line 571, in create_connection
    raise err
error: [Errno 61] Connection refused

======================================================================
ERROR: test_b (tests.bottle_test.FailingTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/pie/apps/test-repo/nose/http-listen/tests/bottle_test.py", line 45, in test_b
    socket.create_connection(('127.0.0.1', port), 1)
  File "/usr/local/lib/python2.7/socket.py", line 571, in create_connection
    raise err
error: [Errno 61] Connection refused

----------------------------------------------------------------------
Ran 2 tests in 0.011s

FAILED (errors=2)
</pre>

nosetests:

<pre>
pie@reactor http-listen % nosetests
Bottle v0.11.4 server starting up (using WSGIRefServer())...
Listening on http://localhost:9312/
Hit Ctrl-C to quit.

/home/pie/apps/test-repo/nose/http-listen/tests/bottle_test.py:35: UserWarning: Server did not start after 1 second
  warnings.warn('Server did not start after 1 second')
....
----------------------------------------------------------------------
Ran 4 tests in 1.094s

OK
</pre>

(There is a 1 second delay while the server start code waits for the server
to materialize which becomes problematic in a real test suite that starts
many servers.)

When I only was attempting to establish a socket connection, I had two
identical tests (test_a and test_b) and they both failed.
In my actual application I was connecting via httplib and
the first request consistently failed but subsequent requests succeeded.

The bottle urllib test now reproduces the same behavior:

<pre>
pie@reactor http-listen % nosetests tests/bottle_urllib_test.py
Bottle v0.11.4 server starting up (using WSGIRefServer())...
Listening on http://localhost:9313/
Hit Ctrl-C to quit.

/home/pie/apps/test-repo/nose/http-listen/tests/bottle_urllib_test.py:36: UserWarning: Server did not start after 1 second
  warnings.warn('Server did not start after 1 second')
Ef.here - - [12/Jan/2013 23:43:21] "GET / HTTP/1.0" 200 7
.f.here - - [12/Jan/2013 23:43:21] "GET / HTTP/1.0" 200 7
.
======================================================================
ERROR: test_a (tests.bottle_urllib_test.FailingTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/pie/apps/test-repo/nose/http-listen/tests/bottle_urllib_test.py", line 43, in test_a
    urllib.urlopen('http://127.0.0.1:%d' % port).read()
  File "/usr/local/lib/python2.7/urllib.py", line 86, in urlopen
    return opener.open(url)
  File "/usr/local/lib/python2.7/urllib.py", line 207, in open
    return getattr(self, name)(url)
  File "/usr/local/lib/python2.7/urllib.py", line 344, in open_http
    h.endheaders(data)
  File "/usr/local/lib/python2.7/httplib.py", line 954, in endheaders
    self._send_output(message_body)
  File "/usr/local/lib/python2.7/httplib.py", line 814, in _send_output
    self.send(msg)
  File "/usr/local/lib/python2.7/httplib.py", line 776, in send
    self.connect()
  File "/usr/local/lib/python2.7/httplib.py", line 757, in connect
    self.timeout, self.source_address)
  File "/usr/local/lib/python2.7/socket.py", line 571, in create_connection
    raise err
IOError: [Errno socket error] [Errno 61] Connection refused

----------------------------------------------------------------------
Ran 3 tests in 0.008s

FAILED (errors=1)
</pre>

However this test appears to intermittently work:

<pre>
pie@reactor http-listen % nosetests tests/bottle_urllib_test.py
Bottle v0.11.4 server starting up (using WSGIRefServer())...
Listening on http://localhost:9313/
Hit Ctrl-C to quit.

/home/pie/apps/test-repo/nose/http-listen/tests/bottle_urllib_test.py:36: UserWarning: Server did not start after 1 second
  warnings.warn('Server did not start after 1 second')
f.here - - [12/Jan/2013 23:43:14] "GET / HTTP/1.0" 200 7
.f.here - - [12/Jan/2013 23:43:14] "GET / HTTP/1.0" 200 7
.f.here - - [12/Jan/2013 23:43:14] "GET / HTTP/1.0" 200 7
.
----------------------------------------------------------------------
Ran 3 tests in 0.008s

OK
</pre>

nosetests, again, succeeds despite waiting code failing:

<pre>
pie@reactor http-listen % nosetests
Bottle v0.11.4 server starting up (using WSGIRefServer())...
Listening on http://localhost:9312/
Hit Ctrl-C to quit.

/home/pie/apps/test-repo/nose/http-listen/tests/bottle_test.py:35: UserWarning: Server did not start after 1 second
  warnings.warn('Server did not start after 1 second')
Bottle v0.11.4 server starting up (using WSGIRefServer())...
Listening on http://localhost:9313/
Hit Ctrl-C to quit.

/home/pie/apps/test-repo/nose/http-listen/tests/bottle_urllib_test.py:36: UserWarning: Server did not start after 1 second
  warnings.warn('Server did not start after 1 second')
...f.here - - [12/Jan/2013 23:44:01] "GET / HTTP/1.0" 200 7
.f.here - - [12/Jan/2013 23:44:01] "GET / HTTP/1.0" 200 7
.f.here - - [12/Jan/2013 23:44:01] "GET / HTTP/1.0" 200 7
...
----------------------------------------------------------------------
Ran 8 tests in 2.264s

OK
</pre>

Environment:

<pre>
pie@reactor http-listen % python -V
Python 2.7.3
pie@reactor http-listen % uname -a
FreeBSD reactor.here 9.1-RELEASE FreeBSD 9.1-RELEASE #0 r243825: Tue Dec  4 09:23:10 UTC 2012     root@farrell.cse.buffalo.edu:/usr/obj/usr/src/sys/GENERIC  amd64
</pre>
