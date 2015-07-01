'use strict';

var Popup = function (options) {
  if (!(this instanceof Popup)) {
    return new Popup(options);
  }
  this.el = $(options.popup);
  this.options = options;
  this._bindEvents();
};

Popup.prototype._bindEvents = function() {
  $(document).on('click', 'div.'+this.options.state_disable_class, this.blockDisabledButton.bind(this));
  $(document).on('click', this.options.div_delete_button, this.showDeletePopup.bind(this));
  $(document).on('click', this.options.popup_close_button, this.hidePopup.bind(this));
  $(document).on('click', this.options.popup_main_button, this.checkButton.bind(this));
};

Popup.prototype.blockDisabledButton = function (event) {
  event.stopImmediatePropagation();
};

Popup.prototype.showDeletePopup = function (event) {
  this.el.css("display", "table");
  $('.popup-inner__content-delete').show();
};

Popup.prototype.hidePopup = function (event) {
  this.el.hide();
  $('.popup-inner__content-delete').hide();
  if ($(event.currentTarget).attr('href') !== undefined) {
    event.preventDefault();
  }
};

Popup.prototype.checkButton = function (event) {
  var status = $(event.currentTarget).data('status');
  var form = $(this.options.sacrud_form)
  if ((status === undefined) || (status == 'cancel')) {
    this.hidePopup(event);
  } else if (form.length) {
    this._formSubmit(form, status);
  }
};

// Used in list template
Popup.prototype._formSubmit = function (form, status) {
  // for delete object, need to send status 'delete'
  $(this.options.input_selected_action).val(status);
  form.submit();
};

// Main entry point
module.exports.Popup = Popup;
