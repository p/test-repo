var foobar = (function() {
  var foobar = function () {
  };
  
  foobar.prototype.test = function() {
    console.log(this);
  };

  console.log(foobar);
  return foobar;
})();

var instance = new foobar();
instance.test();

//console.log(instance);
