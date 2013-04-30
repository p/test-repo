d = ->
  console.log arguments...

c1 = require('casper').create()
c2 = require('casper').create()

c1.start()
c2.start()

c1.then ->
  @open 'http://rpi.edu'
  
c1.then ->
  @test.assertTextExists('RPI')

c2.then ->
  @open 'http://debian.org'

c2.then ->
  @test.assertTextExists('Debian')

c1.run ->
  c2.run ->
    @test.done()
    c1.test.done()
