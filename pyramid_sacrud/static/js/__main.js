(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
var modulePath = '../pyramid_sacrud/gulp/_node_modules/';

var $ = require(modulePath + 'jquery');

var list = require('./app/list.js'),
    popup = require('./app/common/popup.js'),
    checkbox = require('./app/common/checkbox.js'),
    selectable = require('./app/common/selectable.js');

},{"./app/common/checkbox.js":2,"./app/common/popup.js":3,"./app/common/selectable.js":4,"./app/list.js":5}],2:[function(require,module,exports){
module.exports = function(vars) {

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
};
},{}],3:[function(require,module,exports){
module.exports = function(vars) {

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
};
},{}],4:[function(require,module,exports){
module.exports = function(vars) {

    $(function() {

        var rows_state_unselecting,
            current_rows,
            first_selected_row;

        options = {
            'tr_selected_class': 'sacrud-grid-content-grid__body-row_state_active',
            'state_disable_class': 'toolbar-button__item_state_disable',
            'all_checkboxes_button': '#selected_all_item',
            'table_checkboxes': 'input[name="selected_item"]',
            'table_checkboxes_checked': 'input[name="selected_item"]:checked',
            'table_checkboxes_not_checked': 'input[name="selected_item"]:not(:checked)',
            'input_selected_action': 'input[name="selected_action"]',
            'div_action_button': '.action_button',
        };

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
            if ($(options.table_checkboxes_checked).length) {
                $(options.div_action_button).removeClass(options.state_disable_class);
            } else {
                $(options.div_action_button).addClass(options.state_disable_class);
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
},{}],5:[function(require,module,exports){
module.exports = function(vars) {

    $(function() {
        $(document).on('focus', '#site_search', function () {
            // console.log($(this));
            // $(this).val('');
        });
    });

};
},{}]},{},[1]);
