function kill() {
  var subprocess = require('child_process');
  console.log('executing kill');
  var child = subprocess.spawn('kill', [require('system').pid]);
  console.log('executed kill');
}

var casper = require("casper").create();
//casper.exit();

// Without livelocks - as a fallback
setTimeout(kill, 5000);

// With livelocks
//kill();

// Livelock
//while(1) { }

// Currently fails with:
// CasperError: CasperJS couldn't find module child_process                        
//   /home/sandbox/casperjs/bin/bootstrap.js:133 in _require
//   /home/sandbox/casperjs/test.js:2 in kill
