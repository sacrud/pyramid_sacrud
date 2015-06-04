pyramid_sacrud - Pyramid CRUD interface based on `sacrud
<https://github.com/ITCase/sacrud>`_ and SQLAlchemy.

`pyramid_sacrud` will solve your problem of CRUD WEB interface for Pyramid.
Unlike classical CRUD interface, `pyramid_sacrud
<https://github.com/ITCase/pyramid_sacrud>`_ allows override and flexibly
customize interface. (that is closer to `django.contrib.admin`)

Look how easy it is to use with Pyramid:

.. code-block:: python

    from .models import (Model1, Model2, Model3,)
    # add sacrud and project models
    config.include('pyramid_sacrud')
    settings = config.registry.settings
    settings['pyramid_sacrud.models'] = (('Group1', [Model1, Model2]),
                                         ('Group2', [Model3]))

go to http://localhost:6543/sacrud/

Example can be found here https://github.com/ITCase/pyramid_sacrud/tree/master/example
