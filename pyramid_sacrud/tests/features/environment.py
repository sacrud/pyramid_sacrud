import imp

from selenium import webdriver
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

imp.load_source('pyramid_sacrud_example', 'example/pyramid_sacrud_example.py')
from pyramid_sacrud_example import User


def before_all(context):
    context.URL = 'http://127.0.0.1:6543/admin/'
    browser = context.config.userdata.get("browser", "firefox").lower()
    if browser == "firefox":
        context.driver = webdriver.Firefox()
    elif browser == "chrome":
        context.driver = webdriver.Chrome(
            executable_path='/usr/lib/chromium-browser/chromedriver'
        )

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
