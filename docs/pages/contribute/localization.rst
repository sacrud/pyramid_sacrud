Localization contribute
=======================

setup.cfg
----------
See basic settings in `setup.cfg`
(More information see `there <http://babel.edgewall.org/wiki/Documentation/setup.html>`_)

extract_messages:

.. code:: bash

	python setup.py extract_messages

update_catalog:

.. code:: bash

	python setup.py update_catalog

compile_catalog:

.. code:: bash

	python setup.py compile_catalog

Or just run it through `make`

.. code:: bash

    make locale

For translate use `_ps` function:

.. literalinclude:: ../../pyramid_sacrud/includes/localization/__init__.py
   :linenos:
   :language: py

In templates:

.. code-block:: html

    <div class="dashboard-title">{{ _ps('Dashboard') }}</div>
    {{ _ps(_(crumb.name)) }}
