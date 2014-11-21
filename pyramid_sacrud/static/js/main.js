require('jquery');
require('jquery-ui');
require('jqueryui-timepicker-addon');
require('jquery-maskedinput');
require('modernizr');
require('pickadate');
$(function() {
    var options = require('./app/options.js');
    var popup = require('./app/common/popup.js').Popup('div.popup', options);
    var checkbox = require('./app/common/checkbox.js');
    var selectable = require('./app/common/selectable.js');

    selectable(options);
    // popup(options);
});
