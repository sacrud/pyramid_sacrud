.. include:: ../includes/include_contribute.rst

Frontend contribute
-------------------

CSS
~~~

.. note::
    You need install nodejs and stylus preprocessor only for develop

We use stylus preprocessor for write and concat CSS. If you want edit this, add to ini file setting ``sacrud.debug = True``

.. literalinclude:: ../pyramid_sacrud/assets.py
   :linenos:
   :language: py
   :pyobject: add_css_assets

JavaScript coder
~~~~~~~~~~~~~~~~

Use bower and assets hook:

.. literalinclude:: ../pyramid_sacrud/assets.py
   :linenos:
   :language: py
   :pyobject: add_js_assets
