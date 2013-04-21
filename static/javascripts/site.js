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
      return this.resize();
    },
    resize: function() {
      return $('#sidebar').height($(window).height());
    },
    catchKey: function(event) {
      if (event.keyCode === 68) {
        return $('.debug').show();
      }
    }
  };

}).call(this);
