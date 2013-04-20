(function() {

  $(window).on('load', function() {
    return BackdropScaler.initialize();
  });

  this.BackdropScaler = {
    aspectRatio: 1,
    initialize: function() {
      if ($('#backdrop').length > 0) {
        BackdropScaler.aspectRatio = $('#backdrop').width() / $('#backdrop').height();
        $(window).on('resize', function() {
          return BackdropScaler.resize();
        });
        return this.resize();
      }
    },
    resize: function() {
      if (($(window).width() / $(window).height()) < BackdropScaler.aspectRatio) {
        return $('#backdrop').removeClass().addClass('bgheight');
      } else {
        return $('#backdrop').removeClass().addClass('bgwidth');
      }
    }
  };

}).call(this);
