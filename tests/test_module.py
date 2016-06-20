# -*- coding: utf-8 -*-
import os
import sys
import unittest

from kodiswift import Module, Plugin, NotFoundException
from utils import preserve_cwd


def create_plugin_module():
    module = Module('namespace')
    sys.argv = ['./plugin.py']
    path = os.path.join(os.path.dirname(__file__), 'data', 'plugin', 'plugin.py')
    with preserve_cwd(os.path.dirname(path)):
        plugin = Plugin('Hello Kodi', 'plugin.video.helloxbmc', path)
    return plugin, module


class TestModule(unittest.TestCase):
    def test_init(self):
        module = Module('my.module.namespace')
        self.assertEqual('namespace', module._namespace)
        # Test that properties raise an Exception when a module isn't registered
        self.assertRaises(RuntimeError, getattr, module, 'plugin')
        self.assertRaises(RuntimeError, getattr, module, 'cache_path')
        self.assertRaises(RuntimeError, getattr, module, 'addon')
        self.assertRaises(RuntimeError, getattr, module, 'added_items')
        self.assertRaises(RuntimeError, getattr, module, 'handle')
        self.assertRaises(RuntimeError, getattr, module, 'request')
        self.assertRaises(RuntimeError, getattr, module, 'url_prefix')

    def test_properties_after_registration(self):
        plugin, module = create_plugin_module()
        plugin.register_module(module, 'module/')
        self.assertEqual(module.plugin, plugin)
        self.assertEqual(module.addon, plugin.addon)
        self.assertEqual(module.added_items, plugin.added_items)

        # no request registered yet
        self.assertRaises(Exception, getattr, module, 'handle')
        self.assertRaises(Exception, getattr, module, 'request')
        self.assertEqual(module.url_prefix, 'module/')


class TestRoute(unittest.TestCase):
    def test_route(self):
        plugin, module = create_plugin_module()

        @module.route('/')
        @module.route('/videos', 'show_videos', {'video_id': 42})
        @module.route('/video/<video_id>', name='show_video')
        def view(video_id=None):
            return video_id

        plugin.register_module(module, '/module')
        self.assertEqual(plugin.url_for('namespace.view'),
                         'plugin://plugin.video.helloxbmc/module/')
        self.assertEqual(module.url_for('namespace.view'),
                         'plugin://plugin.video.helloxbmc/module/')
        self.assertEqual(module.url_for('view'),
                         'plugin://plugin.video.helloxbmc/module/')
        self.assertRaises(NotFoundException, module.url_for, 'view',
                          explicit=True)
        self.assertRaises(NotFoundException, plugin.url_for, 'view')

        self.assertEqual(plugin.url_for('namespace.show_videos'),
                         'plugin://plugin.video.helloxbmc/module/videos')
        self.assertEqual(module.url_for('namespace.show_videos'),
                         'plugin://plugin.video.helloxbmc/module/videos')
        self.assertEqual(module.url_for('show_videos'),
                         'plugin://plugin.video.helloxbmc/module/videos')
        self.assertRaises(NotFoundException, module.url_for, 'show_videos',
                          explicit=True)
        self.assertRaises(NotFoundException, plugin.url_for, 'show_videos')

        self.assertRaises(KeyError, plugin.url_for, 'namespace.show_video')
        self.assertEqual(plugin.url_for('namespace.show_video', video_id='42'),
                         'plugin://plugin.video.helloxbmc/module/video/42')

    def test_named_routes(self):
        plugin, module = create_plugin_module()

        @module.route('/foo', 'foo')
        @module.route('/bar', 'bar')
        def view(video_id=None):
            return video_id

        plugin.register_module(module, '/module')

        self.assertRaises(NotFoundException, module.url_for, 'view',
                          explicit=True)
        self.assertRaises(NotFoundException, plugin.url_for, 'view')
