#!/usr/bin/python3
"""module testing file_storage.py
"""
import unittest
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
import os
from models import storage


class TestFileStorage(unittest.TestCase):
    """class handling file_storage.py testing
    """

    def test_file_json(self):
        """tests if json file is created
        """
        if os.path.isfile('file.json'):
            os.remove('file.json')
        my_model_1 = BaseModel()
        my_model_1.save()
        self.assertTrue(os.path.isfile('file.json'))

    def test_type(self):
        """tests type of __storage after creating a new instance
        """
        self.assertEqual(type(storage.all()), dict)

    def test_storage(self):
        """tests if storage actually contains the correct number of instances
        """
        if os.path.isfile('file.json'):
            os.remove('file.json')
        my_model = BaseModel()
        my_model.save()
        self.assertGreater(len(storage.all()), 0)
