Localization
============

.. figure:: /_static/img/locale_en.png
    :align: left

    http://localhost:6543/sacrud?_LOCALE_=en

.. figure:: /_static/img/locale_ru.png

    http://localhost:6543/sacrud?_LOCALE_=ru

Translate widget name
---------------------

To translate widgets on main page,
you can use standart translate method for Pyramid.

.. code-block:: python

    from pyramid.i18n import TranslationStringFactory

    _ = TranslationStringFactory('myapplication')
    settings['pyramid_sacrud.models'] = (
        (_('Permissions'), (
                UserPermission,
                UserGroup,
                Group,
                GroupPermission,
                Resource,
                UserResourcePermission,
                GroupResourcePermission,
                ExternalIdentity,
            )
        ),
        (_('Users'), (User, Staff))
    )

For more information see `Internationalization and Localization <http://docs.pylonsproject.org/docs/pyramid/en/latest/narr/i18n.html>`_

Translate model name
--------------------

.. figure:: /_static/img/locale_model_en.png
    :align: left

.. figure:: /_static/img/locale_model_ru.png

| http://localhost:6543/sacrud/users_permissions/update/perm_name/pyramid_sacrud_home/user_id/1?_LOCALE_=en
| http://localhost:6543/sacrud/users_permissions/update/perm_name/pyramid_sacrud_home/user_id/1?_LOCALE_=ru

.. code-block:: python

    class GroupPermission(GroupPermissionMixin, Base):
        verbose_name = _('Permissions of group')

Translate group in edit/create form
-----------------------------------

.. figure:: /_static/img/locale_form_en.png
    :align: left

    http://localhost:6543/admin/users/update/id/1?_LOCALE_=en

.. figure:: /_static/img/locale_form_ru.png

    http://localhost:6543/admin/users/update/id/1?_LOCALE_=ru

.

.. code-block:: python

    from sacrud.common import TableProperty

    class User(UserMixin, Base):
        verbose_name = _('Users')

        id = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(Unicode, nullable=False)
        middlename = Column(Unicode, nullable=False)
        surname = Column(Unicode, nullable=False)

        def __repr__(self):
            return self.name + ' ' + self.middlename + ' ' + self.surname

        # SACRUD
        @TableProperty
        def sacrud_detail_col(cls):
            col = cls.columns
            return [('', [col.user_name, col.email, col.user_password]),
                    (_('personal data'), [col.name, col.middlename, col.surname])]
