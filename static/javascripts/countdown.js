(function() {
  var _this = this;

  $(function() {
    return CountDown.initialize();
  });

  this.CountDown = {
    secondsleft: -1,
    initialize: function() {
      if ($('#turn-countdown').length > 0) {
        CountDown.secondsLeft = parseInt($('#turn-countdown').data('seconds-left'));
        return CountDown.triggerTick();
      }
    },
    triggerTick: function() {
      return window.setTimeout(CountDown.tick, 1000);
    },
    tick: function() {
      var d, h, m;
      d = new Date();
      CountDown.secondsLeft--;
      m = Math.floor(CountDown.secondsLeft / 60);
      h = Math.floor(m / 60);
      m -= h * 60;
      $('#turn-countdown .hours').text(h);
      $('#turn-countdown .minutes').text(m);
      if (d.getSeconds() % 2 === 0) {
        $('.time-colon').css('visibility', 'hidden');
      } else {
        $('.time-colon').css('visibility', 'visible');
      }
      return CountDown.triggerTick();
    }
  };

}).call(this);
