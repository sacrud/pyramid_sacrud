Backend contrubute
------------------

Same as `contributor's section of the documentation <http://docs.pylonsproject.org/en/latest/#contributing>`_ of Pyramid project.

Frontend contribute
-------------------

CSS
~~~

.. note::
    You need install nodejs and stylus preprocessor only for develop

We use stylus preprocessor for write and concat CSS. If you want edit this, add to ini file setting ``sacrud.debug_css = True``

.. literalinclude:: ../../pyramid_sacrud/assets.py
   :linenos:
   :language: py
   :pyobject: add_css_assets

JavaScript coder
~~~~~~~~~~~~~~~~
If you want edit this, add to ini file setting ``sacrud.debug_js = True``

Use `<http://bower.io>`_ and assets hook:

.. literalinclude:: ../../pyramid_sacrud/assets.py
   :linenos:
   :language: py
   :pyobject: add_js_assets

Documentation contribute
------------------------

For generate README.rst run:

.. code:: bash

    make readme

This hook make single \*.rst file replacing ".. include::" directive on plain text.
It is necessary for github and PyPi main page because he does not know how to include.

.. literalinclude:: make_README.py
   :linenos:
   :language: py

If you want generate html and README.rst run:

.. code:: bash

    make readme_html

or

.. code:: bash

    make readme html

Localization contribute
-----------------------

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
