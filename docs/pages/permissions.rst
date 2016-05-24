Authorization
=============

If you use `RootFactory` for authorization, set ``PYRAMID_SACRUD_HOME``
permission for you accessed to pyramid_sacrud.

.. code-block:: python

   from pyramid_sacrud import PYRAMID_SACRUD_HOME, PYRAMID_SACRUD_VIEW

See example:

.. literalinclude:: ../../examples/auth_resource/main.py
   :caption: Rewource with __acl__
