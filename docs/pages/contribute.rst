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


JavaScript coder
~~~~~~~~~~~~~~~~

For working with JavaScript you need install Node.js_, NPM_, Browserify_ and Gulp_.

.. _Node.js: http://nodejs.org/
.. _NPM: https://www.npmjs.org/
.. _Browserify: http://browserify.org/
.. _Gulp: http://gulpjs.com/

If you don’t have node and npm installed, get it first.


Install components
==================

**package.json** for npm in the `pyramid_sacrud/static/js/` folder.

Installing browserify, gulp and other dependencies:

.. code:: bash

    npm install

Install Bower_:

.. _Bower: http://bower.io/

.. code:: bash

    npm install -g bower
      
Manifest file **bower.json** in the `pyramid_sacrud/static/js/` folder.

Install packages with bower install:

.. code:: bash

    bower install

Packages installs to `pyramid_sacrud/static/js/bower_components/`


Getting Started
===============

File for browserify build is **main.js** on `pyramid_sacrud/static/js/`.

Project modules are on `pyramid_sacrud/static/js/app/`.

Before changing js modules you need to run \'watch\' task with gulp: 

.. code:: bash

    gulp watch
    
When you change any js file browserify build **__main.js** on `pyramid_sacrud/static/js/`.


Using modules
=============

To use module, you need to define it in **main.js** via require() function:

.. code-block:: javascript
    
    require('jquery');

After that, they will be available for entire project.


Сreate a new module
===================

To define a module, just create a JavaScript file, and write something like this:

.. code-block:: javascript
    
    module.exports = function() {
        function some_func() {
            // anything do
        }
    };

Add it in **main.js** via require() function and call, to use in site:

.. code-block:: javascript

    var myModule = require('my_module');
    myModule();


Testing
=======

`coming soon`


Documentation contribute
------------------------

For generate README.rst run:

.. code:: bash

    make readme

This hook make single \*.rst file replacing ".. include::" directive on plain text.
It is necessary for github and PyPi main page because he does not know how to include.

.. literalinclude:: ../make_README.py
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
