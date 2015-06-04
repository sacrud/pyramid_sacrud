|Build Status| |Coverage Status| |Stories in Progress| |PyPI|

pyramid_sacrud
==============

Documentation `<http://pyramid-sacrud.readthedocs.org/en/latest/>`_

Overview
--------

pyramid_sacrud - Pyramid CRUD interface based on sacrud_ and SQLAlchemy.

`pyramid_sacrud` will solve your problem of CRUD interface for Pyramid.
Unlike classical CRUD interface, ``pyramid_sacrud`` allows override and
flexibly customize interface. (that is closer to `django.contrib.admin`)

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

And see...

|sacrud_index|

Installing
==========

GitHub
------

.. code-block:: bash

    pip install git+http://github.com/ITCase/pyramid_sacrud.git

PyPi
----

.. code-block:: bash

    pip install pyramid_sacrud

Source
------

.. code-block:: bash

    git clone git+http://github.com/ITCase/pyramid_sacrud.git
    python setup.py install

Contribute
----------

.. code-block:: bash

    git clone git+http://github.com/ITCase/pyramid_sacrud.git
    python setup.py develop

Support and Development
=======================

To report bugs, use the `issue tracker
<https://github.com/ITCase/pyramid_sacrud/issues>`_ or `waffle board
<https://waffle.io/ITCase/pyramid_sacrud>`_.

We welcome any contribution: suggestions, ideas, commits with new futures,
bug fixes, refactoring, docs, tests, translations etc

If you have question, contact me sacrud@uralbash.ru or IRC channel #sacrud

License
=======

The project is licensed under the MIT license.

.. |Build Status| image:: https://travis-ci.org/ITCase/pyramid_sacrud.svg?branch=master
   :target: https://travis-ci.org/ITCase/pyramid_sacrud
.. |Coverage Status| image:: https://coveralls.io/repos/ITCase/pyramid_sacrud/badge.png?branch=master
   :target: https://coveralls.io/r/ITCase/pyramid_sacrud?branch=master
.. |sacrud_index| image:: https://raw.githubusercontent.com/ITCase/pyramid_sacrud/master/docs/_static/img/index.png
   :target: https://raw.githubusercontent.com/ITCase/pyramid_sacrud/master/docs/_static/img/index.png
.. |Stories in Progress| image:: https://badge.waffle.io/ITCase/pyramid_sacrud.png?label=in%20progress&title=In%20Progress
   :target: http://waffle.io/ITCase/pyramid_sacrud
.. |PyPI| image:: http://img.shields.io/pypi/dm/pyramid_sacrud.svg
   :target: https://pypi.python.org/pypi/pyramid_sacrud/

.. _sacrud: https://github.com/ITCase/sacrud/


.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/ITCase/pyramid_sacrud
   :target: https://gitter.im/ITCase/pyramid_sacrud?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
