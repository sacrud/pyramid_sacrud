Configuration
=============

Initialize
----------

.. code-block:: python
    :linenos:

    from .models import (Model1, Model2, Model3,)

    # add SQLAlchemy backend
    config.include('ps_alchemy')

    # add pyramid_sacrud and project models
    config.include('pyramid_sacrud')
    settings = config.registry.settings
    settings['pyramid_sacrud.models'] = (
        ('Group1', [Model1, Model2]),
        ('Group2', [Model3])
    )

check it there http://localhost:6543/sacrud/

Set another prefix
------------------

.. code-block:: python

    config.include('pyramid_sacrud', route_prefix='admin')

now it there http://localhost:6543/admin/

Template redefinition
---------------------

:mod:`pyramid_sacrud` use **Jinja2** template renderer.
Just create template file in your project templates/sacrud directory:

.. code-block:: bash

    yourapp/
    └── templates
        └── sacrud
              └── home.jinja2  <-- custom template for pyramid_sacrud home page

You can find a list of all the templates here
https://github.com/sacrud/pyramid_sacrud/tree/master/pyramid_sacrud/templates/sacrud

Translate widget name
---------------------

.. seealso::

    For more information see `Internationalization and Localization
    <http://docs.pylonsproject.org/docs/pyramid/en/latest/narr/i18n.html>`_

.. figure:: /_static/img/locale_en.png
    :align: left

    http://localhost:6543/sacrud/?_LOCALE_=en

.. figure:: /_static/img/locale_ru.png

    http://localhost:6543/sacrud/?_LOCALE_=ru

.. raw:: html

   <br />

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
