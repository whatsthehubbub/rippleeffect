$ ->
  RE.initialize()

@RE =

  # hook up event handlers and intialize
  initialize: ->
    $(window).on('resize', -> RE.resize())
    $(window).on('keyup', RE.catchKey)
    # todo: differentiate between dismiss and continue

    $(document).on('click', 'html:not(.touch) a:not(.js-no-refresh)', RE.handleButtonClick)
    $(document).on('click', 'html.touch a:not(.js-no-refresh)', RE.handleButtonTouch)

    @resize()

  # update sidebar height when viewport is resized
  resize: ->
    $('#sidebar').height($(window).height());

  catchKey: (event) ->
    if event.keyCode == 68
      $('.debug').show();

  handleButtonClick:(e) ->
    # nothing, for now

  handleButtonTouch: (e) ->
    e.preventDefault()
    window.location.assign($(this).attr('href'))
    return false;
