$ ->
  RE.initialize()

@RE =

  # hook up event handlers and intialize
  initialize: ->
    $(window).on('resize', -> RE.resize())
    $(window).on('keyup', RE.catchKey)
    # todo: differentiate between dismiss and continue

    $(document).on('mouseup', 'a.btn:not(.js-no-refresh)', RE.handleButtonClick)

    @resize()

  # update sidebar height when viewport is resized
  resize: ->
    $('#sidebar').height($(window).height());

  catchKey: (event) ->
    if event.keyCode == 68
      $('.debug').show();

  handleButtonClick: (e) ->
    e.preventDefault()
    document.location.href = $(this).attr('href')
    return false;
