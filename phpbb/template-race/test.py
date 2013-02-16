import urllib
import threading

url = 'http://func/posting.php?mode=post&f=2'

ok = 0
failed = 0
lock = threading.Lock()

def req():
    global ok, failed, lock
    
    f = urllib.urlopen(url)
    body = f.read()
    if 'Subject:' in body:
        ok += 1
    else:
        failed += 1
    
    lock.acquire()
    try:
        print '%d ok, %d failed' % (ok, failed)
    finally:
        lock.release()

def reqmany():
    for i in range(100):
        req()

threads = []
for i in range(10):
    thread = threading.Thread(target=reqmany)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

# ~ 1 in 7 checks fail

# Requires DEBUG to be on in phpbb.

# The cause is template engine writes compiled code to file and then
# reads code back from file for evaluation, on each request.
# Since there is no locking for the read path, given concurrent writes
# to the same file eventually the read path will catch the file when
# it is being written to.
#
# Solutions:
# 1. do not read compiled code from file.
# 2. move compiled file in place (unix only but probably a better solution)
