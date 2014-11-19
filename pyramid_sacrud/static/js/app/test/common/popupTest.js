var assert = require("assert");

var Popup = require('../../common/popup').Popup;

describe('Popup', function(){
  // before(function(){
  // });

  describe('create Popup', function(){
    it('should return -1 when not present', function(){
      var l = new Popup('div.popup', {});
      assert(l);
    });
  });

  // describe('showDeletePopup', function(){

  // });
});