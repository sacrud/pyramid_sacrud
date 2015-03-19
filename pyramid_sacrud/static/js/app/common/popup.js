var Popup = function (el, options) {
    if (!(this instanceof Popup)) {
        return new Popup(el, options);
    }
    this.el = $(el);
    this.options = options;
    this._bindEvents();
};

Popup.prototype._bindEvents = function() {
    $(document).on('click', 'div.'+this.options.state_disable_class, this.blockDisabledButton.bind(this));
    $(document).on('click', this.options.div_delete_button, this.showDeletePopup.bind(this));
    $(document).on('click', this.options.popup_close_button, this.hidePopup.bind(this));
    $(document).on('click', this.options.popup_main_button, this.checkButton.bind(this));
};

// $(document).on('click', 'div.popup', function function_name (argument) {
//     console.log('yippee-ki-yay motherf*cker');
// });

Popup.prototype.blockDisabledButton = function (evnt) {
    evnt.stopImmediatePropagation();
};

Popup.prototype.showDeletePopup = function (evnt) {
    this.el.css("display", "table");
    $('.popup-inner__content-delete').show();
    $('.popup-inner__content-elfinder').hide();
    // this.showDeletePopupContent();
};

Popup.prototype.hidePopup = function (evnt) {
    this.el.hide();
    $('.popup-inner__content-delete').hide();
    $('.popup-inner__content-elfinder').hide();
    if ($(evnt.currentTarget).attr('href') !== undefined) {
        evnt.preventDefault();
    }
    // this.hidePopupContent();
};

// Popup.prototype.showDeletePopupContent = function (evnt) {};
// Popup.prototype.hidePopupContent = function (evnt) {};

Popup.prototype.checkButton = function (evnt) {
    var status = $(evnt.currentTarget).data('status');
    if ((status === undefined) || (status == 'cancel')) {
        this.hidePopup(evnt);
    } else if ($(this.options.sacrud_form).length) {  // if (typeof options != "undefined")
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
module.exports = function popup(el, options) {
    return new Popup(el, options);
};

module.exports.Popup = Popup;
