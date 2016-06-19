# -*- coding: utf-8 -*-
"""
kodiswift.constants
--------------------

This module contains some helpful constants which ease interaction
with Kodi.

:copyright: (c) 2012 by Jonathan Beluch
:license: GPLv3, see LICENSE for more details.
"""
from __future__ import absolute_import

__all__ = ['SortMethod', 'VIEW_MODES']


class SortMethod(object):
    """Static class to hold all of the available sort methods. The prefix
    of 'SORT_METHOD_' is stripped.

    e.g. SORT_METHOD_TITLE becomes SortMethod.TITLE
    """
    ALBUM = 13
    ALBUM_IGNORE_THE = 14
    ARTIST = 11
    ARTIST_IGNORE_THE = 12
    BITRATE = 40
    CHANNEL = 38
    COUNTRY = 16
    DATE = 3
    DATEADDED = 19
    DATE_TAKEN = 41
    DRIVE_TYPE = 6
    DURATION = 8
    EPISODE = 22
    FILE = 5
    FULLPATH = 32
    GENRE = 15
    LABEL = 1
    LABEL_IGNORE_FOLDERS = 33
    LABEL_IGNORE_THE = 2
    LASTPLAYED = 34
    LISTENERS = 36
    MPAA_RATING = 28
    NONE = 0
    PLAYCOUNT = 35
    PLAYLIST_ORDER = 21
    PRODUCTIONCODE = 26
    PROGRAM_COUNT = 20
    SIZE = 4
    SONG_RATING = 27
    STUDIO = 30
    STUDIO_IGNORE_THE = 31
    TITLE = 9
    TITLE_IGNORE_THE = 10
    TRACKNUM = 7
    UNSORTED = 37
    VIDEO_RATING = 18
    VIDEO_RUNTIME = 29
    VIDEO_SORT_TITLE = 24
    VIDEO_SORT_TITLE_IGNORE_THE = 25
    VIDEO_TITLE = 23
    VIDEO_YEAR = 17

    @classmethod
    def from_string(cls, sort_method):
        """Returns the sort method specified. sort_method is case insensitive.
        Will raise an AttributeError if the provided sort_method does not
        exist.

        >>> SortMethod.from_string('title')
        """
        return getattr(cls, sort_method.upper())
