// var $ = require('jquery'),
    // jquery_ui = require('jquery-ui');

module.exports = function(options) {
    $(function() {
        var rows_state_unselecting,
            current_rows,
            first_selected_row;

        $('table > tbody').selectable({
            filter: 'tr', // :not(td)
            cancel: 'a, input, .selectable_disabled',
            start: function (event, ui) {
              current_rows = $(this).data('ui-selectable').selectees.filter('.ui-selected');
            },
            // unselecting: function (event, ui) {},
            selecting: function (event, ui) {
                var selecting_count = $(this).data('ui-selectable').selectees.filter('.ui-selecting').length;
                if (!(rows_state_unselecting)) {
                    rows_state_unselecting = $(this).data('ui-selectable').selectees.filter('.ui-unselecting');
                }
                if (selecting_count == 1) {
                    rows_state_unselecting.removeClass('ui-unselecting');
                    rows_state_unselecting.addClass('ui-selecting');
                    if (current_rows.is(ui.selecting)) {
                        first_selected_row = $(ui.selecting);
                        $(ui.selecting).removeClass('ui-selecting');
                        $(ui.selecting).addClass('ui-unselecting');
                    }
                } else {
                    rows_state_unselecting = rows_state_unselecting.not(ui.selecting);
                    rows_state_unselecting.removeClass('ui-selecting');
                    rows_state_unselecting.addClass('ui-unselecting');
                    if (first_selected_row) {
                        first_selected_row.removeClass('ui-unselecting');
                        first_selected_row.addClass('ui-selecting');
                        first_selected_row = null;
                    }
                }
            },
            selected: function (event, ui) {
                $(ui.selected).addClass(options.tr_selected_class);
                $(ui.selected).find(options.table_checkboxes).prop('checked', true).change();
                // console.log(ui.selected);
                // console.log($(this).data('uiSelectable').selectees.filter('.ui-selected'));
            },
            unselected: function (event, ui) {
                $(ui.unselected).removeClass(options.tr_selected_class);
                $(ui.unselected).find(options.table_checkboxes).prop('checked', false).change();
            },
            stop: function (event, ui) {
                rows_state_unselecting = null;
                first_selected_row = null;
            },
        });

        function change_buttons () {
            if (!($(options.table_checkboxes).length) || $(options.table_checkboxes_checked).length) {
                $(options.div_delete_button).removeClass(options.state_disable_class);
            } else {
                $(options.div_delete_button).addClass(options.state_disable_class);
            }
        }

        function check_checkbox (checkbox) {
            var $parent_tr = checkbox.parents('.sacrud-grid-content-grid__body-row');
            if (checkbox.prop('checked')) {
                $parent_tr.addClass(options.tr_selected_class);
                $parent_tr.addClass('ui-selected');
            } else {
                $parent_tr.removeClass(options.tr_selected_class);
                $parent_tr.removeClass('ui-selected');
            }
        }

        $(options.table_checkboxes_checked).each(function (){
            check_checkbox($(this));
        });

        change_buttons();

        $(document).on('change', options.table_checkboxes , function () {
            check_checkbox($(this));
            change_buttons();
            // if (!($('input:checkbox:not(:checked)'))) {
            if ($(options.table_checkboxes_not_checked).length) {
                $(options.all_checkboxes_button).prop('checked', false);
            } else {
                $(options.all_checkboxes_button).prop('checked', true);
            }
        });

        $(document).on('click', '.'+options.state_disable_class , function (event) {
            event.stopImmediatePropagation();
        });

        $(document).on('change', options.all_checkboxes_button , function () {
            $(options.table_checkboxes).prop('checked', $(this).prop('checked')).change();
        });
    });
};
