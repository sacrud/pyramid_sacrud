.. _architecture:

New Arcitecture
===============

:ref:`old_architecture` is good, but it does not allow use tree structure of
resources and has hard depency from :mod:`SQLAlchemy`, :mod:`sacrud`,
:mod:`sacrud_deform` etc... This is not flexible solution. A new generation of
:mod:`pyramid_sacrud` >= 0.3.0 represent just interface for any backends, like:

* `ps_alchemy <https://github.com/sacrud/ps_alchemy>`_ - handle SQLAlchemy
  resourse
* ps_peewee - handle PeeweeORM resourse
* ps_ponyorm - handle PonyORM resourse
* ps_djangoorm - handle Django ORM resourse
* ps_mongodb - handle MongoDB resourse
* and unniversal interface writing your own backends for example:

  * you can write filesystem backend which shown files in
    :mod:`pyramid_sacrud` and provide to you CRUD operations.
  * OS process backend shown process in :mod:`pyramid_sacrud` and allow to kill it
  * and all you can come to mind.

ziggform_* - it's abstract modules, this is what needs to be done. I like the
idea of `ziggurat_form <https://github.com/ergo/ziggurat_form>`_  so I use such
names.

.. figure:: /_static/pencil/new_architecture.png

.. _old_architecture:

Old Arcitecture
===============

Main page
---------

He takes all the resources of the settings to return them to the template
``home.jinja2``. It implemented in :func:`pyramid_sacrud.views.sa_home`.

.. figure:: /_static/pencil/home_how_it_works.png

List of rows
------------

He takes all rows of resource, paginate it and return to template ``list.jinja2``.
It implemented in :class:`pyramid_sacrud.views.CRUD.List`. For select action
used :mod:`sacrud` and :meth:`sacrud.action.CRUD.read`.

.. figure:: /_static/pencil/read_how_it_works.png

Delete row
----------

He delete selected row and redirect to list of rows. It implemented in
:class:`pyramid_sacrud.views.CRUD.Delete`. For delete action used :mod:`sacrud`
and :meth:`sacrud.action.CRUD.delete`.

.. figure:: /_static/pencil/delete_how_it_works.png

Form for CREATE/DELETE action
-----------------------------

If you send GET request it return HTML form for your module. To generate form
it used :mod:`sacrud_deform`. `sacrud_deform` generate form with schema from
:mod:`ColanderAlchemy` and widgets from :mod:`deform`. The main task of
:mod:`sacrud_deform` is choose the right widgets from :mod:`deform` and make
select widget for relationships. It implemented in
:class:`pyramid_sacrud.views.CRUD.Add` and used template ``create.jinja2``.

.. figure:: /_static/pencil/add_how_it_works.png

POST request for CREATE/DELETE action
-------------------------------------

If you send POST request it validate form and do create/update action from
:mod:`sacrud` respectively :meth:`sacrud.action.CRUD.create` and
:meth:`sacrud.action.CRUD.update`. It implemented in
:class:`pyramid_sacrud.views.CRUD.Add`.

.. figure:: /_static/pencil/add_post_how_it_works.png



