define(['jquery'], function ($) {
  $(function() {
      function check_checkbox (checkbox) {
          if (checkbox.prop('checked')) {
              checkbox.parents('label.checkbox').addClass('checkbox_state_cheked');
          } else {
              checkbox.parents('label.checkbox').removeClass('checkbox_state_cheked');
          }
      }

      $(document).on('change', '.checkbox__checkbox', function () {
          check_checkbox($(this));
      });

      $('input[type="checkbox"]:checked').each(function(){
          check_checkbox($(this));
      });
  });
});
