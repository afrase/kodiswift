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

# The `type' argument of `add_argument' is the only way to manipulate the
# final results of parsing the command line arguments. Unfortunately 'type' is
# only called when a value is passed or a default is set. To support both
# command line args and prompting the user for input, a default has to be set
# for all arguments so `InteractiveType' is guaranteed to be called. The
# `_sentinel' variable is used so `InteractiveType' can tell if an argument
# was used when invoking the CLI.
_sentinel = '==SENTINEL=='


class InteractiveAction(argparse.Action):
    """Sets a known default for all values to guarantee the `type' is called.
    """

    def __init__(self, **kwargs):
        super(InteractiveAction, self).__init__(default=_sentinel, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


class InteractiveType(object):
    def __init__(self, question, validator=None, default=None, example=None):
        super(InteractiveType, self).__init__()
        self.question = question
        self.validator = validator
        self.default = default
        self.example = example

    def __call__(self, arg_string):
        if arg_string is not _sentinel:
            return arg_string
        while True:
            response = False
            if self.default:
                question = '%s [%s]: ' % (self.question, self.default)
            elif self.example:
                question = '%s (e.g. %s): ' % (self.question, self.example)
            else:
                question = self.question + ': '
            # TODO(Sinap): Maybe catch `KeyboardInterrupt' to gracefully exit?
            arg_string = raw_input(question).strip()
            if self.validator is not None:
                response = self.validator(arg_string)
            if response:
                return arg_string
            elif self.default:
                # TODO(Sinap): should this return if the validator failed?
                return self.default
            else:
                # TODO(Sinap): Should we use a class to print the messages
                # instead of using the print method?
                print(self.validator.error_message)


def error_msg(msg):
    """A decorator that sets the error_message attribute of the decorated
    function to the provided value.

    Args:
        msg (str): Message to display
    """

    def decorator(func):
        """Sets the error_message attribute on the provided function
        """
        func.error_message = msg
        return func

    return decorator


@error_msg('Value cannot be blank.')
def non_blank_answer(value):
    return bool(value)


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
    create_sub.add_argument(
        '-n', '--plugin-name',
        action=InteractiveAction,
        type=InteractiveType('What is your plugin name?', non_blank_answer),
        help='The name of the plugin')
    create_sub.add_argument(
        '-d', '--project-dir',
        action=InteractiveAction,
        type=InteractiveType('Where to create the project?',
                             is_existing_folder, os.getcwd()),
        help='The project directory')
    create_sub.add_argument(
        '-u', '--provider-name',
        action=InteractiveAction,
        type=InteractiveType('Enter provider name', non_blank_answer),
        help='The provider name (your name)')
    create_sub.add_argument(
        '-i', '--plugin-id',
        action=InteractiveAction,
        type=InteractiveType('Enter your plugin id', valid_plugin_id,
                             example='plugin.video.example'),
        help='The plugins ID')

    run_sub = subparsers.add_parser('run')
    run_sub.add_argument(
        '-v', '--verbose',
        help='verbose logging')
    run_sub.add_argument(
        '-q', '--quite',
        help='limit logging')

    return parser


def main():
    parser = build_parser()
    print(parser.parse_args())


if __name__ == '__main__':
    main()
