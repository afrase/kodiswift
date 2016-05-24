# -*- coding: utf-8 -*-
from kodiswift import Plugin


plugin = Plugin()


@plugin.route('/')
def index():
    item = {
        'label': 'Hello Kodi!',
        'path': 'http://example.com/video.mp4',
        'is_playable': True
    }
    return [item]


if __name__ == '__main__':
    plugin.run()
