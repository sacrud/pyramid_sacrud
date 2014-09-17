import os

from setuptools import find_packages, setup

this = os.path.dirname(os.path.realpath(__file__))


def readme():
    with open(os.path.join(this, 'README.rst')) as f:
        return f.read()


setup(
    name='pyramid_sacrud',
    version="0.0.1",
    url='http://github.com/ITCase/pyramid_sacrud/',
    author='Svintsov Dmitry',
    author_email='root@uralbash.ru',

    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite="nose.collector",
    license="MIT",
    package_dir={'pyramid_sacrud': 'pyramid_sacrud'},
    description='Pyramid SQLAlchemy CRUD.',
    long_description=readme(),
    install_requires=[
        "sacrud",
        "peppercorn",
        "sacrud_deform",
        "pyramid",
        "sqlalchemy",
        "colander",
        "deform",
        "transaction",
        "webassets",
        'pyramid_webassets',
        'pyramid_beaker',
        'paginate_sqlalchemy',
        'webtest',
        'cssmin',
        'jsmin',
    ],
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
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Framework :: Pyramid ",
        "Topic :: Internet",
        "Topic :: Database",
    ],
)
