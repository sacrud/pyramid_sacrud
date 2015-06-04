from behave import then


@then(u'I should see {status} {name} popup window')  # noqa
def step_impl(context, status, name):
    button = context.driver\
        .find_element_by_class_name('popup_type_message-delete')
    button_display = button.value_of_css_property('display')
    if status == 'active':
        assert button_display != 'none'
    elif status == 'unactive':
        assert button_display == 'none'
    else:
        assert Exception('Bad status name')
