from zope.interface import Attribute, Interface


class ISacrudResource(Interface):
    title = Attribute(
        '''Title of template. This is displayed in the tag <title> on html
        page. For example it can be title="update user John".'''
    )
    breadcrumb = Attribute(
        'Set active link in breadcrumb if True.'
    )
    renderer = Attribute(
        '''Set renderer for view. For example it can be: 'json',
        '/sacrud/list.jinja2', bar.mako', etc...'''
    )
