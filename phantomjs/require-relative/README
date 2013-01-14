PhantomJS: absolute path invocation works:

<pre>
% ~rvm/opt/phantomjs/bin/phantomjs ~pie/apps/test-repo/phantomjs/require-relative/test.js                                                         
1
2
</pre>

CasperJS on the same file hangs:

<pre>
% casperjs ~pie/apps/test-repo/phantomjs/require-relative/test.js
CasperError: CasperJS couldn't find module ./sub

  /home/rvm/opt/casperjs/bin/bootstrap.js:133 in _require
  /home/pie/apps/test-repo/phantomjs/require-relative/test.js:1
^C
</pre>
