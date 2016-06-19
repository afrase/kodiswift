# -*- coding: utf-8 -*-
import os
import tempfile
import unittest

from mock import Mock, patch, call

import kodiswift
from kodiswift import SortMethod
from kodiswift import xbmc
from kodiswift.listitem import ListItem
from kodiswift.xbmcmixin import XBMCMixin


class TestMixedIn(XBMCMixin):
    storage_path = '/tmp/cache'
    if not os.path.isdir(storage_path):
        os.mkdir(storage_path)
    # TODO: use a mock with return values here
    # addon = Plugin('plugin.video.helloxbmc')
    addon = Mock()
    added_items = []
    handle = 0
    _end_of_directory = False


class MixedIn(XBMCMixin):
    storage_path = '/tmp'

    def __init__(self, **kwargs):
        for attr_name, attr_value in kwargs.items():
            setattr(self, attr_name, attr_value)


# noinspection PyUnresolvedReferences
class TestXBMCMixin(unittest.TestCase):
    def setUp(self):
        self.m = TestMixedIn()

    def test_get_storage(self):
        cache = self.m.get_storage('animals')
        cache['dog'] = 'woof'
        cache.close()
        cache = self.m.get_storage('animals')
        self.assertEqual(cache['dog'], 'woof')

    def test_get_string(self):
        self.m.addon.getLocalizedString.return_value = 'Hello Kodi'
        self.assertEqual('Hello Kodi', self.m.get_string('30000'))
        # check if the string comes from cache
        self.m.addon.getLocalizedString.return_value = ''
        self.assertEqual('Hello Kodi', self.m.get_string('30000'))
        # check if retrieval by int and str returns same (and comes from cache)
        self.assertEqual('Hello Kodi', self.m.get_string(30000))

    @patch('kodiswift.xbmcplugin')
    def test_set_content(self, mock_xbmcplugin):
        self.m.set_content('movies')
        self.assertTrue(mock_xbmcplugin.setContent.called_with(0, 'movies'))

    def test_get_setting(self):
        self.m.get_setting('username')
        self.assertTrue(self.m.addon.getSetting.called_with(key='username'))
        # Test int
        self.m.addon.getSetting.return_value = '3'
        self.assertEqual(self.m.get_setting('int'), '3')
        self.assertEqual(self.m.get_setting('int', int), 3)
        # Test bool
        self.m.addon.getSetting.return_value = 'true'
        self.assertEqual(self.m.get_setting('bool'), 'true')
        self.assertEqual(self.m.get_setting('bool', bool), True)
        self.m.addon.getSetting.return_value = 'false'
        self.assertEqual(self.m.get_setting('bool'), 'false')
        self.assertEqual(self.m.get_setting('bool', bool), False)
        # Test unicode
        self.m.addon.getSetting.return_value = 'd\xc3\xb6ner'
        self.assertEqual(self.m.get_setting('unicode'), 'd\xc3\xb6ner')
        self.assertEqual(self.m.get_setting('unicode', unicode), u'd\xf6ner')
        # Test list
        self.m.addon.getSetting.return_value = '2'
        lst = ('1', 2, True, False)
        self.assertEqual(self.m.get_setting('list'), '2')
        self.assertEqual(self.m.get_setting('list', choices=lst), lst[2])

    def test_set_setting(self):
        self.m.set_setting('username', 'xbmc')
        self.assertTrue(
            self.m.addon.setSetting.called_with(key='username', value='xbmc'))

    def test_open_settings(self):
        self.m.open_settings()
        self.assertTrue(self.m.addon.openSettings.called)

    def test_set_resolved_url(self):
        url = 'http://www.example.com/video.mp4'
        ret = self.m.set_resolved_url(url)
        item = ret[0]
        self.assertIsInstance(item, kodiswift.ListItem)
        self.assertTrue(item.played)

    def test_set_resolved_url2(self):
        item = {'path': 'http://www.example.com/video.mp4'}
        ret = self.m.set_resolved_url(item=item)
        item = ret[0]
        self.assertIsInstance(item, kodiswift.ListItem)
        self.assertTrue(item.played)

    @patch.object(xbmc, 'Player')
    @patch('kodiswift.ListItem', wraps=kodiswift.ListItem)
    def test_play_video_dict(self, wrapped_list_item, mock_player):
        plugin = MixedIn(
            storage_path=tempfile.mkdtemp(), addon=Mock(), added_items=[],
            request=Mock(), info_type='pictures', handle=0)

        item = {'label': 'The Ultimate Showdown',
                'path': 'http://example.com/video.mp4'}
        returned = plugin.play_video(item)
        returned_item = returned[0]
        self.assertTrue(returned_item.get_played())

        wrapped_list_item.from_dict.assert_called_with(
            label='The Ultimate Showdown', info_type='video',
            path='http://example.com/video.mp4')
        self.assertTrue(mock_player().play.called)

        # Check that the second arg to play was an instance of xbmc listitem
        # and not kodiswift.ListItem
        item_arg = mock_player().play.call_args[0][1]
        self.assertTrue(isinstance(item_arg, kodiswift.xbmcgui.ListItem))

    @patch('kodiswift.xbmcplugin.addSortMethod')
    def test_add_sort_method(self, add_sort_method):
        plugin = TestMixedIn()

        known_values = [
            # can specify by string
            (('title', None), (0, 9)),
            (('TiTLe', None), (0, 9)),
            # can specify as an attr on the SortMethod class
            ((SortMethod.TITLE, None), (0, 9)),
            (('date', '%D'), (0, 3, '%D')),
            # can specify with the actual int value
            ((3, '%D'), (0, 3, '%D')),
        ]

        for args, call_args_to_verify in known_values:
            plugin.add_sort_method(*args)
            add_sort_method.assert_called_with(*call_args_to_verify)

    @patch('kodiswift.xbmcplugin.addSortMethod')
    def test_finish(self, mock_add_sort_method):
        # TODO: Add more asserts to this test
        items = [
            {'label': 'Foo', 'path': 'http://example.com/foo'},
            {'label': 'Bar', 'path': 'http://example.com/bar'},
        ]
        plugin = TestMixedIn()
        plugin.finish(items, sort_methods=['title', ('dAte', '%D'), 'label',
                                           'mpaa_rating', SortMethod.SIZE])
        calls = [
            call(0, 9),
            call(0, 3, '%D'),
            call(0, 1),
            call(0, 28),
            call(0, 4),
        ]
        mock_add_sort_method.assert_has_calls(calls)

    @patch('kodiswift.xbmc.executebuiltin')
    def test_notify_default_name(self, mock_executebuiltin):
        plugin = TestMixedIn()
        with patch.object(plugin.addon, 'getAddonInfo',
                          return_value='Academic Earth'):
            plugin.notify('Hello World!')
        mock_executebuiltin.assert_called_with(
            'Kodi.Notification("Hello World!", "Academic Earth", "5000", "")'
        )

    @patch('kodiswift.xbmc.executebuiltin')
    def test_notify(self, mock_executebuiltin):
        plugin = TestMixedIn()
        with patch.object(plugin.addon, 'getAddonInfo',
                          return_value='Academic Earth'):
            plugin.notify('Hello World!', 'My Title', 3000,
                          'http://example.com/image.png')
        mock_executebuiltin.assert_called_with(
            'Kodi.Notification("Hello World!", "My Title", "3000", '
            '"http://example.com/image.png")')

    @patch('kodiswift.xbmc.Keyboard')
    def test_keyboard(self, mock_keyboard):
        plugin = TestMixedIn()
        with patch.object(plugin.addon,
                          'getAddonInfo', return_value='Academic Earth'):
            plugin.keyboard()
        mock_keyboard.assert_called_with('', 'Academic Earth', False)

    def test_clear_function_cache(self):
        plugin = MixedIn(
            storage_path=tempfile.mkdtemp(), addon=Mock(), added_items=[],
            request=Mock(), info_type='pictures', handle=0)

        @plugin.cached()
        def echo(msg):
            return msg

        echo('hello')

        # cache should now contain 1 item
        storage = plugin.get_storage('.functions')
        self.assertEqual(len(storage.items()), 1)
        plugin.clear_function_cache()
        self.assertEqual(len(storage.items()), 0)


class TestAddItems(unittest.TestCase):
    @patch('kodiswift.ListItem.from_dict')
    @patch('kodiswift.xbmcplugin.addDirectoryItems')
    def test_add_items(self, add_dir_items, from_dict):
        plugin = MixedIn(storage_path=tempfile.mkdtemp(), addon=Mock(),
                         added_items=[], request=Mock(), info_type='pictures',
                         handle=0)
        items = [
            {'label': 'Course 1', 'path': 'plugin.image.test/foo'},
            {'label': 'Course 2', 'path': 'plugin.image.test/bar'},
        ]
        plugin.add_items(items)

        # TODO: Assert actual arguments passed to the addDirectoryItems call
        self.assertTrue(add_dir_items.called)
        calls = [
            call(label='Course 1', path='plugin.image.test/foo',
                 info_type='pictures'),
            call(label='Course 2', path='plugin.image.test/bar',
                 info_type='pictures'),
        ]
        from_dict.assert_has_calls(calls)

        # TODO: Currently ListItems don't implement __eq__
        # list_items = [ListItem.from_dict(**item) for item in items]
        # self.assertEqual(returned, list_items)

    @patch('kodiswift.ListItem.from_dict')
    @patch('kodiswift.xbmcplugin.addDirectoryItems')
    def test_add_items_no_info_type(self, add_directory_items, from_dict):
        plugin = MixedIn(storage_path=tempfile.mkdtemp(), addon=Mock(),
                         added_items=[], request=Mock(), handle=0)
        items = [
            {'label': 'Course 1', 'path': 'plugin.image.test/foo'}
        ]
        results = plugin.add_items(items)

        self.assertTrue(add_directory_items.called)
        calls = [
            call(label='Course 1', path='plugin.image.test/foo',
                 info_type='video'),
        ]
        from_dict.assert_has_calls(calls)

        list_items = [ListItem.from_dict(**item) for item in items]
        self.assertEqual(results, list_items)

    @patch('kodiswift.ListItem.from_dict')
    @patch('kodiswift.xbmcplugin.addDirectoryItems')
    def test_add_items_item_specific_info_type(self, add_directory_items,
                                               from_dict):
        plugin = MixedIn(
            storage_path=tempfile.mkdtemp(), addon=Mock(), added_items=[],
            request=Mock(), handle=0, info_type='pictures')
        items = [
            {'label': 'Course 1', 'path': 'plugin.image.test/foo',
             'info_type': 'music'}
        ]
        results = plugin.add_items(items)

        self.assertTrue(add_directory_items.called)
        calls = [
            call(label='Course 1', path='plugin.image.test/foo',
                 info_type='music'),
        ]
        from_dict.assert_has_calls(calls)

        list_items = [ListItem.from_dict(**item) for item in items]
        self.assertEqual(results, list_items)


class TestAddToPlaylist(unittest.TestCase):
    def setUp(self):
        with patch('kodiswift.xbmc.Playlist') as playlist:
            self.m = TestMixedIn()
            # Mock some things so we can verify what was called
            mock_playlist = Mock()
            playlist.return_value = mock_playlist
            self.mock_playlist = playlist

    def test_args(self):
        # Verify playlists
        self.assertRaises(
            ValueError, self.m.add_to_playlist, [], 'invalid_playlist')

        # Verify video and music work
        self.m.add_to_playlist([])
        self.m.add_to_playlist([], 'video')
        self.m.add_to_playlist([], 'music')

    @patch('kodiswift.ListItem', wraps=ListItem)
    def test_return_values(self, mock_list_item):
        # Verify dicts are transformed into listitems
        dict_items = [
            {'label': 'Grape Stomp'},
            {'label': 'Boom Goes the Dynamite'},
        ]
        self.m.add_to_playlist(dict_items)

        # Verify from_dict was called properly, defaults to info_type=video
        calls = [
            call(label='Grape Stomp', info_type='video'),
            call(label='Boom Goes the Dynamite', info_type='video'),
        ]
        self.assertEqual(mock_list_item.from_dict.call_args_list, calls)

        # Verify with playlist=music
        mock_list_item.from_dict.reset_mock()

        dict_items = [
            {'label': 'Grape Stomp'},
            {'label': 'Boom Goes the Dynamite'},
        ]
        self.m.add_to_playlist(dict_items, 'music')

        # Verify from_dict was called properly, defaults to info_type=video
        calls = [
            call(label='Grape Stomp', info_type='music'),
            call(label='Boom Goes the Dynamite', info_type='music'),
        ]
        self.assertEqual(mock_list_item.from_dict.call_args_list, calls)

        # Verify an item's info_dict key is not used
        mock_list_item.from_dict.reset_mock()

        dict_items = [
            {'label': 'Grape Stomp', 'info_type': 'music'},
            {'label': 'Boom Goes the Dynamite', 'info_type': 'music'},
        ]
        items = self.m.add_to_playlist(dict_items, 'video')

        # Verify from_dict was called properly, defaults to info_type=video
        calls = [
            call(label='Grape Stomp', info_type='video'),
            call(label='Boom Goes the Dynamite', info_type='video'),
        ]
        self.assertEqual(mock_list_item.from_dict.call_args_list, calls)

        # verify ListItems were created correctly
        for item, returned_item in zip(dict_items, items):
            assert isinstance(returned_item, ListItem)
            self.assertEqual(item['label'], returned_item.label)

        # Verify listitems are unchanged
        mock_list_item.from_dict.reset_mock()

        listitems = [
            ListItem('Grape Stomp'),
            ListItem('Boom Goes the Dyanmite'),
        ]
        items = self.m.add_to_playlist(listitems)

        self.assertFalse(mock_list_item.from_dict.called)
        for item, returned_item in zip(listitems, items):
            self.assertEqual(item, returned_item)

        # Verify mixed lists
        # Verify listitems are unchange
        listitems = [
            ListItem('Grape Stomp'),
            {'label': 'Boom Goes the Dynamite'},
        ]
        items = self.m.add_to_playlist(listitems)
        for item, returned_item in zip(listitems, items):
            assert isinstance(returned_item, ListItem)

    def test_added_to_playlist(self):
        list_items = [
            ListItem('Grape Stomp'),
            ListItem('Boom Goes the Dynamite'),
        ]
        items = self.m.add_to_playlist(list_items)
        for item, call_args in zip(items,
                                   self.mock_playlist.add.call_args_list):
            self.assertEqual(
                (item.get_path(), item.as_xbmc_listitem(), 0), call_args)

    def test_set_view_mode(self):
        with patch('kodiswift.xbmcmixin.xbmc') as _xbmc:
            self.m.set_view_mode(500)
            _xbmc.executebuiltin.assert_called_with(
                'Container.SetViewMode(500)')
