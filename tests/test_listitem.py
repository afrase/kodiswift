# -*- coding: utf-8 -*-
import unittest

import mock

from kodiswift import ListItem, xbmcgui


class TestListItem(unittest.TestCase):
    def setUp(self):
        self.listitem = ListItem('label', 'label2', 'icon', 'thumbnail', 'path')

    def test_init(self):
        li = self.listitem
        self.assertEqual(li.label, 'label')
        self.assertEqual(li.label2, 'label2')
        self.assertEqual(li.icon, 'icon')
        self.assertEqual(li.thumbnail, 'thumbnail')
        self.assertEqual(li.path, 'path')

    def test_label(self):
        item = ListItem('foo')
        self.assertEqual(item.label, 'foo')
        item.label = 'bar'
        self.assertEqual(item.label, 'bar')
        item.set_label('baz')
        self.assertEqual(item.get_label(), 'baz')

    def test_label2(self):
        item = ListItem('foo')
        self.assertIsNone(item.label2)
        item.label2 = 'bar'
        self.assertEqual(item.label2, 'bar')
        item.set_label2('baz')
        self.assertEqual(item.get_label2(), 'baz')

    def test_icon(self):
        item = ListItem()
        self.assertIsNone(item.icon)

        item.icon = 'bar'
        self.assertEqual(item.icon, 'bar')
        self.assertEqual(item.get_icon(), 'bar')

        item.set_icon('baz')
        self.assertEqual(item.icon, 'baz')
        self.assertEqual(item.get_icon(), 'baz')

    def test_thumbnail(self):
        item = ListItem()
        self.assertIsNone(item.thumbnail)

        item.thumbnail = 'bar'
        self.assertEqual(item.thumbnail, 'bar')
        self.assertEqual(item.get_thumbnail(), 'bar')

        item.set_thumbnail('baz')
        self.assertEqual(item.thumbnail, 'baz')
        self.assertEqual(item.get_thumbnail(), 'baz')

    def test_path(self):
        item = ListItem()
        self.assertIsNone(item.path)

        item.path = 'bar'
        self.assertEqual(item.path, 'bar')
        self.assertEqual(item.get_path(), 'bar')

        item.set_path('baz')
        self.assertEqual(item.path, 'baz')
        self.assertEqual(item.get_path(), 'baz')

    def test_poster(self):
        item = ListItem()
        self.assertIsNone(item.poster)

        item.poster = 'bar'
        self.assertEqual(item.poster, 'bar')
        item.poster = 'baz'
        self.assertEqual(item.poster, 'baz')

    def test_played(self):
        item = ListItem()
        self.assertEqual(item.played, False)

        item.played = True
        self.assertEqual(item.played, True)
        item.played = False
        self.assertEqual(item.played, False)

    def test_art(self):
        item = ListItem()
        art = {'thumb': None, 'icon': None}
        self.assertEqual(item.art, art)

        art2 = {'thumb': 'something', 'icon': 'else'}
        item.art = art2
        self.assertEqual(item.art, art2)

        item.set_art(art)
        self.assertEqual(item.art, art)


    def test_context_menu(self):
        menu_items = [('label1', 'foo'), ('label2', 'bar')]
        item = ListItem()
        item.add_context_menu_items(menu_items)
        self.assertEqual(item.get_context_menu_items(), menu_items)

        extra_menu_item = ('label3', 'baz')
        menu_items.append(extra_menu_item)
        item.add_context_menu_items([extra_menu_item])
        self.assertEqual(item.get_context_menu_items(), menu_items)

        # Verify replace_items branch gets executed and works.
        item.add_context_menu_items([extra_menu_item], True)
        self.assertEqual(item.get_context_menu_items(), [extra_menu_item])

    def test_set_info(self):
        # noinspection PyUnresolvedReferences
        with mock.patch.object(xbmcgui.ListItem,
                               'setInfo') as mock_setInfo:
            item = ListItem()
            item.set_info('video', {'title': '300'})
        mock_setInfo.assert_called_with('video', {'title': '300'})

    def test_stream_info(self):
        # noinspection PyUnresolvedReferences
        with mock.patch.object(xbmcgui.ListItem,
                               'addStreamInfo') as mock_stream_info:
            item = ListItem()
            item.add_stream_info('video', {'duration': 185})
            mock_stream_info.assert_called_with('video', {'duration': 185})
            item.add_stream_info('audio', {'language': 'en'})
            mock_stream_info.assert_called_with('audio', {'language': 'en'})

    def test_selected(self):
        item = ListItem()
        self.assertEqual(item.selected, False)
        self.assertEqual(item.is_selected(), False)

        item.selected = True
        self.assertEqual(item.selected, True)
        self.assertEqual(item.is_selected(), True)

        item.select(False)
        self.assertEqual(item.selected, False)
        self.assertEqual(item.is_selected(), False)

    def test_select_getter(self):
        # noinspection PyUnresolvedReferences
        with mock.patch.object(xbmcgui.ListItem, 'isSelected') as mock_selected:
            mock_selected.return_value = False
            item = ListItem()
            self.assertEqual(item.selected, False)
        mock_selected.assert_called_with()

    def test_select_setter(self):
        # noinspection PyUnresolvedReferences
        with mock.patch.object(xbmcgui.ListItem, 'select') as mock_select:
            item = ListItem()
            item.selected = True
            mock_select.assert_called_with(True)
            item.selected = False
            mock_select.assert_called_with(False)

    def test_select(self):
        # noinspection PyUnresolvedReferences
        with mock.patch.object(xbmcgui.ListItem, 'select') as mock_select:
            item = ListItem()
            item.selected = True
            mock_select.assert_called_with(True)
            item.select(False)
            mock_select.assert_called_with(False)

    def test_is_selected(self):
        # noinspection PyUnresolvedReferences
        with mock.patch.object(xbmcgui.ListItem, 'isSelected') as mock_selected:
            mock_selected.return_value = False
            item = ListItem()
            self.assertEqual(item.is_selected(), False)
        mock_selected.assert_called_with()

    @mock.patch('kodiswift.xbmcgui.ListItem.getProperty')
    def test_get_property(self, mock_get_property):
        mock_get_property.return_value = 'bar'
        item = ListItem()
        self.assertEqual(item.get_property('foo'), 'bar')
        mock_get_property.assert_called_with('foo')

    @mock.patch('kodiswift.xbmcgui.ListItem.setProperty')
    def test_set_property(self, mock_set_property):
        item = ListItem()
        item.set_property('foo', 'bar')
        mock_set_property.assert_called_with('foo', 'bar')

    def test_as_tuple(self):
        item = ListItem()
        self.assertEqual(item.as_tuple(), (None, item._listitem, True))


    def test___str__(self):
        item = ListItem()
        item.path = "somePath"
        item.label = "sameLabel"
        self.assertEqual(item.__str__(), u"sameLabel (somePath)")
        self.assertEqual(str(item), u"sameLabel (somePath)")

class TestListItemAsserts(unittest.TestCase):
    def test_non_basestring_key(self):
        item = ListItem()
        self.assertRaises(AssertionError, item.add_context_menu_items,
                          [(42, 'action')])
        self.assertRaises(AssertionError, item.add_context_menu_items,
                          [(None, 'action')])

    def test_non_basestring_val(self):
        item = ListItem()
        self.assertRaises(AssertionError, item.add_context_menu_items,
                          [('label', 42)])
        self.assertRaises(AssertionError, item.add_context_menu_items,
                          [('label', None)])


class TestFromDict(unittest.TestCase):
    def test_from_dict_props(self):
        dct = {
            'properties': {'StartOffset': '256.4'},
        }
        item = ListItem.from_dict(**dct)
        self.assertEqual(item.get_property('StartOffset'), '256.4')

        dct = {
            'properties': [('StartOffset', '256.4')],
        }
        item = ListItem.from_dict(**dct)
        self.assertEqual(item.get_property('StartOffset'), '256.4')

    def test_from_dict(self):
        dct = {
            'label': 'foo',
            'label2': 'bar',
            'icon': 'icon',
            'thumbnail': 'thumbnail',
            'path': 'plugin://my.plugin.id/',
            'selected': True,
            'info': {'title': 'My title'},
            'info_type': 'pictures',
            'properties': [('StartOffset', '256.4')],
            'stream_info': {
                'video': {'duration': 185}
            },
            'context_menu': [('label', 'action')],
            'is_playable': True}

        # noinspection PyUnresolvedReferences
        with mock.patch.object(ListItem, 'set_info',
                               spec=False) as mock_set_info:
            # noinspection PyUnresolvedReferences
            with mock.patch.object(ListItem, 'add_stream_info',
                                   spec=False) as mock_set_stream:
                item = ListItem.from_dict(**dct)

        self.assertEqual(item.label, 'foo')
        self.assertEqual(item.label2, 'bar')
        self.assertEqual(item.icon, 'icon')
        self.assertEqual(item.thumbnail, 'thumbnail')
        self.assertEqual(item.path, 'plugin://my.plugin.id/')
        self.assertEqual(item.selected, True)
        mock_set_info.assert_called_with('pictures', {'title': 'My title'})
        mock_set_stream.assert_called_with('video', {'duration': 185})
        self.assertEqual(item.get_property('StartOffset'), '256.4')
        self.assertEqual(item.get_context_menu_items(), [('label', 'action')])
        self.assertEqual(item.get_property('isPlayable'), 'true')
        self.assertEqual(item.playable, True)
        self.assertEqual(item.is_folder, True)

    def test_from_dict_info_default_info_type(self):
        dct = {'info': {'title': 'My title'}}
        # noinspection PyUnresolvedReferences
        with mock.patch.object(ListItem, 'set_info',
                               spec=False) as mock_set_info:
            _ = ListItem.from_dict(**dct)
        mock_set_info.assert_called_with('video', {'title': 'My title'})
