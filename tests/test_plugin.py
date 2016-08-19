# -*- coding: utf-8 -*-
import os
import pickle
import shutil
import sys
from unittest import TestCase

from mock import patch

import kodiswift
from kodiswift import Plugin
from kodiswift.mockxbmc.xbmc import TEMP_DIR
from utils import preserve_cli_mode, preserve_cwd

# Ensure we are starting clean by removing old test folders
try:
    shutil.rmtree(TEMP_DIR)
except OSError:
    # doesn't exist, just pass
    pass


class TestInit(TestCase):
    def test_init_cli_mode(self):
        name = 'Hello Kodi'
        plugin_id = 'plugin.video.hellokodi'
        path = os.path.join(
            os.path.dirname(__file__), 'data', 'plugin', 'plugin.py')
        with preserve_cwd(os.path.dirname(path)):
            plugin = Plugin(name, plugin_id, path)

        self.assertEqual(plugin_id, plugin.id)
        self.assertEqual(plugin.name, name)
        self.assertEqual(plugin.info_type, 'video')
        self.assertTrue(os.path.isdir(plugin.storage_path))
        self.assertEqual(plugin.added_items, [])
        self.assertRaises(Exception, getattr, plugin, 'handle')
        self.assertRaises(Exception, getattr, plugin, 'request')
        # Test loading from strings.po
        self.assertEqual(
            plugin.addon.getLocalizedString(30100), 'View all results')

        addon_path = kodiswift.xbmc.translatePath(
            plugin.addon.getAddonInfo('path'))
        if not os.path.exists(addon_path):
            os.makedirs(addon_path)

    def test_init_cli_mode_no_strings_po(self):
        name = 'Hello Kodi'
        plugin_id = 'plugin.video.hellokodi'
        path = os.path.join(os.path.dirname(__file__), 'data',
                            'plugin_no_strings_po', 'plugin.py')
        with preserve_cwd(os.path.dirname(path)):
            plugin = Plugin(name, plugin_id, path)
        # Test loading from strings.xml
        self.assertEqual(plugin.addon.getLocalizedString(30100),
                         'View all results')

    def test_init_cli_mode_default_args(self):
        with preserve_cwd(
                os.path.join(os.path.dirname(__file__), 'data', 'plugin')):
            plugin = Plugin()

        self.assertEqual('plugin.video.academicearth', plugin.id)
        self.assertEqual(plugin.name, 'Academic Earth')
        self.assertTrue(os.path.isdir(plugin.storage_path))
        self.assertEqual(plugin.added_items, [])
        self.assertRaises(Exception, getattr, plugin, 'handle')
        self.assertRaises(Exception, getattr, plugin, 'request')

    def test_init_not_cli_mode(self):
        name = 'Hello Kodi'
        plugin_id = 'plugin.video.hellokodi'
        path = os.path.join(os.path.dirname(__file__), 'data', 'plugin',
                            'plugin.py')
        with preserve_cwd(os.path.dirname(path)):
            with preserve_cli_mode(cli_mode=False):
                plugin = Plugin(name, plugin_id, path)

        self.assertEqual(plugin_id, plugin.id)
        self.assertEqual(plugin.name, name)
        self.assertTrue(os.path.isdir(plugin.storage_path))
        self.assertEqual(plugin.added_items, [])
        self.assertRaises(Exception, getattr, plugin, 'handle')
        self.assertRaises(Exception, getattr, plugin, 'request')

    def test_init_not_cli_mode_default_args(self):
        with preserve_cli_mode(cli_mode=False):
            with preserve_cwd(
                    os.path.join(os.path.dirname(__file__), 'data', 'plugin')):
                plugin = Plugin()

        self.assertEqual('plugin.video.academicearth', plugin.id)
        self.assertEqual(plugin.name, 'Academic Earth')
        self.assertTrue(os.path.isdir(plugin.storage_path))
        self.assertEqual(plugin.added_items, [])
        self.assertRaises(Exception, getattr, plugin, 'handle')
        self.assertRaises(Exception, getattr, plugin, 'request')

    def test_info_types(self):
        name = 'Hello Kodi'
        path = __file__

        # can't parse from id, default to video
        with preserve_cli_mode(cli_mode=False):
            with preserve_cwd(
                    os.path.join(os.path.dirname(path), 'data', 'plugin')):
                plugin = Plugin(name, 'script.module.test', path)
                self.assertEqual(plugin.info_type, 'video')

                # parse from ID
                plugin = Plugin(name, 'plugin.audio.test')
                self.assertEqual(plugin.info_type, 'music')

                plugin = Plugin(name, 'plugin.video.test')
                self.assertEqual(plugin.info_type, 'video')

                plugin = Plugin(name, 'plugin.image.test')
                self.assertEqual(plugin.info_type, 'pictures')

                # info_type param should override value parsed from id
                plugin = Plugin(name, 'plugin.video.test', info_type='music')
                self.assertEqual(plugin.info_type, 'music')


class TestParseRequest(TestCase):
    def setUp(self):
        name = 'Hello Kodi'
        plugin_id = 'plugin.video.hellokodi'
        path = os.path.join(
            os.path.dirname(__file__), 'data', 'plugin', 'plugin.py')
        with preserve_cwd(os.path.dirname(path)):
            self.plugin = Plugin(name, plugin_id, path)

    def test_parse_request(self):
        with patch('kodiswift.plugin.Request') as MockRequest:
            sys.argv = ['plugin://plugin.video.hellokodi', '0', '?']
            self.plugin._parse_request()
            MockRequest.assert_called_with(
                'plugin://plugin.video.hellokodi?', '0')

    def test_parse_request_no_qs(self):
        with patch('kodiswift.plugin.Request') as MockRequest:
            sys.argv = ['plugin://plugin.video.hellokodi', '0']
            self.plugin._parse_request()
            MockRequest.assert_called_with(
                'plugin://plugin.video.hellokodi', '0')

    def test_parse_request_path_in_arg0(self):
        # Older versions of xbmc sometimes pass path in arg0
        with patch('kodiswift.plugin.Request') as MockRequest:
            sys.argv = [
                'plugin://plugin.video.hellokodi/videos/', '0', '?foo=bar']
            self.plugin._parse_request()
            MockRequest.assert_called_with(
                'plugin://plugin.video.hellokodi/videos/?foo=bar', '0')

    def test_parse_request_path_in_arg2(self):
        # Older versions of xbmc sometimes pass path in arg2
        with patch('kodiswift.plugin.Request') as MockRequest:
            sys.argv = [
                'plugin://plugin.video.hellokodi', '0', '/videos/?foo=bar']
            self.plugin._parse_request()
            MockRequest.assert_called_with(
                'plugin://plugin.video.hellokodi/videos/?foo=bar', '0')


def new_plugin():
    name = 'Hello Kodi'
    plugin_id = 'plugin.video.hellokodi'
    path = os.path.join(os.path.dirname(__file__), 'data', 'plugin',
                        'plugin.py')
    with preserve_cwd(os.path.dirname(path)):
        return Plugin(name, plugin_id, path)


def _test_plugin_runner(plugin):
    def run(relative_url, handle=0, qs='?'):
        url = 'plugin://%s%s' % (plugin.id, relative_url)
        sys.argv = [url, handle, qs]
        items = plugin.run()
        plugin._end_of_directory = False
        plugin.clear_added_items()
        return items

    return run


class TestBasicRouting(TestCase):
    def test_url_for_func(self):
        plugin = new_plugin()

        @plugin.route('/', name='another_name')
        def main_menu():
            return [{'label': 'Hello Kodi'}]

        self.assertEqual(plugin.url_for(main_menu),
                         'plugin://plugin.video.hellokodi/')
        self.assertEqual(plugin.url_for(main_menu, foo='bar'),
                         'plugin://plugin.video.hellokodi/?foo=bar')
        self.assertEqual(plugin.url_for(main_menu, foo=3),
                         'plugin://plugin.video.hellokodi/?foo=3')

    def test_url_for(self):
        plugin = new_plugin()

        @plugin.route('/')
        def main_menu():
            return [{'label': 'Hello Kodi'}]

        self.assertEqual(plugin.url_for('main_menu'),
                         'plugin://plugin.video.hellokodi/')
        self.assertEqual(plugin.url_for('main_menu', foo='bar'),
                         'plugin://plugin.video.hellokodi/?foo=bar')
        self.assertEqual(plugin.url_for('main_menu', foo=3),
                         'plugin://plugin.video.hellokodi/?foo=3')

    def test_url_for_multiple_routes(self):
        plugin = new_plugin()

        @plugin.route('/')
        @plugin.route('/videos/', name='videos')
        def main_menu():
            return [{'label': 'Hello Kodi'}]

        self.assertEqual(plugin.url_for('main_menu'),
                         'plugin://plugin.video.hellokodi/')
        self.assertEqual(plugin.url_for('main_menu', foo='bar'),
                         'plugin://plugin.video.hellokodi/?foo=bar')
        self.assertEqual(plugin.url_for('main_menu', foo=3),
                         'plugin://plugin.video.hellokodi/?foo=3')
        self.assertEqual(plugin.url_for('videos'),
                         'plugin://plugin.video.hellokodi/videos/')

    def test_options(self):
        plugin = new_plugin()

        @plugin.route('/person/<name>/', options={'name': 'dave'})
        def person(name):
            return [{'label': 'Hello %s' % name}]

        self.assertEqual(plugin.url_for('person', name='jon'),
                         'plugin://plugin.video.hellokodi/person/jon/')
        self.assertEqual(plugin.url_for('person'),
                         'plugin://plugin.video.hellokodi/person/dave/')

    def test_basic_routing(self):
        plugin = new_plugin()

        @plugin.route('/')
        def main_menu():
            return [{'label': 'Hello Kodi'}]

        with preserve_cli_mode(cli_mode=False):
            test_run = _test_plugin_runner(plugin)
            resp = test_run('/')
            self.assertEqual('Hello Kodi', resp[0].get_label())

    def test_options_routing(self):
        plugin = new_plugin()

        @plugin.route('/person/<name>/')
        @plugin.route('/')
        @plugin.route('/dave/', options={'name': 'dave'})
        def person(name='chris'):
            return [{'label': 'Hello %s' % name}]

        with preserve_cli_mode(cli_mode=False):
            test_run = _test_plugin_runner(plugin)
            resp = test_run('/person/jon/')
            self.assertEqual('Hello jon', resp[0].get_label())
            resp = test_run('/dave/')
            self.assertEqual('Hello dave', resp[0].get_label())
            resp = test_run('/')
            self.assertEqual('Hello chris', resp[0].get_label())

    def test_redirect(self):
        plugin = new_plugin()

        @plugin.route('/')
        def main_menu():
            url = plugin.url_for('videos')
            return plugin.redirect(url)

        @plugin.route('/videos/')
        def videos():
            return [{'label': 'Hello Videos'}]

        with preserve_cli_mode(cli_mode=False):
            test_run = _test_plugin_runner(plugin)
            resp = test_run('/')
            self.assertEqual('Hello Videos', resp[0].get_label())


class TestUnsyncedCaches(TestCase):
    def test_unsyced_caches(self):
        plugin = new_plugin()

        @plugin.route('/')
        def route_that_doesnt_call_finish():
            ppl = plugin.get_storage('people')
            ppl['foo'] = 'bar'

        sys.argv = ['plugin://plugin.video.hellokodi/', '1', '?']
        plugin.run()

        # ensure the cache is persisted to disk
        fn = os.path.join(plugin.storage_path, 'people')
        synced = pickle.load(open(fn, 'rb'))
        self.assertEqual(synced.keys(), ['foo'])

        # Since storage's store the timestamp as well, we just check our
        # actual value since we can't guess the timestamp
        self.assertEqual(synced['foo'][0], 'bar')


class TestResolvedUrl(TestCase):
    def test_url_was_resolved(self):
        plugin = new_plugin()

        @plugin.route('/play/<href>')
        def call_play_route(href):
            return plugin.set_resolved_url({
                'path': href + '.mkv',
                'is_playable': True,
            })

        sys.argv = ['plugin://plugin.video.hellokodi/', '1',
                    'play/http%3A%2F%2Fexample.org%2Fget%2F1']
        item = plugin.run()[0]

        # Check Wrapper ListItem
        self.assertEqual(item.path, 'http://example.org/get/1.mkv')
        self.assertEqual(item.playable, True)
        self.assertEqual(item.label, None)

        # Check Mock ListItem
        self.assertEqual(item.as_xbmc_listitem().path,
                         'http://example.org/get/1.mkv')
        self.assertEqual(item.as_xbmc_listitem().getLabel(), None)
        self.assertEqual(item.as_xbmc_listitem().getProperty('isPlayable'),
                         'true')
