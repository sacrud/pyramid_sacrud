require('jquery');
require('jquery-ui');
require('jqueryui-timepicker-addon');
require('jquery-maskedinput');
require('modernizr');
require('pickadate');
$(function() {
    var options = {
            // Popup
            'popup_close_button': 'a.popup-inner__content-link-text',
            'popup_main_button': 'div.popup-button__item',
            'div_delete_button': 'div.toolbar-button__item_type_delete',
            'sacrud_form': 'form#sacrud-form',
            // Selectable (jquery-ui)
            'tr_selected_class': 'sacrud-grid-content-grid__body-row_state_active',
            'state_disable_class': 'toolbar-button__item_state_disable',
            'input_selected_action': 'input[name="selected_action"]',
            'all_checkboxes_button': 'input#selected_all_item',
            'table_checkboxes': 'input[name="selected_item"]',
            'table_checkboxes_checked': 'input[name="selected_item"]:checked',
            'table_checkboxes_not_checked': 'input[name="selected_item"]:not(:checked)',
        };
    var popup = require('./app/common/popup.js').Popup('div.popup', options);
    var checkbox = require('./app/common/checkbox.js');
    var selectable = require('./app/common/selectable.js');

    selectable(options);
    // popup(options);
});
