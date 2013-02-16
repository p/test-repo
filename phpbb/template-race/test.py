import webracer
import threading

ok = 0
failed = 0
lock = threading.Lock()

def req(s):
    global ok, failed, lock

    s.get('http://func/posting.php?mode=post&f=2')
    if 'Subject:' in s.response.body:
        ok += 1
    else:
        failed += 1
    
    lock.acquire()
    try:
        print '%d ok, %d failed' % (ok, failed)
    finally:
        lock.release()

def reqmany():
    s = webracer.Session()
    for i in range(100):
        req(s)

threads = []
for i in range(10):
    thread = threading.Thread(target=reqmany)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

# ~ 1 in 7 checks fail
