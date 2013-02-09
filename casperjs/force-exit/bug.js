// https://github.com/n1k0/casperjs/issues/193

var casper = require("casper").create();
casper.exit();
while(1) { }
