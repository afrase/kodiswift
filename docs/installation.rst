.. _installation:

Installation
============

.. note::

    The purpose of kodiswift is to have the ability to run the addon on the
    command line as well as in Kodi. This means that we will have to install
    kodiswift twice, once for the command line and once as an Kodi addon.

    The Kodi version of kodiswift is a specially packaged version of the main
    release. It excludes some CLI code and tests. It also contains Kodi
    required files like addon.xml.

The easiest way to get the most recent version of kodiswift for Kodi is to
install an addon that requires kodiswift. You can find a list of such addons
on the :ref:`poweredby` page. The other options is download the current Kodi
distribution from https://github.com/jbeluch/kodiswift-xbmc-dist/tags and
unpack it into your addons folder.  

Now, on to installing kodiswift for use on the command line.

virtualenv
----------

Virtualenv is an awesome tool that enables clean installation and removal of
python libraries into a sequestered environment. Using a virtual environment
means that when you install a library, it doesn't pollute your system-wide
python installation. This makes it possible to install different versions of a
library in different environments and they will never conflict. It's a good
habit to get into when doing python development. So, first we're going to
install virtualenv.

If you already have pip installed, you can simply::

    $ sudo pip install virtualenv

or if you only have easy_install::

    $ sudo easy_install virtualenv

I also like to use some helpful virtualenv scripts, so install
virtualenv-wrapper as well::

    $ sudo pip install virtualenv-wrapper

Creating a Virtual Environment
------------------------------

Now we can create our virtualenv::

    $ mkvirtualenv kodiswift

When this completes, your prompt should now be prefixed by `(kodiswift)`. The
new prompt signals that we are now working within our virtualenv. Any libraries
that we install via pip will only be available in this environment. Now we'll
install kodiswift::

    $ pip install kodiswift

Everything should be good to go. When you would like to work on your project
in the future, issue the following command to start your virtual env::

    $ workon kodiswift

and to deactive the virtualenv::

    $ deactivate

You should check out the :ref:`commandline` page next.
