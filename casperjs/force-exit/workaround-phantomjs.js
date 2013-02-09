function kill() {
  var subprocess = require('child_process');
  console.log('executing kill');
  var child = subprocess.spawn('kill', [require('system').pid]);
  console.log('executed kill');
}

//phantom.exit();

// Assuming no thread livelocks, as a fallback:
setTimeout(kill, 5000);

// If livelocks are expected, kill immediately:
//kill();

// livelock
//while(1) { }
