all: test

test:
	python setup.py test

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

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
