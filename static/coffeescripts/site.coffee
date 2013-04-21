$ ->
  RE.initialize()

@RE =

  # hook up event handlers and intialize
  initialize: ->
    $(window).on('resize', -> RE.resize())
    $(window).on('keyup', RE.catchKey)
    @resize()

  # update sidebar height when viewport is resized
  resize: ->
    $('#sidebar').height($(window).height());

  catchKey: (event) ->
    if event.keyCode == 68
      $('.debug').show();
