#!/usr/bin/env python

# Dependencies: redis, botttle (http://bottlepy.org/docs/dev/index.html)

import redis, json
import urllib, cgi, sys

class Consumer(object):
    def __init__(self, name):
        self.name = name
    
    @property
    def url(self):
        return 'https://api.datasource.com/next/%s' % cgi.escape(self.name)
    
    def __call__(self):
        io = urllib.urlopen(self.url)
        body = io.read()
        print(body)
        data = json.loads(body)
        return data['current']

class TestConsumer(object):
    def __init__(self, name, items):
        self.name = name
        self.items = items
    
    def __call__(self):
        return self.items.pop(0)

class DataStore(object):
    def __init__(self):
        self.redis = redis.Redis()
    
    def get(self, name):
        value = self.redis.get('pq:%s' % name)
        # workaround
        if value and value != 'None':
            return int(value)
        else:
            return None
    
    def put(self, name, value):
        if not value:
            # redis stores None as "None"
            value = ''
        self.redis.set('pq:%s' % name, value)

class TestDataStore(object):
    def __init__(self):
        self.store = {}
    
    def get(self, name):
        return self.store.get(name)
    
    def put(self, name, value):
        self.store[name] = value

class Service(object):
    def __init__(self, ca, cb, ds):
        self.ca, self.cb, self.ds = ca, cb, ds
    
    def __call__(self):
        va = self.ds.get(self.ca.name)
        if va is None:
            va = self.ca()
        vb = self.ds.get(self.cb.name)
        if vb is None:
            vb = self.cb()
        if va <= vb:
            self.ds.put(self.ca.name, None)
            self.ds.put(self.cb.name, vb)
            return va
        else:
            self.ds.put(self.ca.name, va)
            self.ds.put(self.cb.name, None)
            return vb

class History(object):
    def __init__(self, service, ds, name):
        self.service = service
        self.ds = ds
        self.name = name
    
    def __call__(self):
        current = self.service()
        last = self.ds.get('last:%s' % self.name)
        self.ds.put('last:%s' % self.name, current)
        return current, last

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        r = redis.Redis()
        for key in r.keys('*'):
            r.delete(key)
        
        ca = TestConsumer('ta', [2, 3, 8])
        assert ca() == 2
        assert ca() == 3
        assert ca() == 8
        
        for ds in TestDataStore(), DataStore():
            assert ds.get('txmissing') is None
            ds.put('tx', 1)
            assert ds.get('tx') == 1
            ds.put('tx', None)
            assert ds.get('tx') is None
        
        for ds in TestDataStore(), DataStore():
            ca = TestConsumer('ta', [2, 3, 8, 99])
            cb = TestConsumer('tb', [4, 5, 6, 99])
            service = Service(ca, cb, ds)
            assert service() == 2
            assert service() == 3
            assert service() == 4
            assert service() == 5
            assert service() == 6
            assert service() == 8
            
            ca = TestConsumer('te', [1, 1, 10, 99])
            cb = TestConsumer('tf', [1, 2, 10, 99])
            service = Service(ca, cb, ds)
            assert service() == 1
            assert service() == 1
            assert service() == 1
            assert service() == 2
            assert service() == 10
            assert service() == 10
            
            ca = TestConsumer('tc', [2, 3, 8, 99])
            cb = TestConsumer('td', [4, 5, 6, 99])
            service = History(Service(ca, cb, ds), ds, 'tc/td')
            assert service() == (2, None)
            assert service() == (3, 2)
            assert service() == (4, 3)
            assert service() == (5, 4)
            assert service() == (6, 5)
            assert service() == (8, 6)
    else:
        import bottle
        
        data_store = DataStore()
        
        @bottle.route('/quiz/merge')
        def merge():
            ca = Consumer(bottle.request.query['stream1'])
            cb = Consumer(bottle.request.query['stream2'])
            history_name = '%s/%s' % (bottle.request.query['stream1'], bottle.request.query['stream2'])
            service = History(Service(ca, cb, data_store), data_store, history_name)
            current, last = service()
            data = dict(current=current, last=last)
            body = json.dumps(data)
            return body
        
        bottle.run()
