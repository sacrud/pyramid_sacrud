|Build Status| |Coverage Status| |Stories in Progress| |PyPI|

pyramid_sacrud
==============

Documentation `<http://pyramid-sacrud.readthedocs.org/en/latest/>`_

Overview
--------

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

And see...

|sacrud_index|

Installing
==========

github
------

.. code-block:: bash

    pip install git+http://github.com/ITCase/pyramid_sacrud.git

current develop version

.. code-block:: bash

    pip install git+http://github.com/ITCase/pyramid_sacrud.git@develop

PyPi
----

.. code-block:: bash

    pip install pyramid_sacrud

source
------

.. code-block:: bash

    git clone git+http://github.com/ITCase/pyramid_sacrud.git
    python setup.py install

Support and Development
=======================

To report bugs, use the `issue tracker <https://github.com/ITCase/pyramid_sacrud/issues>`_
or `waffle board <https://waffle.io/ITCase/pyramid_sacrud>`_.

We welcome any contribution: suggestions, ideas, commits with new futures, bug fixes, refactoring, docs, tests, translations etc

If you know Flask framework, it would be nice create connector to him like this.

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


.. image:: https://d2weczhvl823v0.cloudfront.net/ITCase/pyramid_sacrud/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free

