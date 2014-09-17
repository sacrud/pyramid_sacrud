.. include:: contribute_include.rst

Frontend contribute
-------------------

CSS
~~~

.. note::
    You need install nodejs and stylus preprocessor only for develop

We use stylus preprocessor for write and concat CSS. If you want edit this, add to ini file setting ``sacrud.debug = True``

.. literalinclude:: ../pyramid_sacrud/__init__.py
   :linenos:
   :language: py
   :pyobject: add_css_webasset

JavaScript coder
~~~~~~~~~~~~~~~~

Use bower and webassets hook:

.. literalinclude:: ../pyramid_sacrud/__init__.py
   :linenos:
   :language: py
   :pyobject: add_js_webasset
