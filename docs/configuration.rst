Application Configuration for Pyramid
=====================================

Initialize
----------

:mod:`sacrud` work with Jinja2 template renderer

.. note::
    work only with pyramid_jinja2<=1.10 version yet

.. code-block:: python
    :linenos:

    settings = config.registry.settings
    config.include('pyramid_jinja2')

    from .models import (Model1, Model2, Model3,)
    # add sacrud and project models
    config.include('sacrud.pyramid_ext')
    settings['sacrud.models'] = {'Group1': {
                                    'tables': [Model1, Model2],
                                    'position': 1,},
                                 'Group2': {
                                    'tables': [Model3],
                                    'position': 4,}
                                }

check it there http://localhost:6543/sacrud/

Set another prefix
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    config.include('sacrud.pyramid_ext', route_prefix='admin')

now it there http://localhost:6543/admin/

Configure models
----------------

Model verbose name
~~~~~~~~~~~~~~~~~~

.. code-block:: python
    :linenos:
    :emphasize-lines: 12

    class User(Base):

        __tablename__ = 'user'

        id = Column(Integer, primary_key=True)
        name = Column(String)

        def __init__(self, name):
            self.name = name

        # SACRUD
        verbose_name = 'My user model'

Instead "user", it will display "My user model"

.. image:: _static/img/verbose_name.png
    :alt: Model verbose name

Column verbose name
~~~~~~~~~~~~~~~~~~~

.. code-block:: python
    :linenos:
    :emphasize-lines: 7

    class User(Base):

        __tablename__ = 'user'

        id = Column(Integer, primary_key=True)
        name = Column(String,
                      info={"verbose_name": u'name of user', })

        def __init__(self, name):
            self.name = name

Instead "name", it will display "name of user"

.. image:: _static/img/column_verbose_name.png
    :alt: Column verbose name

Description for column
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python
    :linenos:
    :emphasize-lines: 8

    class User(Base):

        __tablename__ = 'user'

        id = Column(Integer, primary_key=True)
        name = Column(String,
                      info={"verbose_name": u'name of user',
                            "description": "put there name"})

        def __init__(self, name):
            self.name = name

Adds a description below

.. image:: _static/img/column_description.png
    :alt: Column description

Add css class for column
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python
    :linenos:
    :emphasize-lines: 14-16

    class TestCustomizing(Base):
        __tablename__ = "test_customizing"

        id = Column(Integer, primary_key=True)
        name = Column(String, info={"description": "put there name"})
        date = Column(Date, info={"verbose_name": 'date JQuery-ui'})
        name_ru = Column(String, info={"verbose_name": u'Название', })
        name_fr = Column(String, info={"verbose_name": u'nom', })
        name_bg = Column(String, info={"verbose_name": u'Име', })
        name_cze = Column(String, info={"verbose_name": u'název', })
        description = Column(Text)
        description2 = Column(Text)

        sacrud_css_class = {'tinymce': [description, description2],
                            'content': [description],
                            'name': [name], 'Date': [date]}

Adds css class for column

.. image:: _static/img/column_css.png
    :alt: Column with custom css classes

Configure displayed fields in grid
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python
    :linenos:
    :emphasize-lines: 18

    class TestCustomizing(Base):
        __tablename__ = "test_customizing"

        id = Column(Integer, primary_key=True)
        name = Column(String, info={"description": "put there name"})
        date = Column(Date, info={"verbose_name": 'date JQuery-ui'})
        name_ru = Column(String, info={"verbose_name": u'Название', })
        name_fr = Column(String, info={"verbose_name": u'nom', })
        name_bg = Column(String, info={"verbose_name": u'Име', })
        name_cze = Column(String, info={"verbose_name": u'název', })
        description = Column(Text)
        description2 = Column(Text)

        sacrud_css_class = {'tinymce': [description, description2],
                            'content': [description],
                            'name': [name], 'Date': [date]}

        sacrud_list_col = [name, name_ru, name_cze]

Shows only name, name_ru and name_cze columns in grid

.. image:: _static/img/sacrud_list_col.png
    :alt: Hide columns in grid

Configure displayed columns for detailed object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python
    :linenos:
    :emphasize-lines: 19-28

    class TestCustomizing(Base):
        __tablename__ = "test_customizing"

        id = Column(Integer, primary_key=True)
        name = Column(String, info={"description": "put there name"})
        date = Column(Date, info={"verbose_name": 'date JQuery-ui'})
        name_ru = Column(String, info={"verbose_name": u'Название', })
        name_fr = Column(String, info={"verbose_name": u'nom', })
        name_bg = Column(String, info={"verbose_name": u'Име', })
        name_cze = Column(String, info={"verbose_name": u'název', })
        description = Column(Text)
        description2 = Column(Text)

        sacrud_css_class = {'tinymce': [description, description2],
                            'content': [description],
                            'name': [name], 'Date': [date]}

        sacrud_list_col = [name, name_ru, name_cze]
        sacrud_detail_col = [('name space', [name,
                                             widget_horizontal(name_ru, name_bg,
                                                               name_fr, name_cze,
                                                               sacrud_name=u"i18n names")]),
                             ('description', [description, date,
                                              widget_horizontal(in_menu, visible,
                                                                in_banner,
                                                                sacrud_name=u"Расположение"),
                                              description2])
                             ]

Agregate and composite columns in detail view

.. image:: _static/img/sacrud_detail_col.png
    :alt: Agregate columns

Composite fields and column as custom function
----------------------------------------------

.. code-block:: python

    from sacrud.common.custom import widget_horizontal, widget_link, widget_m2m

Horizontal fields widget
~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

    see image above ("i18n names" row)

Column as link widget
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python
    :linenos:
    :emphasize-lines: 12

    class TestCustomizing(Base):
        __tablename__ = "test_customizing"

        id = Column(Integer, primary_key=True)
        name = Column(String, info={"description": "put there name"})
        date = Column(Date, info={"verbose_name": 'date JQuery-ui'})
        name_ru = Column(String, info={"verbose_name": u'Название', })
        name_fr = Column(String, info={"verbose_name": u'nom', })
        name_bg = Column(String, info={"verbose_name": u'Име', })
        name_cze = Column(String, info={"verbose_name": u'název', })

        sacrud_list_col = [widget_link(column=name, sacrud_name=u'name'), name_ru, name_cze]

Adds link for rows in column "name"

.. image:: _static/img/sacrud_list_col.png
    :alt: Column as link

M2M relation widget
~~~~~~~~~~~~~~~~~~~

Template redefinition
---------------------

Just create template file in your project template directory

.. code::

    myapp/
    └── templates
        └── sacrud

Dashboard config
----------------

Example from `<https://github.com/ITCase/pyramid_sacrud_example>`_

Configure your project

.. literalinclude:: _pyramid_sacrud_example/sacrud_example/__init__.py
   :linenos:
   :emphasize-lines: 85-88
   :language: py

External config for :ref:`Pyramid extension<pyramid_ext>`

.. literalinclude:: _pyramid_sacrud_example/sacrud_example/sacrud_config.py
   :linenos:
   :emphasize-lines: 31-
   :language: py

Dashboard model

.. note::
    If you need save dashboard widgets position

.. literalinclude:: _pyramid_sacrud_example/sacrud_example/models/funny_models.py
   :linenos:
   :language: py
   :pyobject: WidgetPosition

And set setting in you ini file

.. code::

    sacrud.dashboard_position_model = sacrud_example.models.funny_models:WidgetPosition

Result

.. image:: _static/img/dashboard.png
    :alt: Widgets dashboard
    :width: 900px
