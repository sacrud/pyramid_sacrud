import os
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

here = os.path.dirname(os.path.realpath(__file__))


def read(name):
    with open(os.path.join(here, name)) as f:
        return f.read()


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = [
            '--cov=pyramid_sacrud', '-v', '-s'
        ]

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.verbose = True
        self.test_suite = 'tests'

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='pyramid_sacrud',
    version="0.3.3",
    url='http://github.com/sacrud/pyramid_sacrud/',
    author='Svintsov Dmitry',
    author_email='sacrud@uralbash.ru',

    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    cmdclass={"test": PyTest},
    test_suite='pytest',
    license="MIT",
    description='Pyramid CRUD, admin web interface.',
    long_description=read('README.rst') + '\n' + read('CHANGES.rst'),
    install_requires=read('requirements.txt'),
    tests_require=read('requirements.txt') + read('requirements-test.txt'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Natural Language :: Russian',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Framework :: Pyramid ",
        "Topic :: Internet",
        "Topic :: Database"
    ],
)
