Frontend contribute
===================

For working with CSS and JavaScript you need install Node.js_, npm_ and
WebPack_.

.. _Node.js: http://nodejs.org/
.. _npm: https://www.npmjs.org/
.. _WebPack: https://webpack.github.io/

.. note::

    If you don’t have Node.js and NPM installed, get it first.

Installing Node.js dependencies:

.. code:: bash

    npm install

CSS
---

СSS files are located in ``pyramid_sacrud/static/css/``.
CSS pack in ``__main.css`` file in ``pyramid_sacrud/static/css/``.

JavaScript
----------

Js pack in ``__main.js`` in ``pyramid_sacrud/static/js/assets/``.

For update each dependency in package.json, just use `npm-check-updates
<https://www.npmjs.org/package/npm-check-updates>`_.

.. code-block:: bash

   $ npm install -g npm-check-updates
   $ npm-check-updates -u
   $ npm install

Build
-----

.. code-block:: bash

   webpack

For production:

.. code-block:: bash

   webpack -p
