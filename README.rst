|Build Status| |Coverage Status| |PyPI|

pyramid_sacrud
==============

Documentation `<http://pyramid-sacrud.readthedocs.org/>`_

Overview
--------

Pyramid CRUD interface. Provides an administration web interface for Pyramid.
Unlike classic CRUD, ``pyramid_sacrud`` allows overrides and flexibility to
customize your interface, similar to ``django.contrib.admin`` but uses a
different backend to provide resources. `New Architecture
<http://pyramid-sacrud.readthedocs.org/pages/contribute/architecture.html#architecture>`_
built on the resources and mechanism traversal, allows to use it in various
cases.

The list of standard backends:

* `ps_alchemy <http://github.com/sacrud/ps_alchemy>`_ - provides SQLAlchemy
  models.
* ps_mongo - provides MongoDB.
* etc..

Look how easy it is to use with Pyramid and SQLAlchemy:

.. code-block:: python

    from .models import (Model1, Model2, Model3,)

    # add SQLAlchemy backend
    config.include('ps_alchemy')

    # add sacrud and project models
    config.include('pyramid_sacrud')
    settings = config.registry.settings
    settings['pyramid_sacrud.models'] = (('Group1', [Model1, Model2]),
                                         ('Group2', [Model3]))

go to http://localhost:6543/sacrud/

And see...

|sacrud_index|

Example can be found here https://github.com/sacrud/ps_alchemy/tree/master/example

Installing
==========

.. code-block:: bash

    pip install pyramid_sacrud

Support and Development
=======================

To report bugs, use the `issue tracker
<https://github.com/sacrud/pyramid_sacrud/issues>`_.

We welcome any contribution: suggestions, ideas, commits with new futures,
bug fixes, refactoring, docs, tests, translations etc

If you have question, contact me sacrud@uralbash.ru or IRC channel #sacrud

License
=======

The project is licensed under the MIT license.

.. |Build Status| image:: https://travis-ci.org/sacrud/pyramid_sacrud.svg?branch=master
   :target: https://travis-ci.org/sacrud/pyramid_sacrud
.. |Coverage Status| image:: https://coveralls.io/repos/sacrud/pyramid_sacrud/badge.png?branch=master
   :target: https://coveralls.io/r/sacrud/pyramid_sacrud?branch=master
.. |sacrud_index| image:: https://raw.githubusercontent.com/sacrud/pyramid_sacrud/master/docs/_static/img/index.png
   :target: https://raw.githubusercontent.com/sacrud/pyramid_sacrud/master/docs/_static/img/index.png
.. |PyPI| image:: http://img.shields.io/pypi/dm/pyramid_sacrud.svg
   :target: https://pypi.python.org/pypi/pyramid_sacrud/
