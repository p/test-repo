These tests create an HTTP server on a daemon thread
and attempt to connect to it via a socket.

Both tests use wsgiref.

If wsgiref is imported at global module scope, the test works.

If wsgiref is imported from the daemon thread, the server does not
begin to listen no matter how long it is waited for, while it is waited for.

When running the tests via `nosetests <test>`, global import succeeds:

<pre>
pie@reactor http-listen % nosetests tests/wsgiref_test.py
..
----------------------------------------------------------------------
Ran 2 tests in 0.001s

OK
</pre>

Daemon thread import fails:

<pre>
pie@reactor http-listen % nosetests tests/wsgiref_broken_test.py
/home/pie/apps/test-repo/nose/http-listen/tests/wsgiref_broken_test.py:36: UserWarning: Server did not start after 1 second
  warnings.warn('Server did not start after 1 second')
EE
======================================================================
ERROR: test_a (tests.wsgiref_broken_test.FailingTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/pie/apps/test-repo/nose/http-listen/tests/wsgiref_broken_test.py", line 43, in test_a
    socket.create_connection(('127.0.0.1', port), 1)
  File "/usr/local/lib/python2.7/socket.py", line 571, in create_connection
    raise err
error: [Errno 61] Connection refused

======================================================================
ERROR: test_b (tests.wsgiref_broken_test.FailingTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/pie/apps/test-repo/nose/http-listen/tests/wsgiref_broken_test.py", line 46, in test_b
    socket.create_connection(('127.0.0.1', port), 1)
  File "/usr/local/lib/python2.7/socket.py", line 571, in create_connection
    raise err
error: [Errno 61] Connection refused

----------------------------------------------------------------------
Ran 2 tests in 0.002s

FAILED (errors=2)
</pre>

When running the entire suite via `nosetests`, despite the server
not beginning to listen while it is being waited for, the suite succeeds:

<pre>
pie@reactor http-listen % nosetests
/home/pie/apps/test-repo/nose/http-listen/tests/wsgiref_broken_test.py:36: UserWarning: Server did not start after 1 second
  warnings.warn('Server did not start after 1 second')
....
----------------------------------------------------------------------
Ran 4 tests in 1.169s

OK
</pre>

Environment:

<pre>
pie@reactor http-listen % python -V
Python 2.7.3
pie@reactor http-listen % uname -a
FreeBSD reactor.here 9.1-RELEASE FreeBSD 9.1-RELEASE #0 r243825: Tue Dec  4 09:23:10 UTC 2012     root@farrell.cse.buffalo.edu:/usr/obj/usr/src/sys/GENERIC  amd64
</pre>
