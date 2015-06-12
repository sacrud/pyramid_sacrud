from behave import then


@then('I should see xpath')
def step_impl(context):
    xpath = context.text
    if not context.driver.find_element_by_xpath(xpath):
        raise Exception("Xpath not found")
