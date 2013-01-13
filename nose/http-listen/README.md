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
