Support and Development
=======================

To report bugs, use the `issue tracker <https://github.com/ITCase/pyramid_sacrud/issues>`_
or `waffle board <https://waffle.io/ITCase/pyramid_sacrud>`_.

We welcome any contribution: suggestions, ideas, commits with new futures, bug fixes, refactoring, docs, tests, translations etc

If you know Flask framework, it would be nice create connector to him like this.

If you have question, contact me sacrud@uralbash.ru

HTML coder
----------

CSS
~~~

.. note::
    You need install nodejs and stylus preprocessor

We use stylus preprocessor for write and concat CSS. If you want edit this, add to ini file setting ``sacrud.debug = True``

.. literalinclude:: ../pyramid_sacrud/__init__.py
   :linenos:
   :language: py
   :pyobject: add_css_webasset

JavaScript
~~~~~~~~~~

Use bower and webassets hook:

.. literalinclude:: ../pyramid_sacrud/__init__.py
   :linenos:
   :language: py
   :pyobject: add_js_webasset
