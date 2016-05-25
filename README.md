kodiswift
==========

[![Build Status](https://travis-ci.org/Sinap/kodiswift.svg?branch=develop)](https://travis-ci.org/Sinap/kodiswift)
[![codecov](https://codecov.io/gh/Sinap/kodiswift/branch/develop/graph/badge.svg)](https://codecov.io/gh/Sinap/kodiswift)
[![Code Health](https://landscape.io/github/Sinap/kodiswift/develop/landscape.svg?style=flat)](https://landscape.io/github/Sinap/kodiswift/develop)

A micro framework to enable rapid development of Kodi plugins.


## Features
* Run the addon from the command line *or* within Kodi without changing any
  code.
* Helper libraries to make common Kodi api operations easy, like adding items,
  getting settings, creating temporary files, etc.
* Handles all the url parsing involved in plugin routing. No need to deal with
  complicated URLs and query strings.

## Installation

kodiswift is available in pypi, so you can install via pip:

    pip install kodiswift

You should probably also read
http://www.kodiswift.com/en/latest/installation.html#installation to ensure it
is properly installed for Kodi as well.

## Documentation

The current documentation can be found at http://www.kodiswift.com. It covers
installation, quickstart, a guide to writing an addon and documentation for the
full kodiswift API.

## Upgrading from kodiswift

This project is the next version of kodiswift. While the APIs are similar,
there are a few things that are not backwards compatible with the original
version, hence the new name.

If you are upgrading an addon that used kodiswift, see
http://www.kodiswift.com/en/latest/upgrading.html#upgrading.

## Development

kodiswift is now available in the official Kodi Eden repository. Every time a
new release is created and uploaded to pypi, a new Kodi release will be created
as well. Be aware that Kodi's "version" for kodiswift will not match the
official python package version.

New features and bug fixes are done on the develop branch of this repo. If you
are interested in using the develop branch, you can install locally via pip:

    pip install git+git://github.com/jbeluch/kodiswift.git@develop

The documentation for the develop branch can be found at
http://www.kodiswift.com/en/develop/api.html#api.

## Contributing

Bugs, patches and suggestions are all welcome. I'm working on adding tests and
getting better coverage. Please ensure that your patches include tests as well
as updates to the documentation. Thanks!

## Support

\#kodiswift on freenode

https://github.com/jbeluch/kodiswift

Subscribe to the mailing list to be notified of new releases or to get help.
Send an email to kodiswift@librelist.com to subscribe.

web@jonathanbeluch.com
