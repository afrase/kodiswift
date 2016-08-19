"""

kodiswift
---------

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

The current documentation still needs updated

Development
```````````

This project is a fork of xbmcswift2.


Contact
```````

https://github.com/Sinap/kodiswift

afrase91@gmail.com
"""
from setuptools import setup, find_packages

setup(
    name='kodiswift',
    version='0.0.5',
    author='Aaron Frase',
    author_email='afrase91@gmail.com',
    description='A micro framework for rapid development of Kodi plugins.',
    license='GPL3',
    keywords='example documentation tutorial',
    url='https://github.com/Sinap/kodiswift',
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    long_description=__doc__,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Natural Language :: English',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
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
