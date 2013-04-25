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
      $(document).on('click', '#load-messages', RE.handleMoreMessages);
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
    },
    handleMoreMessages: function(e) {
      var currentPage, endpoint, lastPage, newPage;
      e.preventDefault();
      console.log('hier');
      currentPage = $('#message-list').data('current-page');
      lastPage = $('#message-list').data('last-page');
      endpoint = $('#message-list').data('endpoint');
      if (currentPage < lastPage) {
        console.log('going');
        newPage = currentPage + 1;
        $.get(endpoint + newPage).done(function(data) {
          $('#message-list').data('current-page', newPage);
          if (newPage >= $('#message-list').data('last-page')) {
            $('#load-messages-container').remove();
          }
          return $('#message-list-container').append(data);
        });
      }
      return false;
    }
  };

}).call(this);
