'use strict';

require('picker');
require('pickadate');
require('pickatime');

$(function() {
    var options = require('./app/options.js');
    var popup = require('./app/common/popup.js').Popup(options.popup, options);
    var selectable = require('./app/common/selectable.js').SelectableTable('table > tbody', options);
});
