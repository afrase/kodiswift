# -*- coding: utf-8 -*-
import tempfile
import unittest

from kodiswift.cli import create


class TestCreate(unittest.TestCase):
    def test_update_regular_file(self):
        file_obj, filename = tempfile.mkstemp(suffix='.py', text=True)
        with open(filename, 'w') as file_obj:
            file_obj.write(
                'This is a test of the emergency {broadcast} system.')

        create.update_file(filename, {'broadcast': 'kitten'})

        with open(filename, 'r') as file_obj:
            result = file_obj.read()
        self.assertEqual('This is a test of the emergency kitten system.',
                         result)

    def test_update_xml_file(self):
        file_obj, filename = tempfile.mkstemp(suffix='addon.xml', text=True)
        with open(filename, 'w') as file_obj:
            file_obj.write('<tag provider={provider}/>')

        create.update_file(filename, {
            'provider': 'name aka "another name" <name@domain.com> \'foo\''})

        with open(filename, 'r') as file_obj:
            result = file_obj.read()

        expected = ('<tag provider="name aka &quot;another name&quot; '
                    '&lt;name@domain.com&gt; \'foo\'"/>')
        self.assertEqual(expected, result)
