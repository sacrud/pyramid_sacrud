Support and Development
=======================

To report bugs, use the `issue tracker <https://github.com/ITCase/sacrud/issues>`_
or `waffle board <https://waffle.io/ITCase/sacrud>`_.

We welcome any contribution: suggestions, ideas, commits with new futures, bug fixes, refactoring, docs, tests, translations etc

If you know Flask framework, it would be nice create connector to him like :ref:`pyramid_ext <pyramid_ext>`

If you have question, contact me sacrud@uralbash.ru

HTML coder
----------

CSS
~~~

.. note::
    You need install nodejs and stylus preprocessor

We use stylus preprocessor for write and concat CSS. If you want edit this, add to ini file setting ``sacrud.debug = True``

For more detail see :ref:`pyramid_ext <pyramid_ext>`

.. literalinclude:: ../sacrud/pyramid_ext/__init__.py
   :linenos:
   :language: py
   :pyobject: add_css_webasset

JavaScript
~~~~~~~~~~

Use bower and webassets hook:

.. literalinclude:: ../sacrud/pyramid_ext/__init__.py
   :linenos:
   :language: py
   :pyobject: add_js_webasset
