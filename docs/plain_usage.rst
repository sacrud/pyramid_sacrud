Plain use `sacrud`
=================

CREATE action
-------------

.. code-block:: python
    :linenos:

    from sacrud.action import CRUD

    data = {'name': 'Electronics',
            'parent_id': '10',
           }
    group_obj = CRUD(DBSession, Groups, request=data).add()
    print group_obj.id

For more details see:

* :mod:`sacrud.action.CRUD`
* :mod:`sacrud.tests.test_action.ActionTest.test_create`

UPDATE action
-------------

.. code-block:: python
    :linenos:

    from sacrud.action import CRUD

    data = {'name': 'Admin',
           }
    CRUD(DBSession, Profile, pk={'id': 5}, request=data).add()

For more details see:

* :mod:`sacrud.action.CRUD`
* :mod:`sacrud.tests.test_action.ActionTest.test_update`


DELETE action
-------------

.. code-block:: python
    :linenos:

    from sacrud.action import CRUD

    CRUD(DBSession, Profile, pk={'id': 1}).delete()

For more details see:

* :mod:`sacrud.action.CRUD`
* :mod:`sacrud.tests.test_action.ActionTest.test_delete`

Example projects use plain `sacrud`
-----------------------------------

`sacrud_example <https://github.com/ITCase/pyramid_sacrud_example>`_

.. literalinclude:: _pyramid_sacrud_example/sacrud_example/lib/fixture.py
   :linenos:
   :language: py
   :pyobject: add_fixture
