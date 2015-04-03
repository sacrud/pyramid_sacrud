Documentation contribute
========================

For generate README.rst run:
----------------------------

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

