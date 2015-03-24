var webdriver = require('selenium-webdriver');
var driver = new webdriver.Builder()
    .withCapabilities(webdriver.Capabilities.phantomjs())
    .build();

var chai = require('chai');
var expect = require('chai').expect;

var cheerio = require("cheerio");

var URL = 'http://127.0.0.1:6543/',
    LOGIN = 'admin',
    PASSWORD = '123';

describe('SACRUD Dashboard link check', function() {

    before(function(done) {
        driver.get(URL+'login/').then(function(){ done(); });
    });

    it('Login', function(done){
        var username = driver.findElement(webdriver.By.name('login'));
        var password = driver.findElement(webdriver.By.name('password'));
        username.sendKeys(LOGIN);
        password.sendKeys(PASSWORD);
        password.submit().then(function(){ done(); });
    });

    it('Check links', function(done){
        driver.get(URL+'admin/').then(function(){ done(); });
        driver.getPageSource().then(function(page_html) {
            var $ = cheerio.load(page_html);
            links = $(".dashboard a");
            $(links).each(function(){
                var link = $(this).attr('href');
                driver.get(link);
                driver.manage().logs().get('har').then(function(msg) {
                    expect(msg).to.not.contain('Error downloading', 'Page '+link+' contain Error 404');
                });
            });
        });
    });

    it('Logout', function(done){
        var logout = driver.findElement(webdriver.By.name('logoutLink'));
        logout.click().then(function(){ done(); });
    });

    after(function(done) {
        driver.quit().then(function(){ done();});
    });

});