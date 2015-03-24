var webdriver = require('selenium-webdriver');
var driver = new webdriver.Builder()
    .withCapabilities(webdriver.Capabilities.phantomjs())
    .build();

var URL = 'http://127.0.0.1:6543/',
    LOGIN = 'admin',
    PASSWORD = '123';

describe('SACRUD Login/Logout', function() {

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

    it('Go to dashboard', function(done){
        driver.get(URL+'admin/').then(function(){ done(); });
    });

    it('Logout', function(done){
        var logout = driver.findElement(webdriver.By.name('logoutLink'));
        logout.click().then(function(){ done(); });
    });

    after(function(done) {
        driver.quit().then(function(){ done();});
    });

});