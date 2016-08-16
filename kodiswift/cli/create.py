# -*- coding: utf-8 -*-
"""
kodiswift.cli.create
---------------------

This module contains the code to initialize a new Kodi addon project.

:copyright: (c) 2012 by Jonathan Beluch
:license: GPLv3, see LICENSE for more details.
"""
from __future__ import print_function, absolute_import

import os
import shutil
from xml.sax import saxutils


def update_file(filename, items):
    """Edits the given file in place, replacing any instances of {key} with the
    appropriate value from the provided items dict. If the given filename ends
    with ".xml" values will be quoted and escaped for XML.
    """
    should_escape = filename.endswith('addon.xml')

    with open(filename, 'r') as inp:
        text = inp.read()

    for key, val in items.items():
        if should_escape:
            val = saxutils.quoteattr(str(val))
        text = text.replace('{%s}' % key, str(val))
    output = text

    with open(filename, 'w') as out:
        out.write(output)


def create_new_project(args):
    template_dir = os.path.join(os.path.dirname(__file__), 'data')
    plugin_dir = os.path.join(args.project_dir, args.plugin_id)
    shutil.copytree(template_dir, plugin_dir,
                    ignore=shutil.ignore_patterns('*.pyc'))

    for root, _, files in os.walk(plugin_dir):
        for filename in files:
            update_file(os.path.join(root, filename), vars(args))

    print('Projects successfully created in %s.' % plugin_dir)
