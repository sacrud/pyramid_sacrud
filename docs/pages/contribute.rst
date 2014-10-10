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


