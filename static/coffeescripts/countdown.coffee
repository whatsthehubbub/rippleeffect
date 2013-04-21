$ ->
  CountDown.initialize()

@CountDown =

  secondsleft: -1


# hook up event handlers and intialize
  initialize: =>
    if $('#turn-countdown').length > 0
      CountDown.secondsLeft = parseInt($('#turn-countdown').data('seconds-left'));
      CountDown.tick()

  triggerTick: =>
    window.setTimeout(CountDown.tick, 1000)

  tick: =>
    d = new Date()

    # todo: we could only do this every minute, but it would be a bit less accurate
    # todo: reload the page when we hit 0?
    CountDown.secondsLeft--

    # reload the page when the turn has passed
    if CountDown.secondsLeft < -10
      window.location.reload()

    m = Math.max(Math.floor(CountDown.secondsLeft / 60), 0);
    h = Math.max(Math.floor(m / 60), 0);
    m -= h * 60

    if h < 10
      h = "0" + h

    if m < 10
      m = "0" + m

    $('#turn-countdown .hours').text(h)
    $('#turn-countdown .minutes').text(m)

    if d.getSeconds() % 2 == 0
      $('.time-colon').css('visibility', 'hidden')
    else
      $('.time-colon').css('visibility', 'visible')

    CountDown.triggerTick()