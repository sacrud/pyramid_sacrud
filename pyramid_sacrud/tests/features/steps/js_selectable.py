import json

from behave import given, then, when


@given(u'list of user entries')
def step_impl(context):
    context.driver.get(context.URL + 'user/')


@when(u'f5')  # noqa
def step_impl(context):
    context.driver.refresh()


@when(u'select {id} item')  # noqa
def step_impl(context, id):
    if id == 'all':
        context.driver.find_element_by_id('selected_all_item').click()
    elif id.isdigit():
        context.driver.find_element_by_xpath(
            '''.//*[@value='["id", {}]']'''.format(id)).click()
    else:
        assert Exception('Bad id value')


@then(u'I should see {action} selected_all_item')  # noqa
def step_impl(context, action):
    is_selected = context.driver\
        .find_element_by_id('selected_all_item').is_selected()
    if action == 'selected':
        assert is_selected is True
    elif action == 'unselected':
        assert is_selected is False
    else:
        assert Exception('Bad action value')


@then(u'I should see checkbox is {action}')  # noqa
def step_impl(context, action):
    default_action = action
    checkbox_list = context.driver.find_elements_by_name('selected_item')
    for checkbox in checkbox_list:
        for row in context.table or ():
            user_id = int(json.loads(checkbox.get_attribute('value'))[1])
            if int(row['id']) == user_id:
                action = row['value']
                break
            else:
                action = default_action
        if action == 'selected':
            assert checkbox.is_selected() is True
        elif action == 'unselected':
            assert checkbox.is_selected() is False
        else:
            assert Exception('Bad action value')


@when(u'click delete button')  # noqa
def step_impl(context):
    context.driver.find_element_by_class_name(
        'toolbar-button__item-name').click()


@then(u'I should see {status} delete button')  # noqa
def step_impl(context, status):
    delete_button = context.driver\
        .find_element_by_class_name('toolbar-button__item-name')
    parent = delete_button.find_element_by_xpath('..')
    unactive_css_class = 'toolbar-button__item_state_disable'
    if status is 'unactive':
        assert unactive_css_class in parent.get_attribute('class')
    elif status is 'active':
        assert unactive_css_class not in parent.get_attribute('class')
    else:
        assert Exception('Bad status name')
