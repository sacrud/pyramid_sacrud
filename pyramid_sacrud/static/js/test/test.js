var SELENIUM_HOST = 'http://127.0.0.1:4444/wd/hub',
    LOGIN_URL = 'http://127.0.0.1:8000/login/',
    POPUP_TEST_URL = 'http://127.0.0.1:8000/admin/test_bool/';

var webdriver = require('selenium-webdriver');
var driver = new webdriver.Builder()
    //.usingServer(SELENIUM_HOST)
    .withCapabilities({ 'browserName': 'phantomjs', 'webStorageEnabled': true})
    .build();

var chai = require('chai'),
    assert = chai.assert,
    expect = chai.expect;

var options = require('../app/options.js');
var jsdom = require("jsdom").jsdom;


// webdriver.promise.controlFlow().on('uncaughtException', function(e) {
//     console.log('Произошла ошибка: ', e);
// });


describe('SACRUD Tests', function() {

    before(function(done) {
        // Get admin page for tests
        driver.get(LOGIN_URL);
        var username = driver.findElement(webdriver.By.name('login'));
        username.sendKeys('admin');
        var password = driver.findElement(webdriver.By.name('password'));
        password.sendKeys('123');
        password.submit();
        driver.get(POPUP_TEST_URL).then(function(){ done(); });
    });

    describe('Popup', function() {

        var elements = {};

        it('Should find elements for popup in DOM', function(done) {
            function check_element_existence (name, css_arg, done) {
                driver.isElementPresent(webdriver.By.css(css_arg)).then(function(exists) {
                    assert.isTrue(exists, 'Element "'+css_arg+'" is not found');
                    elements[name] = driver.findElement(webdriver.By.css(css_arg));
                    if (done !== undefined) { done(); }
                });
            }
            check_element_existence('div_popup', 'div.popup');
            check_element_existence('div_delete_button', options.div_delete_button);
            check_element_existence('popup_close_button', options.popup_close_button);
            check_element_existence('popup_main_button', options.popup_main_button, done);
            // on list and may be undefined:
            // sacrud_form
            // input_selected_action
        });

        it('Should correctly handle found elements', function(done) {
            driver.getPageSource().then(function(page_html) {
                var dom_window = jsdom(page_html).parentWindow;
                document = dom_window.document;
                $ = require('../bower_components/jquery/dist/jquery.js')(dom_window);

                var Popup = require("../app/common/popup.js").Popup,
                    popup_obj = new Popup('div.popup', options);

                elements['div_delete_button'].getAttribute('class').then(function(class_value) {
                    expect(class_value).to.contain(options.state_disable_class, 'The "Delete" button should be disabled if nothing is selected');
                    done();
                });

                // webdriver.until.elementIsVisible(div_popup).fn().then(function(val) {
                //     driver.executeScript('arguments[0].style.display="block";', div_popup);
                // });

                // console.log('--- jquery popup ---');
                // $('div.popup').click();
                // console.log($('div.popup').length);
                // console.log($('div.popup').hasClass('popup'));
                // $('.sacrud-grid-content-grid__body-item-checkbox').attr('checked', true);
                // console.log($('.sacrud-grid-content-grid__body-item-checkbox').attr('checked'));
            });
        });

        // it('Go to SACRUD!', function(){
            // var goButton = driver.findElement(webdriver.By.name('goToSACRUD'));
            //     goButton.click();
        // });

        // it('Logout to SACRUD', function(){
        //     var logout = driver.findElement(webdriver.By.name('logoutLink'));
        //         logout.click();
        // });


        after(function(done) {
            driver.quit().then(function(){ done();});
        });
    });
});

