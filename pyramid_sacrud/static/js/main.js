require('jquery');
require('jquery-ui');
require('jqueryui-timepicker-addon');
require('jquery-maskedinput');
require('modernizr');

var list = require('./app/list.js'),
    popup = require('./app/common/popup.js'),
    checkbox = require('./app/common/checkbox.js'),
    selectable = require('./app/common/selectable.js');
    // datetimepicker = require.resolve('jqueryui-timepicker-browser');

popup();
checkbox();
selectable();
