# -*- coding: utf-8 -*-
from __future__ import absolute_import

import sys

PY3 = sys.version_info.major == 3

if PY3:
    iteritems = lambda d: iter(d.items())

    text_type = str
    string_types = (str,)

    # noinspection PyUnresolvedReferences
    import pickle

    # noinspection PyShadowingBuiltins
    input = input
    # noinspection PyUnresolvedReferences
    import urllib.parse as urllib
    # noinspection PyUnresolvedReferences
    import urllib.parse as urlparse
    # noinspection PyUnresolvedReferences,PyCompatibility
    from urllib.request import urlopen
else:
    # noinspection PyShadowingBuiltins
    unichr = unichr
    text_type = unicode
    string_types = (str, unicode)

    # noinspection PyCompatibility
    iteritems = lambda d: d.iteritems()

    # noinspection PyUnresolvedReferences
    import cPickle as pickle

    # noinspection PyShadowingBuiltins
    input = raw_input
    # noinspection PyUnresolvedReferences
    import urllib
    # noinspection PyUnresolvedReferences
    import urlparse
    # noinspection PyUnresolvedReferences,PyCompatibility
    from urllib2 import urlopen
