# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

from kodiswift.logger import log
from kodiswift.mockxbmc import utils

__all__ = ['Addon']


def _get_env_setting(name):
    return os.getenv('KODISWIFT_%s' % name.upper())


# noinspection PyPep8Naming
class Addon(object):
    def __init__(self, id=None):
        # In CLI mode, kodiswift must be run from the root of the addon
        # directory, so we can rely on getcwd() being correct.
        addon_xml = os.path.join(os.getcwd(), 'addon.xml')
        _id = None
        if os.path.exists(addon_xml):
            _id = utils.get_addon_id(addon_xml)
        self._info = {
            'id': id or _id,
            'name': utils.get_addon_name(addon_xml),
            'profile': 'special://profile/addon_data/%s/' % _id,
            'path': 'special://home/addons/%s' % _id
        }
        self._strings = {}
        self._settings = {}
        strings_fn = os.path.join(
            os.getcwd(), 'resources', 'language', 'English', 'strings.po')
        utils.load_addon_strings(self, strings_fn)

    def getAddonInfo(self, prop):
        properties = ['author', 'changelog', 'description', 'disclaimer',
                      'fanart', 'icon', 'id', 'name', 'path', 'profile',
                      'stars', 'summary', 'type', 'version']
        if prop not in properties:
            raise ValueError('%s is not a valid property.' % prop)
        return self._info.get(prop, 'Unavailable')

    def getLocalizedString(self, str_id):
        key = str(str_id)
        if key not in self._strings:
            raise KeyError('id not found in English/strings.po or '
                           'strings.xml.')
        return self._strings[key]

    def getSetting(self, key):
        log.warning('xbmcaddon.Plugin.getSetting() has not been implemented '
                    'in CLI mode.')
        try:
            value = self._settings[key]
        except KeyError:
            # see if we have an env var
            value = _get_env_setting(key)
            if _get_env_setting(key) is None:
                value = raw_input(
                    '* Please enter a temporary value for %s: ' % key)
            self._settings[key] = value
        return value

    def setSetting(self, key, value):
        self._settings[key] = value

    def openSettings(self):
        pass
