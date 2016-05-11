"""
    kodiswift.actions
    ------------------

    This module contains wrapper functions for Kodi built-in functions.

    :copyright: (c) 2012 by Jonathan Beluch
    :license: GPLv3, see LICENSE for more details.
"""


def background(url):
    """This action will run an addon in the background for the provided URL.

    See 'Kodi.RunPlugin()' at
    http://wiki.xbmc.org/index.php?title=List_of_built-in_functions.
    """
    return 'Kodi.RunPlugin(%s)' % url


def update_view(url):
    """This action will update the current container view with provided url.

    See 'Kodi.Container.Update()' at
    http://wiki.xbmc.org/index.php?title=List_of_built-in_functions.
    """
    return 'Kodi.Container.Update(%s)' % url
