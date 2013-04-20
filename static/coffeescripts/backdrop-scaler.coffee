#$(window).load(function() {
#                          var theWindow        = $(window),
#                          $bg              = $("#bg"),
#                          aspectRatio      = $bg.width() / $bg.height();
#
#               function resizeBg() {
#                 if ( (theWindow.width() / theWindow.height()) < aspectRatio ) {
#                                                                               $bg
#                                                                                 .removeClass()
#                                                                                 .addClass('bgheight');
#} else {
#$bg
#  .removeClass()
#  .addClass('bgwidth');
#}
#}
#theWindow.resize(resizeBg).trigger("resize");/
#});


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
      $('#backdrop').removeClass().addClass('bgheight')
    else
      $('#backdrop').removeClass().addClass('bgwidth')