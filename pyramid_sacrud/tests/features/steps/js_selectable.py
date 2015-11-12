import json

from behave import then, when, given


@given(u'list of user entries')
def step_impl(context):
    context.driver.get(context.URL + 'user/')


@when(u'select {id} item')  # noqa
def step_impl(context, id):
    if id == 'all':
        context.driver.find_element_by_id('select_all_item')\
            .find_element_by_xpath("..")\
            .find_element_by_tag_name("label").click()
    elif id.isdigit():
        context.driver.find_element_by_xpath(
            '''.//*[@value='["id", {}]']'''.format(id))\
            .find_element_by_xpath("..")\
            .find_element_by_tag_name("label").click()
    else:
        assert Exception('Bad id value')


@then(u'I should see {action} selected_all_item')  # noqa
def step_impl(context, action):
    is_selected = context.driver\
        .find_element_by_id('select_all_item').is_selected()
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
    context.driver.find_element_by_class_name('delete-button').click()


@when(u'click cancel button')  # noqa
def step_impl(context):
    context.driver.find_element_by_class_name('cancel-button').click()


@then(u'I should see {status} delete button')  # noqa
def step_impl(context, status):
    delete_button = context.driver.find_element_by_class_name('delete-button')
    if status == 'unactive':
        assert 'disabled' in delete_button.get_attribute('class')
    elif status == 'active':
        assert 'disabled' not in delete_button.get_attribute('class')
    else:
        assert Exception('Bad status name')
