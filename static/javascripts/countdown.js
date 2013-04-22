(function() {
  var _this = this;

  $(function() {
    return CountDown.initialize();
  });

  this.CountDown = {
    secondsleft: -1,
    refresh: true,
    initialize: function() {
      if ($('#turn-countdown').length > 0) {
        CountDown.secondsLeft = parseInt($('#turn-countdown').data('seconds-left'));
        if (CountDown.secondsLeft === 0) {
          CountDown.refresh = false;
        }
        return CountDown.tick();
      }
    },
    triggerTick: function() {
      return window.setTimeout(CountDown.tick, 1000);
    },
    tick: function() {
      var d, h, m;
      d = new Date();
      CountDown.secondsLeft--;
      if (CountDown.secondsLeft < -90 && CountDown.refresh) {
        window.location.reload();
      }
      m = Math.max(Math.floor(CountDown.secondsLeft / 60), 0);
      h = Math.max(Math.floor(m / 60), 0);
      m -= h * 60;
      if (h < 10) {
        h = "0" + h;
      }
      if (m < 10) {
        m = "0" + m;
      }
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
