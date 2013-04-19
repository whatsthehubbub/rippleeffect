(function() {
  var _this = this;

  $(function() {
    return CountDown.initialize();
  });

  this.CountDown = {
    initialize: function() {
      return CountDown.triggerTick();
    },
    triggerTick: function() {
      return window.setTimeout(CountDown.tick, 1000);
    },
    tick: function() {
      var d;
      d = new Date();
      if (d.getSeconds() % 2 === 0) {
        $('.time-colon').css('visibility', 'hidden');
      } else {
        $('.time-colon').css('visibility', 'visible');
      }
      return CountDown.triggerTick();
    }
  };

}).call(this);
