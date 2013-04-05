(function() {

  $(function() {
    return $('.placeholder-container').each(function(i, el) {
      var $el;
      $el = $(el);
      return $el.find(':nth-child(1)').watermark($el.data('placeholder'), {
        useNative: false
      });
    });
  });

}).call(this);
