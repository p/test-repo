partial = require 'partial'

d = console.log

foo = (x, y, z)->
  #d x, y, z
  x * y + z

class Bar
  constructor: ()->
    @base = 1000
  
  foo: (x, y, z)->
    d this, @base, x, y, z
    @base + x * y + z

assert = require 'assert'

pfoo = partial(foo)(2)
assert.equal(16, pfoo(3, 10))

b = new Bar
pbar = partial(b.foo.bind(b))(2)
assert.equal(1016, pbar(3, 10))
