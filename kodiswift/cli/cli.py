# -*- coding: utf-8 -*-
"""
kodiswift.cli.cli
------------------

The main entry point for the kodiswift console script. CLI commands can be
registered in this module.

:copyright: (c) 2012 by Jonathan Beluch
:license: GPLv3, see LICENSE for more details.
"""
from __future__ import absolute_import

import os
import argparse
import string

_sentinel = '==DEFAULT=='


class InteractiveAction(argparse.Action):
    def __init__(self, **kwargs):
        super(InteractiveAction, self).__init__(default=_sentinel, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


class InteractiveType(object):
    def __init__(self, question, validator=None, default=None):
        self.question = question
        self.default = default
        self.validator = validator

    def __call__(self, arg_string):
        if arg_string is not _sentinel:
            return arg_string
        while True:
            response = False
            if self.default:
                self.question = '%s [%s]: ' % (self.question, self.default)
            else:
                self.question += ': '
            arg_string = raw_input(self.question)
            if self.validator is not None:
                response = self.validator(arg_string)
            if response:
                return arg_string
            elif self.default:
                return self.default
            else:
                print(self.validator.error_message)


def error_msg(msg):
    """A decorator that sets the error_message attribute of the decorated
    function to the provided value.
    """

    def decorator(func):
        """Sets the error_message attribute on the provided function"""
        func.error_message = msg
        return func

    return decorator


@error_msg('Value cannot be blank.')
def non_blank_answer(value):
    return value


@error_msg('Value cannot be blank and only contain letters and underscores.')
def valid_plugin_id(value):
    valid = string.ascii_letters + string.digits + '.' + '_'
    return value and all(c in valid for c in value)


@error_msg('The provided path must be an existing folder.')
def is_existing_folder(value):
    return os.path.isdir(value)


def build_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    create_sub = subparsers.add_parser('create')
    create_sub.add_argument('-n', '--plugin-name',
                            action=InteractiveAction,
                            type=InteractiveType(
                                'What is your plugin name?',
                                non_blank_answer),
                            help='Plugin name')
    create_sub.add_argument('-d', '--project-dir',
                            action=InteractiveAction,
                            type=InteractiveType(
                                'Where to create the project?',
                                is_existing_folder,
                                os.getcwd()),
                            help='Parent directory')
    create_sub.add_argument('-u', '--provider-name',
                            action=InteractiveAction,
                            type=InteractiveType(
                                'Enter provider name',
                                non_blank_answer),
                            help='Provider name')
    create_sub.add_argument('-i', '--plugin-id',
                            action=InteractiveAction,
                            type=InteractiveType(
                                'Enter your plugin id',
                                valid_plugin_id),
                            help='Plugin ID')

    run_group = subparsers.add_parser('run')
    run_group.add_argument('-v', '--verbose',
                           help='verbose logging')
    run_group.add_argument('-q', '--quite',
                           help='limit logging')
    return parser


def main():
    parser = build_parser()
    print(parser.parse_args(['create']))


if __name__ == '__main__':
    main()
