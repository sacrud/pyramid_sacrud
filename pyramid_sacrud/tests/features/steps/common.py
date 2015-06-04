import time

from behave import when
from selenium.webdriver.common.keys import Keys


@when('sleep {seconds}')
def step_impl(context, seconds):
    time.sleep(int(seconds))


@when(u'f5')  # noqa
def step_impl(context):
    # context.driver.refresh()
    context.driver.find_element_by_tag_name('body').send_keys(Keys.F5)
    time.sleep(2)
