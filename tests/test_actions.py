# -*- coding: utf-8 -*-
import unittest

from kodiswift.actions import background, update_view


class TestActions(unittest.TestCase):
    def test_background(self):
        expected = 'RunPlugin(plugin://plugin.video.hellokodi/script.py)'
        actual = background('plugin://plugin.video.hellokodi/script.py')
        self.assertEqual(actual, expected)

    def test_update_view(self):
        expected = 'Container.Update(plugin://plugin.video.hellokodi)'
        actual = update_view('plugin://plugin.video.hellokodi')
        self.assertEqual(actual, expected)
