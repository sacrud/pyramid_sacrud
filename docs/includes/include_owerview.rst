pyramid_sacrud - Pyramid CRUD interface based on `sacrud <https://github.com/ITCase/sacrud>`_ and SQLAlchemy.

`pyramid_sacrud` will solve your problem of CRUD interface for Pyramid.
Unlike classical CRUD interface, `pyramid_sacrud <https://github.com/ITCase/pyramid_sacrud>`_ allows override and flexibly customize interface.
(that is closer to `django.contrib.admin`)

Look how easy it is to use with Pyramid:

.. code-block:: python

    from .models import (Model1, Model2, Model3,)
    # add sacrud and project models
    config.include('pyramid_sacrud')
    settings = config.registry.settings
    settings['pyramid_sacrud.models'] = {'Group1': {
                                            'tables': [Model1,
                                                       Model2],
                                            'position': 1,},
                                         'Group2': {
                                            'tables': [Model3],
                                            'position': 4,}
                                         }

go to http://localhost:6543/sacrud/
