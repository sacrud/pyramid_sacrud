var webdriver = require('selenium-webdriver');

var SELENIUM_HOST = 'http://127.0.0.1:4444/wd/hub',
    URL = 'http://127.0.0.1:8000/login/';

var driver = new webdriver.Builder()
    //.usingServer(SELENIUM_HOST)
    .withCapabilities({ 'browserName': 'phantomjs' })
    .build();

var chai = require('chai'),
    assert = chai.assert,
    expect = chai.expect;

describe('SACRUD Tests', function() {
    before(function(done) {
        driver.get(URL).then(function(){ done(); });
    });

    it('Login to SACRUD', function() {
        var username = driver.findElement(webdriver.By.name('login'));
        username.sendKeys('admin');
        username.getAttribute('value').then(function(value) {
            assert.equal(value, 'admin');
        });
        var password = driver.findElement(webdriver.By.name('password'));
        password.sendKeys('123');
        password.getAttribute('value').then(function(value) {
            assert.equal(value, '123');
        });
        var loginButton = driver.findElement(webdriver.By.name('submit'));
            loginButton.click();
    });

    it('Go to SACRUD!', function(){
        var goButton = driver.findElement(webdriver.By.name('goToSACRUD'));
            goButton.click();
    });

    it('Logout to SACRUD', function(){
        var logout = driver.findElement(webdriver.By.name('logoutLink'));
            logout.click();
    });

    after(function(done) {
        driver.quit().then(function(){ done();});
    });
});