import imp

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

imp.load_source('pyramid_sacrud_example', 'example/pyramid_sacrud_example.py')
from pyramid_sacrud_example import User


user_agent = (
    "Mozilla/28.0 (Macintosh; Intel Mac OS X 10_8_4) " +
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
)

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = user_agent


def before_all(context):
    context.URL = 'http://127.0.0.1:6543/admin/'
    context.driver = webdriver.Firefox()

    # SQLAlchemy connection
    context.engine = create_engine('sqlite:///example/example.sqlite')
    context.models = {'user': User}


def before_scenario(context, scenario):
    DBSession = scoped_session(sessionmaker())
    DBSession.configure(bind=context.engine)
    context.dbsession = DBSession


def after_scenario(context, scenario):
    context.dbsession.close()


def after_all(context):
    context.driver.quit()
