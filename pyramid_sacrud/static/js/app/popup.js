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

Popup.prototype.blockDisabledButton = function (evnt) {
  evnt.stopImmediatePropagation();
};

Popup.prototype.showDeletePopup = function (evnt) {
  this.el.css("display", "table");
  $('.popup-inner__content-delete').show();
  $('.popup-inner__content-elfinder').hide();
};

Popup.prototype.hidePopup = function (evnt) {
  this.el.hide();
  $('.popup-inner__content-delete').hide();
  $('.popup-inner__content-elfinder').hide();
  if ($(evnt.currentTarget).attr('href') !== undefined) {
    evnt.preventDefault();
  }
};

Popup.prototype.checkButton = function (evnt) {
  var status = $(evnt.currentTarget).data('status');
  if ((status === undefined) || (status == 'cancel')) {
    this.hidePopup(evnt);
  } else if ($(this.options.sacrud_form).length) {
    this._formSubmit($(this.options.sacrud_form), status);
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
