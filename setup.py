"""a setuptools based setup module.

THIS HAS TO BE COPIED TO FOLDER THAT CONTAINS BASE, before executing (from there):

 python3 setup.py bdist_wheel

the wheel will then be in the dist folder

Then, from a virtualenv:

 wheel install <wheelname>

This will not install package dependencies (use PIP for the install to achieve this).

"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

from os import path, walk

#from config_base import evoke_major_version, evoke_minor_version

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'base/README.md')) as f:
    long_description = f.read()

# find all of the site data files
def site_files():
  tree=walk('base/site')
  files=[]
  for (dirpath,dirnames,filenames) in tree:
    if filenames:
      dp=dirpath.split('/',1)[1]
      files.append((dp,[(dirpath+'/'+f) for f in filenames]))
#    print(dirpath,filenames)
  return files

# the main setup:
setup(
    name='evoke',

    # Versions should comply with PEP440
    version='5.6',
    description='a simple and powerful python web framework with pythonic "evo" templating',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/howiemac/evoke',

    # Author details
    author='The Evoke Foundation',
    author_email='howiemac@gmail.com',

    # Choose your license
    license='modified BSD',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 3.6',
    ],

    # What does your project relate to?
    keywords='development http html twisted mysql',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
#    packages=find_packages(exclude=[]),
    packages=[
    'base',
    'base.app',
    'base.app.code',
    'base.data',
    'base.lib',
    'base.render',
    'base.serve',
    'base.Page',
    'base.Permit',
    'base.Reset',
    'base.Session',
    'base.User',
    ],
    #+find_packages(where='base',exclude=[]),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['twisted','mysqlclient','pillow'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={},

    # If there are data files included in your packages that need to be
    # installed, specify them here.
    # package_data={
    #    'sample': ['package_data.dat'],
    #},
    package_data={
        '': ['evo/*.evo'],
        'base.app.code': ['devstart','restart','start','stop'],
        '': ['site'],
#        'base.Page':['evo/*.evo'],
#        'base.User':['evo/*.evo'],
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],
    data_files=site_files(),
#    [
#        ('site/css', ['base/site/css/base.css']),
#        ('site/js', ['base/site/js/base.js']),
#    ],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={}
#        'console_scripts': [
#            'sample=sample:main',
#        ],
#    },

)

