import time
from behave import given, when, then


@given(u'update {id} {table} URL')  # noqa
def step_impl(context, id, table):
    context.driver.get(
        context.URL + '{}/update/id/{}'.format(table, id))


@given(u'create {table} URL')  # noqa
def step_impl(context, table):
    context.driver.get(
        context.URL + '{}/create/'.format(table, id))


@given(u'list {table} URL')  # noqa
def step_impl(context, table):
    context.driver.get(
        context.URL + '{}/'.format(table, id))


@given(u'User {name} form')  # noqa
def step_impl(context, name):
    user = context.dbsession.query(
        context.models['user']).filter_by(name=name).one()
    context.driver.get(context.URL + 'user/update/id/{}'.format(user.id))


@when(u'Change user name to {name}')  # noqa
def step_impl(context, name):
    name_field = context.driver.find_element_by_xpath(
        ".//*[starts-with(@id, 'deformField') and @name='name']"
    )
    name_field.clear()
    name_field.send_keys(name)
    context.driver.find_element_by_xpath(
        "//*[@name = 'form.submitted']"
    ).click()
    context.user = context.dbsession.query(
        context.models['user']).filter_by(name=name).one()


@when(u'Change {name} to {value}')  # noqa
def step_impl(context, name, value):
    field = context.driver.find_element_by_xpath(
        ".//*[starts-with(@id, 'deformField') and @name='{}']".format(name)
    )
    if value.lower() == 'toggle':
        id = field.get_attribute("id")
        context.driver.find_element_by_xpath(
            ".//label[@for='{}' and not(@class)]".format(id)
        ).click()
    else:
        field.clear()
        field.send_keys(value)


@then(u'{field} == {value}')  # noqa
def step_impl(context, field, value):
    field = context.driver.find_element_by_xpath(
        ".//*[starts-with(@id, 'deformField') and @name='{}']".format(field)
    )
    field_value = field.get_attribute('value')
    if value.lower() == 'true':
        assert field.is_selected()
    elif value.lower() == 'false':
        assert not field.is_selected()
    else:
        assert value == field_value


@when('Submitt')  # noqa
def step_impl(context):
    context.driver.find_element_by_xpath(
        "//*[@name = 'form.submitted']"
    ).click()


@when(u'Delete user {name}')  # noqa
def step_impl(context, name):
    user = context.dbsession.query(
        context.models['user']).filter_by(name=name).one()
    context.user_id = user.id
    context.driver.get(context.URL + 'user/delete/id/{}'.format(user.id))


@then(u'I should find user in user table')  # noqa
def step_impl(context):
    user = context.user
    time.sleep(2)
    context.driver.get(context.URL + 'user/update/id/{}'.format(user.id))
    assert user.name in context.driver.page_source


@then(u"I don't want find user in user table")  # noqa
def step_impl(context):
    user_id = context.user_id
    user = context.dbsession.query(
        context.models['user']).filter_by(id=user_id).first()
    assert user is None
    context.driver.get(context.URL + 'user/update/id/{}'.format(user_id))
    assert '404' in context.driver.page_source
