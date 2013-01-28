casper.start()

casper.then ->
  @open 'http://www.python.org/'

casper.then ->
  @click {type: 'xpath', path: '//missing'}

casper.run ->
  @test.done()

