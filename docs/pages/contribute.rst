Backend contrubute
==================

Same as `contributor's section of the documentation <http://docs.pylonsproject.org/en/latest/#contributing>`_ of Pyramid project.

Frontend contribute
===================

For working with CSS and JavaScript you need install Node.js_, NPM_, Bower_, Browserify_ and Gulp_.

.. _Node.js: http://nodejs.org/
.. _NPM: https://www.npmjs.org/
.. _Bower: http://bower.io/
.. _Browserify: http://browserify.org/
.. _Gulp: http://gulpjs.com/

.. note::

    If you don’t have Node.js and NPM installed, get it first.


Install components
------------------

**package.json** for NPM, **gulpfile.js** for Gulp and **bower.json** for Bower in the `pyramid_sacrud/static/` folder.

Installing Browserify, Gulp and other dependencies:

.. code:: bash

    npm install

Install Bower:

.. code:: bash

    npm install -g bower
      
Install packages with Bower install:

.. code:: bash

    bower install

Packages installs to `pyramid_sacrud/static/js/bower_components/`



CSS
---

СSS files are on `pyramid_sacrud/static/css/`.
    
Before changing css files you need to run "watch" task with gulp: 

.. code:: bash

    gulp watch

When you change any css file gulp concatenates all in **__main.css** on `pyramid_sacrud/static/css/`.


JavaScript coder
----------------

Getting Started
~~~~~~~~~~~~~~~

File for browserify build is **main.js** on `pyramid_sacrud/static/js/`.

Project modules are on `pyramid_sacrud/static/js/app/`.

Before changing js modules you need to run "watch" task with gulp: 

.. code:: bash

    gulp watch
    
When you change any js file, browserify build **__main.js** on `pyramid_sacrud/static/js/`.


Project modules
~~~~~~~~~~~~~~~
Options
.......
JQuery selectors list.

Popup
.....
Popup object is needed for works with pop-up window.

Create a new Popup:

.. code-block:: javascript

    var Popup = require('popup.js');
    var popup = new Popup(el, options);
    
.. epigraph::
    Arguments:
        * el - JQuery selector (set in options.popup).
        * options - Options object.

SelectableTable
...............

SelectableTable object is needed for works with table. Using JQuery-UI Selectable widget.

Create a new SelectableTable:

.. code-block:: javascript

    var SelectableTable = require('selectable.js');
    var selectable_table = new SelectableTable(el, options);
    
.. epigraph::

    Arguments:
        * el - JQuery selector (set in options.popup).
        * options - Options object.


Install modules
~~~~~~~~~~~~~~~
All modules are installed using the bower. After installing, you need set path to new module in package.json in "browser" and specify "exports" and "depends"(if need) in "browserify-shim" settings:

.. code-block:: json

    "browser": {
        "jquery": "path_to_module/jquery.js",
        "jquery-ui": "path_to_module/jquery-ui.js"
    },
    "browserify-shim": {
        "jquery": {
            "exports": "$"
        },
        "jquery-ui": {
          "exports": null,
          "depends": "jquery"
        }
    }


Using modules
~~~~~~~~~~~~~
To use module, you need to define it in **main.js** via require() function:

.. code-block:: javascript
    
    require('jquery');

After that, they will be available for entire project.


Сreate a new module
~~~~~~~~~~~~~~~~~~~

To define a module, just create a JavaScript file, and write something like this:

.. code-block:: javascript
    
    module.exports = function some_func(args) { 
        // anything do
    };    

Add it in **main.js** via require() function and call, to use in site:

.. code-block:: javascript

    var myModule = require('my_module');
    myModule(some_args);


Testing
~~~~~~~
The tests are written using Mocha framework.
For their work, you need install Mocha_, Chai_ and Selenium-webdriver_.

.. _Mocha: http://mochajs.org/
.. _Chai: http://chaijs.com/
.. _Selenium-webdriver: https://www.npmjs.org/package/selenium-webdriver/

.. note::
    
    Install Mocha in global(with -g) on Windows.

.. code:: bash

    npm install mocha
    npm install chai
    npm install selenium-webdriver

.. note::

    Also, you need a project running on the localhost with 8000 port. For example, you may use pyramid_sacrud_example_ (docs_)

    .. _pyramid_sacrud_example: https://github.com/ITCase/pyramid_sacrud_example
    .. _docs: http://pyramid-sacrud-example.readthedocs.org/en/latest/index.html
    
        
All tests are in the directory `pyramid_sacrud/static/js/test/`

To run tests for javascript, you need to use **npm test** command from category containing package.json:

.. code:: bash

    npm test
    

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
