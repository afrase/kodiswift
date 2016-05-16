"""
    kodiswift.storage
    ~~~~~~~~~~~~~~~~~~

    This module contains persistent storage classes.

    :copyright: (c) 2012 by Jonathan Beluch
    :license: GPLv3, see LICENSE for more details.
"""
import collections
import csv
import json
import os
import shutil
import time
from datetime import datetime

from kodiswift._compat import pickle
from kodiswift.logger import log


class _persistentdictmixin(object):
    """Persistent dictionary with an API compatible with shelve and anydbm.

    The dict is kept in memory, so the dictionary operations run as fast as
    a regular dictionary.

    Write to disk is delayed until close or sync (similar to gdbm's fast mode).

    Input file format is automatically discovered.
    Output file format is selectable between pickle, json, and csv.
    All three serialization formats are backed by fast C implementations.
    """

    def __init__(self, filename, flag='c', mode=None, file_format='pickle'):
        self.flag = flag  # r=readonly, c=create, or n=new
        self.mode = mode  # None or an octal triple like 0644
        self.file_format = file_format  # 'csv', 'json', or 'pickle'
        self.filename = filename
        if flag != 'n' and os.access(filename, os.R_OK):
            log.debug('Reading %s storage from disk at "%s"',
                      self.file_format, self.filename)
            with open(filename, 'rb') as f:
                self.load(f)

    def sync(self):
        """Write the dict to disk"""
        if self.flag == 'r':
            return
        filename = self.filename
        temp_name = filename + '.tmp'
        file_obj = open(temp_name, 'wb')
        try:
            self.dump(file_obj)
        except Exception:
            os.remove(temp_name)
            raise
        finally:
            file_obj.close()
        shutil.move(temp_name, self.filename)  # atomic commit
        if self.mode is not None:
            os.chmod(self.filename, self.mode)

    def close(self):
        """Calls sync"""
        self.sync()

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()

    def dump(self, file_obj):
        """Handles the writing of the dict to the file object"""
        if self.file_format == 'csv':
            csv.writer(file_obj).writerows(self.raw_dict().items())
        elif self.file_format == 'json':
            json.dump(self.raw_dict(), file_obj, separators=(',', ':'))
        elif self.file_format == 'pickle':
            pickle.dump(dict(self.raw_dict()), file_obj, 2)
        else:
            raise NotImplementedError('Unknown format: ' +
                                      repr(self.file_format))

    def load(self, fileobj):
        """Load the dict from the file object"""
        # try formats from most restrictive to least restrictive
        for loader in (pickle.load, json.load, csv.reader):
            fileobj.seek(0)
            try:
                return self.initial_update(loader(fileobj))
            except Exception:
                pass
        raise ValueError('File not in a supported format')

    def raw_dict(self):
        """Returns the underlying dict"""
        raise NotImplementedError


class _Storage(collections.MutableMapping, _persistentdictmixin):
    """Storage that acts like a dict but also can persist to disk.

    :param filename: An absolute filepath to reprsent the storage on disk. The
                     storage will loaded from this file if it already exists,
                     otherwise the file will be created.
    :param file_format: 'pickle', 'json' or 'csv'. pickle is the default. Be
                        aware that json and csv have limited support for python
                        objets.

    .. warning:: Currently there are no limitations on the size of the storage.
                 Please be sure to call :meth:`~kodiswift._Storage.clear`
                 periodically.
    """

    def __init__(self, filename, file_format='pickle'):
        """Acceptable formats are 'csv', 'json' and 'pickle'."""
        super(_Storage, self).__init__(filename, file_format=file_format)
        self._items = {}

    def __setitem__(self, key, val):
        self._items.__setitem__(key, val)

    def __getitem__(self, key):
        return self._items.__getitem__(key)

    def __delitem__(self, key):
        self._items.__delitem__(key)

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return self._items.__len__

    def raw_dict(self):
        """Returns the wrapped dict"""
        return self._items

    initial_update = collections.MutableMapping.update

    def clear(self):
        super(_Storage, self).clear()
        self.sync()


class TimedStorage(_Storage):
    """A dict with the ability to persist to disk and TTL for items."""

    def __init__(self, filename, file_format='pickle', ttl=None):
        """TTL if provided should be a datetime.timedelta. Any entries
        older than the provided TTL will be removed upon load and upon item
        access.
        """
        super(TimedStorage, self).__init__(filename, file_format=file_format)
        self.TTL = ttl

    def __setitem__(self, key, val, raw=False):
        if raw:
            self._items[key] = val
        else:
            self._items[key] = (val, time.time())

    def __getitem__(self, key):
        val, timestamp = self._items[key]
        ttl_diff = datetime.utcnow() - datetime.utcfromtimestamp(timestamp)
        if self.TTL and ttl_diff > self.TTL:
            del self._items[key]
            return self._items[key][0]  # Will raise KeyError
        return val

    def initial_update(self, mapping):
        """Initially fills the underlying dictionary with keys, values and
        timestamps.
        """
        for key, val in mapping.items():
            _, timestamp = val
            ttl_diff = datetime.utcnow() - datetime.utcfromtimestamp(timestamp)
            if not self.TTL or ttl_diff < self.TTL:
                self.__setitem__(key, val, raw=True)

    def dump(self, file_obj):
        pass
