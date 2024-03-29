$(window).on('load', -> BackdropScaler.initialize() )

@BackdropScaler =

  aspectRatio: 1,

  initialize: ->
    if($('#backdrop').length > 0)
      BackdropScaler.aspectRatio = $('#backdrop').width() / $('#backdrop').height()
      $(window).on('resize', -> BackdropScaler.resize())
      @resize()

  resize: ->
    if ( $(window).width() / $(window).height() ) < BackdropScaler.aspectRatio
      $('#backdrop').removeClass('bgwidth').addClass('bgheight')
    else
      $('#backdrop').removeClass('bgheight').addClass('bgwidth')
    $('#backdrop').show()