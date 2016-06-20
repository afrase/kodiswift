# -*- coding: utf-8 -*-
import unittest

from kodiswift.common import kodi_url, clean_dict, pickle_dict, unpickle_dict


class TestXBMCUrl(unittest.TestCase):
    def test_xbmc_url(self):
        known_values = (
            # url, options_dict, expected_value
            ('url', {}, 'url'),
            ('url', {'key': 'val'}, 'url|key=val'),
            ('url', {'key': 3}, 'url|key=3'),
            ('url', {'a': 'b', 'c': 'd'}, 'url|a=b&c=d'),
            ('url', {'symbol': '=', 'c': 'd'}, 'url|symbol=%3D&c=d'),
        )
        for url, options, expected in known_values:
            self.assertEqual(expected, kodi_url(url, **options))


class TestCleanDict(unittest.TestCase):
    def test_clean_dict(self):
        items = {'foo': 'foo', 'bar': None, 'baz': False, 'age': 0}
        expected = {'foo': 'foo', 'baz': False, 'age': 0}
        self.assertEqual(expected, clean_dict(items))


class TestPickleDict(unittest.TestCase):
    def test_pickle_dict(self):
        items = {
            'name': u'jon',
            'animal': 'dog',
            'boolean': True,
            'number': 42,
            'list': ['a', 'b'],
            'dict': {'foo': 'bar'},
        }
        pickled = pickle_dict(items)
        expected = (
            ('name', u'jon'),
            ('animal', 'dog'),
            ('boolean', 'I01\n.'),
            ('number', 'I42\n.'),
            ('list', "(lp1\nS'a'\naS'b'\na.",),
            ('dict', "(dp1\nS'foo'\np2\nS'bar'\np3\ns."),
        )

        self.assertEqual(len(pickled.items()), 7)
        for key, val in expected:
            self.assertEqual(pickled.get(key), val)
        fields = pickled.get('_pickled').split(',')
        self.assertEqual(sorted(fields), ['boolean', 'dict', 'list', 'number'])
        self.assertEqual(unpickle_dict(pickled), items)
        self.assertEqual(unpickle_dict(pickle_dict(items)), items)


class TestDownloadPage(unittest.TestCase):
    def test_download_page(self):
        pass
