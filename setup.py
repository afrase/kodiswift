"""

kodiswift
~~~~~~~~~~

A micro framework to enable rapid development of Kodi plugins.


Features
````````

* Run the addon from the command line *or* within Kodi without changing any
  code.
* Helper libraries to make common Kodi api operations easy, like adding items,
  getting settings, creating temporary files, etc.
* Handles all the url parsing involved in plugin routing. No need to deal with
  complicated URLs and query strings.


Documentation
`````````````

The current documentation can be found at http://www.kodiswift.com

Development
```````````

This module is now available in the official Kodi Eden repository as
kodiswift.

This project is the next version of kodiswift. While the APIs are similar,
there are a few things that are not backwards compatible with the original
version, hence the new name.


Contact
```````

https://github.com/jbeluch/kodiswift

web@jonathanbeluch.com
"""
from setuptools import setup, find_packages

setup(
    name='kodiswift',
    version='0.3.0',
    author='Jonathan Beluch',
    author_email='web@jonathanbeluch.com',
    description='A micro framework for rapid development of Kodi plugins.',
    license='GPL3',
    keywords='example documentation tutorial',
    url='https://github.com/jbeluch/kodiswift',
    packages=find_packages(),
    include_package_data=True,
    long_description=__doc__,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python',
    ],
    entry_points={
        'console_scripts': [
            'kodiswift = kodiswift.cli.cli:main',
        ]
    },
    tests_require=[
        'nose',
        'mock',
    ],
)
