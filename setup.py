import os
import glob
import fnmatch
from pyramid_sacrud import version
from setuptools import setup


def opj(*args):
    path = os.path.join(*args)
    return os.path.normpath(path)

badnames = [".pyc", ".py", "~", "no_"]


def find_data_files(srcdir, *wildcards, **kw):
    # get a list of all files under the srcdir matching wildcards,
    # returned in a format to be used for install_data
    def walk_helper(arg, dirname, files):
        if '.svn' in dirname:
            return
        names = []
        lst, wildcards = arg
        for wc in wildcards:
            wc_name = opj(dirname, wc)
            for f in files:
                filename = opj(dirname, f)

                if not any(bad in filename for bad in badnames):
                    if fnmatch.fnmatch(filename, wc_name)\
                            and not os.path.isdir(filename):
                        names.append(filename)
        if names:
            lst.append((dirname, names))

    file_list = []
    recursive = kw.get('recursive', True)
    if recursive:
        os.path.walk(srcdir, walk_helper, (file_list, wildcards))
    else:
        walk_helper((file_list, wildcards),
                    srcdir,
                    [os.path.basename(f) for f in glob.glob(opj(srcdir, '*'))])
    return file_list
files = find_data_files('pyramid_sacrud/', '*.*')
print 'files', files

setup(
    name='pyramid_sacrud',
    version=version.__version__,
    url='http://github.com/ITCase/pyramid_sacrud/',
    author='Svintsov Dmitry',
    author_email='root@uralbash.ru',

    packages=['pyramid_sacrud', 'pyramid_sacrud.common',
              'pyramid_sacrud.views'],
    data_files=files,
    include_package_data=True,
    zip_safe=False,
    test_suite="nose.collector",
    license="MIT",
    package_dir={'pyramid_sacrud': 'pyramid_sacrud'},
    package_data={
        'pyramid_sacrud': ['static/style/*.css',
                           'static/js/*.js',
                           'static/js/jquery/*.js',
                           'static/images/*',
                           'templates/*.jinja2', 'templates/forms/*.jinja2',
                           'templates/forms/actions/*.jinja2',
                           'templates/types/*.jinja2',
                           'tests/*.py', ],
    },
    description='Pyramid SQLAlchemy CRUD.',
    long_description=open('README.md').read(),
    install_requires=[
        "sacrud",
        "pyramid",
        "sqlalchemy",
        "transaction",
        'zope.sqlalchemy',
        'pyramid_webassets',
        'webhelpers',
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
