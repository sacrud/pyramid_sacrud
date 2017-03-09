.. sacrud documentation master file, created by
   sphinx-quickstart on Fri Jun 27 15:28:02 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Overview
========

.. image:: _static/img/index.png
   :width: 600px
   :alt: SACRUD main page
   :align: right

Pyramid CRUD interface. Provides an administration web interface for Pyramid.
Unlike classic CRUD, ``pyramid_sacrud`` allows overrides and flexibility to
customize your interface, similar to ``django.contrib.admin`` but uses a
different backend to provide resources. :ref:`architecture` built on the
resources and mechanism traversal, allows to use it in various cases.

The list of standard backends:

* `ps_alchemy <http://github.com/sacrud/ps_alchemy>`_ - provides SQLAlchemy
  models.
* ps_mongo - provides MongoDB (doesn't exist yet).
* etc..

.. raw:: html

   <br clear="both"/>

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

Example can be found here:

   * https://github.com/sacrud/pyramid_sacrud/tree/master/examples
   * https://github.com/sacrud/ps_alchemy/tree/master/example

Usage
=====

.. toctree::
  :maxdepth: 2

  pages/install
  pages/configuration
  pages/permissions
  pages/examples/index.rst
  pages/api

Contribute
==========

.. toctree::
  :maxdepth: 3

  pages/contribute/index.rst

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

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

