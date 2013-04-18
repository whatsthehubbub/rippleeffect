(function() {

  $(function() {
    return RE.initialize();
  });

  this.RE = {
    initialize: function() {
      $(window).on('resize', function() {
        return RE.resize();
      });
      return this.resize();
    },
    resize: function() {
      return $('#sidebar').height($(window).height());
    }
  };

}).call(this);
