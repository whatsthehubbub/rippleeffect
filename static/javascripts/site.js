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
      $(document).on('mouseup', 'a.btn:not(.js-no-refresh)', RE.handleButtonClick);
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
    handleButtonClick: function(e) {
      e.preventDefault();
      document.location.href = $(this).attr('href');
      return false;
    }
  };

}).call(this);
