define(['jquery'], function ($) {
  $(function() {
      function show_delete_content() {
          $('.popup-inner__content-delete').show();
          $('.popup-inner__content-elfinder').hide();
      }

      $(document).on('click', '.action_button', function () {
          $('.popup').show();
          show_delete_content();
      });

      $(document).on('click', '.popup-inner__content-link-text', function (event) {
          $('.popup').hide();
          show_delete_content();
          event.preventDefault();
      });

      $(document).on('click', '.popup-button__item', function () {
          var status = $(this).data('status');
          if (status == 'cancel') {
              $('.popup').hide();
          } else if (typeof options != "undefined") {
              $(options.input_selected_action).val(status);
              $('#sacrud-form').submit();
          }
      });

      // $(document).on('click', function (e) {
      //     if (!($(e.target).closest('.popup-inner').length) && $('.popup').is(':visible')) {
      //         $('.popup').hide();
      //     }
      // });
  });
});
