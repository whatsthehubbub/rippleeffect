$ ->
  RE.initialize()

@RE =

  # hook up event handlers and intialize
  initialize: ->
    $(window).on('resize', -> RE.resize())
    @resize()

  # update sidebar height when viewport is resized
  resize: ->
    $('#sidebar').height($(window).height());