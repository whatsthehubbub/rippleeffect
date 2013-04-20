(function() {

  $(function() {
    return Frontline.initialize();
  });

  this.Frontline = {
    initialize: function() {
      if ($('#team-box').length > 0) {
        return this.initTeamBox();
      }
    },
    initTeamBox: function() {
      var events;
      events = "click";
      if ($('html').hasClass('touch')) {
        events += " touchstart";
      }
      console.log(events);
      return $('#team-box .avatar').on(events, function() {
        $('#team-box .avatar').removeClass('active');
        $(this).addClass('active');
        $('#team-mate-name').text($(this).data('name'));
        $('#team-mate-email').text($(this).data('email'));
        $('#team-mate-inspect-id').val($(this).data('id'));
        $('#team-mate-predict-id').val($(this).data('id'));
        $('#team-box-inactive').hide();
        return $('#team-box-active').show();
      });
    }
  };

}).call(this);
