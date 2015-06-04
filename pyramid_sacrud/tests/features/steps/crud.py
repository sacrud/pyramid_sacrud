from behave import given


@given(u'update {id} {table} URL')  # noqa
def step_impl(context, id, table):
    context.driver.get(
        context.URL + '{}/update/id/{}'.format(table, id))
