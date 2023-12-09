#!/usr/bin/python3
"""test_base_model module
"""
import unittest
from models.place import Place
import uuid
from datetime import datetime
import os
from models import storage


class TestPlace(unittest.TestCase):
    """class testing base_model module
    """
    my_model_1 = Place()
    x = my_model_1.to_dict()
    my_model_1.save()
    y = my_model_1.to_dict()
    my_model_2 = Place(**x)
    def test_updated_at(self):
        """save method modifies updated_at instance attribute
        thus x and y should not be similar at updated_at values
        """
        self.assertNotEqual(TestPlace.x['updated_at'], TestPlace.y['updated_at'])
        self.assertEqual(TestPlace.x['created_at'], TestPlace.y['created_at'])

    def test_to_dict(self):
        """tests if to_dict method returns a dictionary
        """
        self.assertEqual(type(TestPlace.x), dict)
        self.assertEqual(type(TestPlace.y), dict)

    def test_kwargs(self):
        """tests if kwargs changes created_at and updated_at times
        from string to datetime
        """
        self.assertEqual(type(TestPlace.my_model_2.created_at), datetime)
        self.assertEqual(type(TestPlace.my_model_2.updated_at), datetime)

    def test_if_kwargs_works(self):
        """tests whether kwargs actually creates an object from scratch
        """
        if os.path.isfile("file.json"):
            os.remove("file.json")
        dummy_model = Place(**TestPlace.y)
        dummy_model.save()
        self.assertGreater(len(storage.all()), 0)

    def test_if_kwargs_modified_its_parent(self):
        """tests if kwargs-id and parents-id are similar
        """
        dummy = Place(**TestPlace.y)
        self.assertEqual(TestPlace.my_model_1.id, dummy.id)

    def test_uuid(self):
        """test if different instances have unique ids
        """
        my_model_z = Place()
        self.assertNotEqual(TestPlace.my_model_1.id, my_model_z.id)

    def test_type(self):
        """tests type of instance attributes
        """
        self.assertEqual(type(TestPlace.my_model_1.created_at), datetime)
        self.assertEqual(type(TestPlace.my_model_1.updated_at), datetime)
        self.assertEqual(type(TestPlace.my_model_1.id), str)
