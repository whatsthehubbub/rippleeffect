(function() {

  $(function() {
    return RE.initialize();
  });

  this.RE = {
    initialize: function() {
      $(window).on('resize', function() {
        return RE.resize();
      });
      $(window).on('keyup', RE.catchKey);
      $(document).on('click', 'html:not(.touch) a:not(.js-no-refresh)', RE.handleButtonClick);
      $(document).on('click', 'html.touch a:not(.js-no-refresh)', RE.handleButtonTouch);
      return this.resize();
    },
    resize: function() {
      return $('#sidebar').height($(window).height());
    },
    catchKey: function(event) {
      if (event.keyCode === 68) {
        return $('.debug').show();
      }
    },
    handleButtonClick: function(e) {},
    handleButtonTouch: function(e) {
      e.preventDefault();
      window.location.assign($(this).attr('href'));
      return false;
    }
  };

}).call(this);
