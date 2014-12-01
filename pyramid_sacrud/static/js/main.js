require('jquery');
require('jquery-ui');
require('jqueryui-timepicker-addon');
require('jquery-maskedinput');
require('modernizr');
require('pickadate');
require('pickatime');

$(function() {
    var options = require('./app/options.js');
    var popup = require('./app/common/popup.js').Popup(options.popup, options);
    var selectable = require('./app/common/selectable.js').SelectableTable('table > tbody', options);
    // var checkbox = require('./app/common/checkbox.js');
});
