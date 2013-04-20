$ ->
  Frontline.initialize()

@Frontline =

# hook up event handlers and intialize
  initialize: ->
    if($('#team-box').length > 0)
      @initTeamBox()

  # attach event handlers that update the current team mate form
  initTeamBox: ->
    events = "click"
    if $('html').hasClass('touch')
      events += " touchstart"

    console.log(events)

    $('#team-box .avatar').on(events, ->

      # deselect all team members, select the current one
      $('#team-box .avatar').removeClass('active')
      $(this).addClass('active')

      # populate the team box player
      $('#team-mate-name').text($(this).data('name'));
      $('#team-mate-email').text($(this).data('email'));
      $('#team-mate-inspect-id').val($(this).data('id'));
      $('#team-mate-predict-id').val($(this).data('id'));

      # hide the boilerpate, show the player
      $('#team-box-inactive').hide();
      $('#team-box-active').show();


    )