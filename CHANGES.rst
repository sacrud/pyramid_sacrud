0.2.0 (2015-11-13)
==================

- new materialize-css design
- webpack.js for build css and js

0.1.3 (2015-09-08)
==================

- fix fonts in MANIFEST.in
- fix update action, when value changed to empty

0.1.2 (2015-08-19)
==================

- remove crud_sessionmaker and use CRUD action directly  

0.1.1 (2015-06-12)
==================

Bug Fixes
---------

- Fix mass delete action with tree structure
- Move mass actions in separate view ``pyramid_sacrud.views.CRUD.Action``
- Fix non unicode flash message
- Add title to templates

0.1.0 (2015-06-12)
==================

- Now, ``sacrud_list_template`` and ``sacrud_edit_template`` options overrides
  the template (not include like before).

0.0.9 (2015-06-11)
==================

- fix settings['pyramid_sacrud.models'] with one table in list

0.0.8 (2015-06-04)
==================

- added BDD tests (#88, #89, #90)
- added example (see https://github.com/ITCase/pyramid_sacrud/tree/master/example)

Bug Fixes
---------

- fix settings['pyramid_sacrud.models'] with list of one list
- fix error 404 with static files
- clean javascript requires

0.0.7 (2015-04-24)
==================

Bug Fixes
---------

- fix for ItemsView not being subscriptable in py3 (#82)
- fix for ItemsView not being subscriptable in py3 (#82)

0.0.6 (2015-04-05)
==================

- added CHANGES.txt

Bug Fixes
---------

- fix home page dashboard widgets (#67)
- fix width of pagination (#64)
- fix pyramid_jinja2 version in requirements (#37)
- fix mass delete action

Features
--------

- new format of settings (read the docs)
- migrate to stefanofontanelli/ColanderAlchemy
- added support polymorphic tree models (#24)
