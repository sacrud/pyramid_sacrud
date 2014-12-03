var webdriver = require('selenium-webdriver');
var driver = new webdriver.Builder().withCapabilities({'browserName': 'phantomjs'}).build();

var chai = require('chai'),
    expect = chai.expect;

var options = require('../app/options.js');
var elements = {};


describe('SACRUD tests', function() {

    function check_element_existence (name, css_arg, err_msg, done) {
        if (err_msg === undefined) {
            err_msg = 'Element "'+css_arg+'" is not found';
        }
        driver.isElementPresent(webdriver.By.css(css_arg)).then(function(exists) {
            expect(exists, err_msg).to.be.true();
            elements[name] = driver.findElement(webdriver.By.css(css_arg));
            if (done !== undefined) { done(); }
        });
    }

    before(function(done) {
        driver.get('http://127.0.0.1:8000/login/').then(function(){ done(); });
    });

    describe('Login', function() {
        it('Should login to SACRUD', function(done){
            var username = driver.findElement(webdriver.By.name('login'));
            var password = driver.findElement(webdriver.By.name('password'));
            username.sendKeys('admin');
            password.sendKeys('123');
            password.submit().then(function(){ done(); });
        });
    });

    // it('Should correctly handle found elements', function(done) {
    //     var SelectableTable = require("../app/common/selectable.js").SelectableTable;
    //     SelectableTable.prototype._bindSelectable = function() {};
    // });

    describe('Popup', function() {

        // var jsdom = require("jsdom").jsdom;

        before(function(done) {
            driver.get('http://127.0.0.1:8000/admin/test_bool/').then(function(){ done(); });  //test_bool  test_all_types
            // driver.getPageSource().then(function(page_html) {
            //     // var dom_window = jsdom(page_html).parentWindow;
            //     // document = dom_window.document;
            //     // $ = require('../bower_components/jquery/dist/jquery.js')(dom_window);
            //     done();
            // });
        });

        it('Should find elements for popup in DOM', function(done) {
            check_element_existence('div_popup', options.popup);
            check_element_existence('div_delete_button', options.div_delete_button);
            check_element_existence('popup_close_button', options.popup_close_button);
            check_element_existence('popup_delete_button', options.popup_main_button+'[data-status="delete"]');
            check_element_existence('popup_cancel_button', options.popup_main_button+'[data-status="cancel"]', undefined, done);
        });

        it('Popup should be invisible, after opening page', function(done) {
            webdriver.until.elementIsVisible(elements['div_popup']).fn().then(function(visible) {
                expect(visible, options.popup + ' must be invisible').to.be.false();
                done();
            });
        });


        describe('Grid', function() {
            it('"Delete" button state should be disabled by default', function(done) {
                elements['div_delete_button'].getAttribute('class').then(function(class_value) {
                    expect(class_value).to.contain(options.state_disable_class, '"Delete" button must contain class "'+options.state_disable_class+'" if nothing is selected');
                    done();
                });
            });

            it('"Delete" button state should be active(change class), after check item', function(done) {
                check_element_existence('table_checkbox', options.table_checkboxes, 'Not found objects in grid. Change url for test or create objects.', function() {
                    elements['table_checkbox'].click();
                    elements['table_checkbox'].getAttribute('checked').then(function(checked) {
                        expect(checked, options.table_checkboxes + ' must be checked after click').to.equal('true');
                    });
                });
                elements['div_delete_button'].getAttribute('class').then(function(class_value) {
                    expect(class_value).to.not.contain(options.state_disable_class, 'The "Delete" button should be active, after selecting item');
                    done();
                });
            });

            it('Popup should be visible, after clicking on active "Delete" button', function(done) {
                elements['div_delete_button'].click();
                webdriver.until.elementIsVisible(elements['div_popup']).fn().then(function(visible) {
                    expect(visible, options.popup + ' must be visible').to.be.true();
                    done();
                });
            });

            it('Popup should be invisible, after clicking on "Cancel" button', function(done) {
                elements['popup_cancel_button'].click();
                webdriver.until.elementIsVisible(elements['div_popup']).fn().then(function(visible) {
                    expect(visible, options.popup + ' must be invisible').to.be.false();
                    done();
                });
            });

            it('Popup should be invisible, after clicking on "close" link', function(done) {
                driver.executeScript('arguments[0].style.display="block";', elements['div_popup']);
                // not work in phantomjs
                // elements['popup_close_button'].click(); // driver.executeScript("arguments[0].click();", elements['popup_close_button']);
                driver.executeScript('$("'+options.popup_close_button+'").click();');
                webdriver.until.elementIsVisible(elements['div_popup']).fn().then(function(visible) {
                    expect(visible, options.popup + ' must be invisible').to.be.false();
                    done();
                });
            });

            it('"Delete" button state should be disabled(change class), after uncheck item', function(done) {
                elements['table_checkbox'].click();
                elements['table_checkbox'].getAttribute('checked').then(function(checked) {
                    expect(checked).to.be.null();
                });
                elements['div_delete_button'].getAttribute('class').then(function(class_value) {
                    expect(class_value).to.contain(options.state_disable_class, 'The "Delete" button should be active, after selecting item');
                    done();
                });
            });

            it('Popup should be invisible, after clicking on disabled "Delete" button', function(done) {
                elements['div_delete_button'].click();
                webdriver.until.elementIsVisible(elements['div_popup']).fn().then(function(visible) {
                    expect(visible, options.popup + ' must be visible').to.be.false();
                    done();
                });
            });


            // it('Should correctly handle found elements', function(done) {
            //     var Popup = require("../app/common/popup.js").Popup,
            //         popup_obj = new Popup(options.popup, options);
            //     var SelectableTable = require("../app/common/selectable.js").SelectableTable;
            //     SelectableTable.prototype._bindSelectable = function() {};
            //     var selectable_table_obj = new SelectableTable('table > tbody', options);
            //     driver.findElements(webdriver.By.css(options.table_checkboxes)).then(function(element_list) {
            //         console.log('-----');
            //         console.log(element_list.length);
            //         expect(element_list).to.not.have.length(0);
            //         console.log(element_list[0]);
            //         element_list[0].getAttribute('class').then(function(class_value) {
            //             console.log('.......');
            //             console.log(class_value);
            //             done();
            //         });
            //     });
            //     webdriver.until.elementIsVisible(div_popup).fn().then(function(val) {
            //         driver.executeScript('arguments[0].style.display="block";', div_popup);
            //     });
            //     console.log('--- jquery popup ---');
            //     $(options.popup).click();
            //     console.log($(options.popup).length);
            //     console.log($(options.popup).hasClass('popup'));
            //     $('.sacrud-grid-content-grid__body-item-checkbox').attr('checked', true);
            //     console.log($('.sacrud-grid-content-grid__body-item-checkbox').attr('checked'));
            // });
            // it('Go to SACRUD!', function(){
                // var goButton = driver.findElement(webdriver.By.name('goToSACRUD'));
                //     goButton.click();
            // });
        });
    });

    describe('Selectable', function() {

        it('Should find elements for selectable in DOM', function(done) {
            elements = {};
            check_element_existence('sacrud_form', options.sacrud_form);
            check_element_existence('all_checkboxes_button', options.all_checkboxes_button);

            driver.isElementPresent(webdriver.By.tagName('tbody')).then(function(exists) {
                expect(exists, 'Not found table body on page').to.be.true();
                driver.findElement(webdriver.By.tagName('tbody')).findElements(webdriver.By.tagName('tr')).then(function(element_list) {
                    expect(element_list, 'Not found rows in table').to.not.have.length(0);
                    elements['rows_list'] = element_list;
                    done();
                });
            });
        });

        it('Table row should change class, after clicking', function(done) {
            elements['rows_list'][0].click();
            elements['rows_list'][0].getAttribute('class').then(function(class_value) {
                expect(class_value).to.contain(options.tr_selected_class, 'Table row must contain class "'+options.tr_selected_class+'" after first clicking');
                done();
            });
        });

        it('All table rows should change class, after clicking header checkbox', function(done) {
            elements['all_checkboxes_button'].click();
            driver.findElements(webdriver.By.className(options.tr_selected_class)).then(function(element_list) {
                expect(element_list.length, 'Select not all checkboxes').to.equal(elements['rows_list'].length);
                done();
            });
        });

    });

    describe('Logout', function() {
        it('Should logout from SACRUD', function(done){
            var logout = driver.findElement(webdriver.By.name('logoutLink'));
            logout.click().then(function(){ done(); });
        });
    });

    after(function(done) {
        driver.quit().then(function(){ done();});
    });

});

