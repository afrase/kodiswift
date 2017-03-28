# -*- coding: utf-8 -*-
import unittest
from mock import patch
import StringIO
from kodiswift.cli import console
from kodiswift.listitem import ListItem


class TestConsole(unittest.TestCase):
    def test_get_max_len(self):
        items = ['a', 'bb', 'ccc', 'dddd']
        self.assertEqual(console.get_max_len(items), 4)
        self.assertEqual(console.get_max_len([]), 0)

    def test_display_video(self):
        items = [
            {'label': 'X', 'path': 'Y'},
            {'label': 'Z', 'path': 'Q'}
        ]
        list_items = [ListItem.from_dict(**item) for item in items]

        with patch('sys.stdout', new=StringIO.StringIO()) as stdout:
            console.display_video(list_items)

        output = stdout.getvalue().strip()
        self.assertEquals(output, '-------------------\n'
                                  'Playing Media Z (Q)\n'
                                  '-------------------\n'
                                  '[0] X (Y)')

    def test_display_video_form_listitems(self):
        items = [
            {'label': '..', 'path': 'Y'},
            {'label': 'Z', 'path': 'Q', 'played': True}
        ]
        list_items = [ListItem.from_dict(**item) for item in items]
        list_items[1].set_played(True)

        with patch('sys.stdout', new=StringIO.StringIO()) as stdout:
            console.display_listitems(list_items, "PARENT_URL")

        output = stdout.getvalue().strip()
        self.assertEquals(output, '-------------------\n'
                                  'Playing Media Z (Q)\n'
                                  '-------------------\n'
                                  '[0] .. (Y)')

    def test_display_listitems_with_single_item(self):
        items = [
            {'label': '..', 'path': 'Y'},
            {'label': 'Z', 'path': 'Q'}
        ]
        list_items = [ListItem.from_dict(**item) for item in items]

        with patch('sys.stdout', new=StringIO.StringIO()) as stdout:
            console.display_listitems(list_items, 'PARENT_URL')

        output = stdout.getvalue().strip()
        self.assertEquals(output, '==========\n'
                                  'Current URL: PARENT_URL\n'
                                  '----------\n'
                                  ' #  Label Path\n'
                                  '----------\n'
                                  '[0] .. (Y)\n'
                                  '[1] Z  (Q)\n'
                                  '----------')

    def test_display_listitems_with_multiple_items(self):
        items = [
            {'label': 'A_LABEL', 'path': 'A_PATH'},
            {'label': 'B_LABEL', 'path': 'B_PATH'},
            {'label': 'C_LABEL', 'path': 'C_PATH'}
        ]
        list_items = [ListItem.from_dict(**item) for item in items]

        with patch('sys.stdout', new=StringIO.StringIO()) as stdout:
            console.display_listitems(list_items, 'PARENT_URL')

        output = stdout.getvalue().strip()
        self.assertEquals(output, '====================\n'
                                  'Current URL: PARENT_URL\n'
                                  '--------------------\n'
                                  ' #  Label   Path\n'
                                  '--------------------\n'
                                  '[0] A_LABEL (A_PATH)\n'
                                  '[1] B_LABEL (B_PATH)\n'
                                  '[2] C_LABEL (C_PATH)\n'
                                  '--------------------')
