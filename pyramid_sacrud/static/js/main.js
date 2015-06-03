'use strict';

require('./vendor/jquery.ui.core.min');
require('./vendor/jquery.ui.widget.min');
require('./vendor/jquery.ui.mouse.min');
require('./vendor/jquery.ui.selectable.min');
require('./vendor/jquery.ui.effect.min');

var options = require('./app/options.js');
var popup = require('./app/popup.js').Popup(options);
var selectable = require('./app/selectable.js').SelectableTable('table > tbody', options);
