import os
from kodiswift.logger import log
from kodiswift.mockxbmc import utils


def _get_env_setting(name):
    return os.getenv('KODISWIFT_%s' % name.upper())


# noinspection PyPep8Naming
class Addon(object):
    def __init__(self, addon_id=None):
        # In CLI mode, kodiswift must be run from the root of the addon
        # directory, so we can rely on getcwd() being correct.
        addon_xml = os.path.join(os.getcwd(), 'addon.xml')
        self._info = {
            'id': addon_id or utils.get_addon_id(addon_xml),
            'name': utils.get_addon_name(addon_xml),
        }
        self._strings = {}
        self._settings = {}

    def getAddonInfo(self, prop):
        properties = ['author', 'changelog', 'description', 'disclaimer',
                      'fanart', 'icon', 'id', 'name', 'path', 'profile',
                      'stars', 'summary', 'type', 'version']
        assert prop in properties, '%s is not a valid property.' % prop
        return self._info.get(prop, 'Unavailable')

    def getLocalizedString(self, str_id):
        key = str(str_id)
        assert key in self._strings, 'id not found in English/strings.xml.'
        return self._strings[key]

    def getSetting(self, key):
        log.warning('xbmcaddon.Addon.getSetting() has not been implemented in '
                    'CLI mode.')
        try:
            value = self._settings[key]
        except KeyError:
            # see if we have an env var
            value = _get_env_setting(key)
            if _get_env_setting(key) is None:
                value = raw_input('* Please enter a temporary value for %s: ' %
                                  key)
            self._settings[key] = value
        return value

    def setSetting(self, key, value):
        self._settings[key] = value

    def openSettings(self):
        pass
