Docker
======

.. include:: ../../../examples/docker_crud/README.rst

.. figure:: /_static/img/examples/docker-list.png
   :align: center

.. figure:: /_static/img/examples/docker-image.png
   :align: center

How it works
------------

``pyramid_sacrud`` copes with the resource technology, especially those who
adhere to the principle of Pyramid ``traversal``.
In this example, we create resources, associate them with the own views, but
inherit the templates from ``pyramid_sacrud`` and `ps_crud
<https://github.com/sacrud/ps_crud/>`_.
Also entry point for all resources from ``pyramid_sacrud`` settings is
:class:`~pyramid_sacrud.resources.GroupResource`.

Resources
~~~~~~~~~

When you pass the ``Docker`` in ``pyramid_sacrud`` settings, it automatically
derives from :class:`~pyramid_sacrud.resources.GroupResource`.
``Docker`` is a base resource and it not displayed in the Web interface,
therefore it doesn't require binding to the view.

.. literalinclude:: ../../../examples/docker_crud/resources.py
   :caption: Docker - base resource
   :pyobject: Docker

``Image`` represent a list of all docker images in Web interface.

.. literalinclude:: ../../../examples/docker_crud/resources.py
   :caption: Image - represent docker image lists
   :pyobject: Image

It uses view:

.. literalinclude:: ../../../examples/docker_crud/views.py
   :caption: View for Image resource
   :pyobject: admin_docker_list_view

With template ``ps_crud/list.jinja2`` from extension module ``ps_crud``.

.. code-block:: python

    @view_config(
        context=Image,
        renderer='ps_crud/list.jinja2',
        route_name=PYRAMID_SACRUD_VIEW
    )
    def admin_docker_list_view(context, request):
        """Show list of docker images."""

``UpdateFactory`` designed to reflect a particular image.

.. literalinclude:: ../../../examples/docker_crud/resources.py
   :caption: UpdateFactory - choices image
   :pyobject: UpdateFactory

.. literalinclude:: ../../../examples/docker_crud/views.py
   :caption: View for UpdateFactory resource
   :pyobject: admin_docker_update_view

Templates
~~~~~~~~~

.. literalinclude:: ../../../examples/docker_crud/templates/sacrud/redefineme.jinja2
   :caption: Added Docker logo to redefineme.jinja2 template
   :language: html+jinja

.. literalinclude:: ../../../examples/docker_crud/templates/target.jinja2
   :caption: Template for show image
   :language: html+jinja

Source code
-----------

`<https://github.com/sacrud/pyramid_sacrud/examples/docker_crud>`_
