Frontend contribute
===================

For working with CSS and JavaScript you need install Node.js_, NPM_, Bower_,
Browserify_ and Gulp_.

.. _Node.js: http://nodejs.org/
.. _NPM: https://www.npmjs.org/
.. _Bower: http://bower.io/
.. _Browserify: http://browserify.org/
.. _Browserify-Shim: https://github.com/thlorenz/browserify-shim
.. _Gulp: http://gulpjs.com/

.. note::

    If you don’t have Node.js and NPM installed, get it first.

Installing Node.js dependencies:

.. code:: bash

    npm install

Install Bower:

.. code:: bash

    npm install --global bower

Install packages with Bower:

.. code:: bash

    bower install

Packages will be install to **pyramid_sacrud/bower_components/**

CSS
---

СSS files are located in **pyramid_sacrud/static/css/**.

Before changing css files you may run **gulp watch** task:

.. code:: bash

    gulp watch

or you can change css and then and run **gulp css** task:

.. code:: bash

    gulp css

.. note::

    For more information about **gulp css** task see **gulpfile.js**

When you change any **css** file gulp concatenates all files in folder and
create **__pyramid_sacrud.css** file in `pyramid_sacrud/static/css/`.

JavaScript
----------

**pyramid_sacrud** use **Browserify**, file for browserify build is **main.js**
in **pyramid_sacrud/static/js/**.

.. code:: bash

    pyramid_sacrud/pyramid_sacrud/static/js
    |
    |   main.js
    |   __pyramid_sacrud.js
    |   __pyramid_sacrud.js.map
    |
    +---app
    |   |   options.js
    |   |
    |   /---common
    |           checkbox.js
    |           popup.js
    |           selectable.js
    |
    /---tests
            link-check.js
            login-logout.js
            tests.js


Before changing **js** modules you may run **gulp watch** task:

.. code:: bash

    gulp watch

or you can change js and then and run **gulp browserify** task:

.. code:: bash

    gulp browserify


When you change any js file, browserify build **__pyramid_sacrud.js** in **pyramid_sacrud/static/js/**.

.. note::

    For more information about **gulp browserify** task see **gulpfile.js**

.. tip::

    For more information about browserify visit Browserify_

Project modules
~~~~~~~~~~~~~~~

Options
"""""""
JQuery selectors list.

Popup
"""""
Popup object is needed for works with pop-up window.

Create a new Popup:

.. code-block:: javascript
    :linenos:

    var Popup = require('popup.js');
    var popup = new Popup(options);

.. epigraph::

    Arguments:
        * options - Options object.

SelectableTable
"""""""""""""""
SelectableTable object is needed for works with table. Using JQuery-UI Selectable widget.

Create a new SelectableTable:

.. code-block:: javascript
    :linenos:

    var SelectableTable = require('selectable.js');
    var selectable_table = new SelectableTable(el, options);

.. epigraph::

    Arguments:
        * el - JQuery selector (set in options.popup).
        * options - Options object.

Install modules
~~~~~~~~~~~~~~~
All modules are installed by using **bower**. After installing, you need set
path to module in package.json in "browser" and specify "exports" and
"depends"(if need) in "browserify-shim" settings, default **package.json** file
looks like:

.. code-block:: js
    :linenos:

    "browser": {
        "jquery": "./bower_components/jquery/dist/jquery.min.js",
        "jquery-ui": "./bower_components/jquery-ui/ui/minified/jquery-ui.min.js"
    },
    "browserify-shim": {
        "jquery": "$",
        "jquery-ui": {
            "depends": "jquery"
        },
    }

.. tip::

    For more information about browserify visit Browserify-Shim_

For update each dependency in package.json, just use `npm-check-updates
<https://www.npmjs.org/package/npm-check-updates>`_.

.. code-block:: bash

   $ npm install -g npm-check-updates
   $ npm-check-updates -u
   $ npm install

Using modules
~~~~~~~~~~~~~
To use module, you need to define it in **main.js** via **require()** function:

.. code-block:: javascript
    :linenos:

    require('jquery');

After that, they will be available for entire project.

Сreate a new module
~~~~~~~~~~~~~~~~~~~

To define a module, just create a JavaScript file **my_module.js**, in **pyramid_sacrud/static/js/** and write something like this:

.. code-block:: javascript
    :linenos:

    module.exports = function some_func(args) {
        console.log(args)
    };

Add it in **main.js** via **require()** function and call, to use in site:

.. code-block:: javascript
    :linenos:

    var myModule = require('my_module');
    myModule(args);

Testing
-------

Install Testing tools:

.. code:: bash

    npm install

or install package manually

.. code:: bash

    npm install mocha chai cheerio phantomjs --save-dev

Tests are written using Mocha framework, you need install Mocha_, Chai_, Cheerio_ and Phantomjs_.

.. _Mocha: http://mochajs.org/
.. _Chai: http://chaijs.com/
.. _Cheerio: https://github.com/cheeriojs/cheerio
.. _Phantomjs: http://phantomjs.org/

.. note::

    Also, you need a project running on the **localhost:6543** port. See
    `example <https://github.com/ITCase/pyramid_sacrud/tree/master/example>`_ project.

.. important::

    Install Mocha in global (npm install mocha --global) for Windows.


All tests found in directory **pyramid_sacrud/static/js/test/**

To run tests for javascript, use **npm test** command from category containing package.json:

.. code:: bash

    npm test

or run

.. code:: bash

    mocha -b --timeout 5000 pyramid_sacrud/static/js/tests/
