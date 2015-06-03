var rows_state_unselecting, current_rows, first_selected_row, global_options;

var SelectableTable = function (el, options) {
  if (!(this instanceof SelectableTable)) {
    return new SelectableTable(el, options);
  }
  global_options = options;
  this.el = $(el);
  this._bindEvents();
  this._bindSelectable();
  this._afterInit();
};

SelectableTable.prototype.checkCheckbox = function (checkbox) {
  var $parent_tr = $(checkbox).parents('.sacrud-grid-content-grid__body-row');
  if ($(checkbox).prop('checked')) {
    $parent_tr.addClass(global_options.tr_selected_class);
    $parent_tr.addClass('ui-selected');
  } else {
    $parent_tr.removeClass(global_options.tr_selected_class);
    $parent_tr.removeClass('ui-selected');
  }
};

SelectableTable.prototype.changeButtons = function () {
  if ($(global_options.sacrud_form).length) {
    if ($(global_options.table_checkboxes_checked).length) {
      $(global_options.div_delete_button).removeClass(global_options.state_disable_class);
    } else {
      $(global_options.div_delete_button).addClass(global_options.state_disable_class);
    }
  } else {
    $(global_options.div_delete_button).removeClass(global_options.state_disable_class);
  }
};

SelectableTable.prototype._bindEvents = function() {
  $(document).on('change', global_options.table_checkboxes, this.checkboxChange.bind(this));
  $(document).on('change', global_options.all_checkboxes_button , this.allCheckboxChange.bind(this));
};

SelectableTable.prototype.checkboxChange = function (evnt) {
  this.checkCheckbox($(evnt.currentTarget));
  this.changeButtons();
  if ($(global_options.table_checkboxes_not_checked).length) {
    $(global_options.all_checkboxes_button).prop('checked', false);
  } else {
    $(global_options.all_checkboxes_button).prop('checked', true);
  }
};

SelectableTable.prototype.allCheckboxChange = function (evnt) {
  $(global_options.table_checkboxes).prop('checked', $(evnt.currentTarget).prop('checked')).change();
};

SelectableTable.prototype._bindSelectable = function() {
  this.el.selectable({
    filter: 'tr', // :not(td)
    cancel: 'a, input, .selectable_disabled',
    start: this._start,
    selecting: this._selecting,
    selected: this._selected,
    unselected: this._unselected,
    stop: this._stop,
    // unselecting: function (event, ui) {},
  });
};

SelectableTable.prototype._afterInit = function() {
  var checkboxes = $(global_options.table_checkboxes_checked);
  for (var i=0; i < checkboxes.length; i++) {
    this.checkCheckbox(checkboxes[i]);
  }
  this.changeButtons();
};

// jquery-ui.selectable functions
SelectableTable.prototype._start = function(event, ui) {
  current_rows = $(this).data('ui-selectable').selectees.filter('.ui-selected');
};

SelectableTable.prototype._selecting = function (event, ui) {
  var selecting_count = $(this).data('ui-selectable').selectees.filter('.ui-selecting').length;
  if (!(rows_state_unselecting)) {
    rows_state_unselecting = $(this).data('ui-selectable').selectees.filter('.ui-unselecting');
  }
  if (selecting_count == 1) {
    rows_state_unselecting.switchClass('ui-unselecting', 'ui-selecting');
    if (current_rows.is(ui.selecting)) {
      first_selected_row = $(ui.selecting);
      $(ui.selecting).switchClass('ui-selecting', 'ui-unselecting');
    }
  } else {
    rows_state_unselecting = rows_state_unselecting.not(ui.selecting);
    rows_state_unselecting.switchClass('ui-selecting', 'ui-unselecting');
    if (first_selected_row) {
      rows_state_unselecting.switchClass('ui-unselecting', 'ui-selecting');
      first_selected_row = null;
    }
  }
};

SelectableTable.prototype._selected = function (event, ui) {
  $(ui.selected).addClass(global_options.tr_selected_class);
  $(ui.selected).find(global_options.table_checkboxes).prop('checked', true).change();
};

SelectableTable.prototype._unselected = function (event, ui) {
  $(ui.unselected).removeClass(global_options.tr_selected_class);
  $(ui.unselected).find(global_options.table_checkboxes).prop('checked', false).change();
};

SelectableTable.prototype._stop = function (event, ui) {
  rows_state_unselecting = null;
  first_selected_row = null;
};


// Main entry point
module.exports = function selectable_table(el, options) {
  return new SelectableTable(el, options);
};

module.exports.SelectableTable = SelectableTable;
