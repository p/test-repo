d = (args...)->
  console.log args...

page = require('webpage').create()

page.open 'http://localhost:8773', (status)->
  d page.evaluate ->
    document.forms[0].name
  page.evaluate ->
    document.forms[0].submit()
  setTimeout next, 1000

next = ->
  d page.url
  d page.plainText
  phantom.exit()

# should print:
#
# fooform
# http://localhost:8773/send
# h=hv&s=sv

# actually prints:
#
# fooform
# http://localhost:8773/send
# h=hv
#
# (submit button's name-value not sent to the server)
