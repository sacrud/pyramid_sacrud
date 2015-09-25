Usage
=====

.. code-block:: bash

   $ cd example
   $ python ps_pages_example.py

or

.. code-block:: bash

   $ cd example
   $ python setup.py develop
   $ pserve development.ini --reload

and goto http://localhost:6543/admin/

Auth example
------------

.. code-block:: bash

   $ pserve development_auth.ini --reload

and goto http://localhost:6543/admin/
and then http://localhost:6543/login
