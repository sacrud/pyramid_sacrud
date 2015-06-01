var assert = require('chai').assert;

describe('Popup tests', function(){
  it('Should find elements for popup in DOM', function(done) {
    check_element_existence('div_popup', options.popup);
    check_element_existence('div_delete_button', options.div_delete_button);
    check_element_existence('popup_close_button', options.popup_close_button);
    check_element_existence('popup_delete_button', options.popup_main_button+'[data-status="delete"]');
    check_element_existence('popup_cancel_button', options.popup_main_button+'[data-status="cancel"]', undefined, done);
  });
});
