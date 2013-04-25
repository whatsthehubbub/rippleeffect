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
    $(document).on('click', '#load-messages', RE.handleMoreMessages)
    $(document).on('click', '.js-confirmable', RE.confirmLink)

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

  handleMoreMessages: (e) ->
    e.preventDefault()
    console.log('hier')

    currentPage = $('#message-list').data('current-page')
    lastPage = $('#message-list').data('last-page')
    endpoint = $('#message-list').data('endpoint')

    if(currentPage < lastPage)
      console.log('going')
      newPage = currentPage + 1
      $.get( endpoint+(newPage) ).done (data) ->
        $('#message-list').data('current-page', newPage)

        if newPage >= $('#message-list').data('last-page')
          $('#load-messages-container').remove()

        $('#message-list-container').append(data)

    return false

  confirmLink: (e) ->
    e.preventDefault()

    response = confirm( $(this).data('confirmation') )

    if response
      window.location.assign($(this).attr('href'))

    return false