express = require 'express'

app = express()
app.use express.bodyParser()

form = '
<html>
<head></head>
<body>
<form action="/send" method="post" name="fooform">
<input type="hidden" name="h" value="hv" />
<input type="submit" name="s" value="sv" />
</body></html>
'

app.get '/', (req, res)->
  res.setHeader 'Content-Type', 'text/html'
  res.setHeader 'Content-Length', form.length
  res.end form

app.post '/send', (req, res)->
  body = []
  for param of req.body
    body.push param + '=' + req.body[param]
  body = body.join '&'
  res.setHeader 'Content-Type', 'text/plain'
  res.setHeader 'Content-Length', body.length
  res.end body

app.listen 8773
console.log 'Listening on port 8773'

# Submitting the form should produce:
# h=hv&s=sv
