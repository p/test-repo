d = (args...)->
  console.log args...

page = require('webpage').create()

fixsubmit = (selector)->
  form = document.querySelector selector
  for element in form.elements
    if ((element.tagName.toLowerCase() == 'input' ||
        element.tagName.toLowerCase() == 'button') &&
        element.type.toLowerCase() == 'submit')
      
      if element.name != undefined && element.value != undefined
        hidden = document.createElement('input')
        hidden.type = 'hidden'
        hidden.name = element.name
        hidden.value = element.value
        hidden.className = 'phantomjs-form-submit-workaround'
        form.appendChild hidden
        return form.innerHTML

page.open 'http://localhost:8773', (status)->
  d page.evaluate ->
    document.forms[0].name
  
  d page.evaluate fixsubmit, 'form[name=fooform]'
  
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
# <input type="hidden" name="h" value="hv"><input type="submit" name="s" value="sv"><input type="hidden" name="s" value="sv" class="phantomjs-form-submit-workaround">
# http://localhost:8773/send
# h=hv&s=sv
