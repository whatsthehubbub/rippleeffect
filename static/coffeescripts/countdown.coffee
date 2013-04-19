$ ->
  CountDown.initialize()

@CountDown =

  secondsleft: -1


# hook up event handlers and intialize
  initialize: =>
    if $('#turn-countdown').length > 0
      CountDown.secondsLeft = parseInt($('#turn-countdown').data('seconds-left'));
      CountDown.triggerTick();

  triggerTick: =>
    window.setTimeout(CountDown.tick, 1000)

  tick: =>
    d = new Date()

    # todo: we could only do this every minute, but it would be a bit less accurate
    # todo: reload the page when we hit 0?
    CountDown.secondsLeft--
    m = Math.floor(CountDown.secondsLeft / 60);
    h = Math.floor(m / 60);
    m -= h * 60
    $('#turn-countdown .hours').text(h)
    $('#turn-countdown .minutes').text(m)

    if d.getSeconds() % 2 == 0
      $('.time-colon').css('visibility', 'hidden')
    else
      $('.time-colon').css('visibility', 'visible')

    CountDown.triggerTick()