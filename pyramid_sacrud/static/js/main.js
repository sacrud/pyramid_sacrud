require('jquery');
require('jquery-ui');
require('jqueryui-timepicker-addon');
require('jquery-maskedinput');
require('modernizr');

var list = require('./app/list.js'),
    popup = require('./app/common/popup.js'),
    checkbox = require('./app/common/checkbox.js'),
    selectable = require('./app/common/selectable.js'),
    options = {
        'tr_selected_class': 'sacrud-grid-content-grid__body-row_state_active',
        'state_disable_class': 'toolbar-button__item_state_disable',
        'all_checkboxes_button': '#selected_all_item',
        'table_checkboxes': 'input[name="selected_item"]',
        'table_checkboxes_checked': 'input[name="selected_item"]:checked',
        'table_checkboxes_not_checked': 'input[name="selected_item"]:not(:checked)',
        'input_selected_action': 'input[name="selected_action"]',
        'div_delete_button': '.toolbar-button__item_type_delete',
    };

selectable(options);
popup(options);
// checkbox();  // use only with custom checkboxes
