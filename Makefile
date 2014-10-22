all: test

test:
	nosetests --with-coverage --cover-package pyramid_sacrud --cover-erase --with-doctest --nocapture

coverage: test
	coverage html

run:
	pserve development.ini

shell:
	pshell development.ini

extract_messages:
	python setup.py extract_messages

update_catalog:
	python setup.py update_catalog

compile_catalog:
	python setup.py compile_catalog

locale: extract_messages update_catalog compile_catalog
