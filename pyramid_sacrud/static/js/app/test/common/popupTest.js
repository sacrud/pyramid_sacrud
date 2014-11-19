var assert = require("assert");

describe('Array', function(){
  describe('#indexOf()', function(){
    it('should return -1 when the value is not present', function(){
      assert.equal(-1, [1,2,3].indexOf(5));
      assert.equal(-1, [1,2,3].indexOf(0));
    });
  });
});


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
