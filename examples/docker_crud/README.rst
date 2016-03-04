Usage
-----

Simple admin web interface with CRUD operation for docker images. You can
delete and view it. In example uses default crud templates from
`ps_crud <https://github.com/sacrud/ps_crud>`_ module.

.. code-block:: bash

   $ cd examples/docker_crud/
   $ pip install -e .
   $ pserve development.ini --reload

and goto http://localhost:6543/admin/
