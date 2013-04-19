$ ->
  CountDown.initialize()

@CountDown =


# hook up event handlers and intialize
  initialize: =>
    CountDown.triggerTick();

  triggerTick: =>
    window.setTimeout(CountDown.tick, 1000)

  tick: =>
    d = new Date()

    if d.getSeconds() % 2 == 0
      $('.time-colon').css('visibility', 'hidden')
    else
      $('.time-colon').css('visibility', 'visible')

    CountDown.triggerTick()