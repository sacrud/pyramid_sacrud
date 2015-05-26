from setuptools import setup

version = '1.0'

setup(
    name='pyramid_sacrud_example',
    version=version,
    py_modules=['pyramid_sacrud_example'],
    entry_points="""
[paste.app_factory]
main = pyramid_sacrud_example:main
    """,
)
