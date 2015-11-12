from behave import then


@then(u'I should see {status} {name} popup window')  # noqa
def step_impl(context, status, name):
    popup = context.driver.find_element_by_id('modal1')
    popup_display = popup.value_of_css_property('display')
    if status == 'active':
        assert popup_display != 'none'
    elif status == 'unactive':
        assert popup_display == 'none'
    else:
        assert Exception('Bad status name')
