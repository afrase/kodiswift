import time
from datetime import timedelta
from tempfile import NamedTemporaryFile
from unittest import TestCase

from kodiswift.storage import TimedStorage, PersistentStorage, Formats


class TestCache(TestCase):

    def test_pickle(self):
        with NamedTemporaryFile() as temp:
            storage = PersistentStorage(temp.name, Formats.PICKLE)

            storage['name'] = 'jon'
            storage.update({'answer': 42})
            storage.close()

            storage2 = PersistentStorage(temp.name, Formats.PICKLE)
            storage2.load()
            self.assertEqual(storage, storage2)
            self.assertEqual(2, len(storage2.items()))
            self.assertTrue('name' in storage2.keys())
            self.assertTrue('answer' in storage2.keys())
            self.assertEqual('jon', storage2.pop('name'))
            self.assertEqual(42, storage2['answer'])

    def test_json(self):
        with NamedTemporaryFile() as temp:
            storage = PersistentStorage(temp.name, file_format='json')

            storage['name'] = 'jon'
            storage.update({'answer': '42'})
            storage.close()

            storage2 = PersistentStorage(temp.name, file_format='json')
            storage2.load()
            self.assertEqual(sorted(storage.items()), sorted(storage2.items()))
            self.assertEqual(2, len(storage2.items()))
            self.assertTrue('name' in storage2.keys())
            self.assertTrue('answer' in storage2.keys())
            self.assertEqual('jon', storage2.pop('name'))
            self.assertEqual('42', storage2['answer'])


class TestTimedStorage(TestCase):

    def test_timed_pickle(self):
        with NamedTemporaryFile() as temp:
            storage = TimedStorage(temp.name, timedelta(hours=1),
                                   file_format=Formats.PICKLE)
        storage['name'] = 'jon'
        storage.update({'answer': 42})
        storage.close()

        storage2 = TimedStorage(temp.name, timedelta(hours=1),
                                file_format=Formats.PICKLE)
        storage2.load()
        self.assertEqual(sorted(storage.items()), sorted(storage2.items()))

        time.sleep(2)
        storage3 = TimedStorage(temp.name, timedelta(seconds=2),
                                file_format=Formats.PICKLE)
        storage3.load()
        self.assertEqual([], sorted(storage3.items()))
        storage3.close()

        storage4 = TimedStorage(temp.name, timedelta(hours=1),
                                file_format=Formats.PICKLE)
        storage4.load()
        self.assertEqual(sorted(storage3.items()), sorted(storage4.items()))

    def test_timed_json(self):
        with NamedTemporaryFile() as temp:
            storage = TimedStorage(temp.name, timedelta(hours=1),
                                   file_format=Formats.JSON)
        storage['name'] = 'jon'
        storage.update({'answer': 42})
        storage.close()

        storage2 = TimedStorage(temp.name, timedelta(hours=1),
                                file_format=Formats.JSON)
        storage2.load()
        self.assertEqual(sorted(storage.items()), sorted(storage2.items()))

        time.sleep(2)
        storage3 = TimedStorage(temp.name, timedelta(seconds=2),
                                file_format=Formats.JSON)
        storage3.load()
        self.assertEqual([], sorted(storage3.items()))
        storage3.close()

        storage4 = TimedStorage(temp.name, timedelta(hours=1),
                                file_format=Formats.JSON)
        storage4.load()
        self.assertEqual(sorted(storage3.items()), sorted(storage4.items()))
