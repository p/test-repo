Without patch:

<pre>
rvm@reactor casperjs % ./bin/casperjs test ~pie/apps/test-repo/casperjs/format-selector/test.coffee
Test file: /home/pie/apps/test-repo/casperjs/format-selector/test.coffee        
FAIL Cannot dispatch click event on nonexistent selector: [object Object]
#    type: uncaughtError
#    file: /home/pie/apps/test-repo/casperjs/format-selector/test.coffee:1155
#    error: Cannot dispatch click event on nonexistent selector: [object Object]
#           CasperError: Cannot dispatch click event on nonexistent selector: [object Object]
#               at mouseEvent (:1155)
#               at click (:404)
#               at /home/pie/apps/test-repo/casperjs/format-selector/test.coffee:12
#               at runStep (:1348)
#               at checkStep (:347)
#    stack: not provided
CasperError: Cannot dispatch click event on nonexistent selector: [object Object]
  /home/rvm/apps/casperjs:1155 in mouseEvent
  /home/rvm/apps/casperjs:404 in click
  /home/pie/apps/test-repo/casperjs/format-selector/test.coffee:12
  /home/rvm/apps/casperjs:1348 in runStep
  /home/rvm/apps/casperjs:347 in checkStep
FAIL 1 tests executed in 1.888s, 0 passed, 1 failed.                            

Details for the 1 failed test:

In /home/pie/apps/test-repo/casperjs/format-selector/test.coffee:1155
  Untitled suite in /home/pie/apps/test-repo/casperjs/format-selector/test.coffee
    uncaughtError: Cannot dispatch click event on nonexistent selector: [object Object]
</pre>

With patch:

<pre>
rvm@reactor casperjs % ./bin/casperjs test ~pie/apps/test-repo/casperjs/format-selector/test.coffee
Test file: /home/pie/apps/test-repo/casperjs/format-selector/test.coffee        
FAIL Cannot dispatch click event on nonexistent selector: [selector type=xpath, path=//missing]
#    type: uncaughtError
#    file: /home/pie/apps/test-repo/casperjs/format-selector/test.coffee:1165
#    error: Cannot dispatch click event on nonexistent selector: [selector type=xpath, path=//missing]
#           CasperError: Cannot dispatch click event on nonexistent selector: [selector type=xpath, path=//missing]
#               at mouseEvent (:1165)
#               at click (:404)
#               at /home/pie/apps/test-repo/casperjs/format-selector/test.coffee:12
#               at runStep (:1358)
#               at checkStep (:347)
#    stack: not provided
CasperError: Cannot dispatch click event on nonexistent selector: [selector type=xpath, path=//missing]
  /home/rvm/apps/casperjs:1165 in mouseEvent
  /home/rvm/apps/casperjs:404 in click
  /home/pie/apps/test-repo/casperjs/format-selector/test.coffee:12
  /home/rvm/apps/casperjs:1358 in runStep
  /home/rvm/apps/casperjs:347 in checkStep
FAIL 1 tests executed in 1.78s, 0 passed, 1 failed.                             

Details for the 1 failed test:

In /home/pie/apps/test-repo/casperjs/format-selector/test.coffee:1165
  Untitled suite in /home/pie/apps/test-repo/casperjs/format-selector/test.coffee
    uncaughtError: Cannot dispatch click event on nonexistent selector: [selector type=xpath, path=//missing]
</pre>
