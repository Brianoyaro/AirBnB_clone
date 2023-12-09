#!/usr/bin/python3
"""test_base_model module
"""
import unittest
from models.base_model import BaseModel
import uuid
from datetime import datetime
import os
from models import storage


class TestBaseModel(unittest.TestCase):
    """class testing base_model module
    """
    my_model_1 = BaseModel()
    x = my_model_1.to_dict()
    my_model_1.save()
    y = my_model_1.to_dict()
    my_model_2 = BaseModel(**x)
    def test_updated_at(self):
        """save method modifies updated_at instance attribute
        thus x and y should not be similar at updated_at values
        """
        self.assertNotEqual(TestBaseModel.x['updated_at'], TestBaseModel.y['updated_at'])
        self.assertEqual(TestBaseModel.x['created_at'], TestBaseModel.y['created_at'])

    def test_to_dict(self):
        """tests if to_dict method returns a dictionary
        """
        self.assertEqual(type(TestBaseModel.x), dict)
        self.assertEqual(type(TestBaseModel.y), dict)

    def test_kwargs(self):
        """tests if kwargs changes created_at and updated_at times
        from string to datetime
        """
        self.assertEqual(type(TestBaseModel.my_model_2.created_at), datetime)
        self.assertEqual(type(TestBaseModel.my_model_2.updated_at), datetime)

    def test_if_kwargs_works(self):
        """tests whether kwargs actually creates an object from scratch
        """
        if os.path.isfile("file.json"):
            os.remove("file.json")
        dummy_model = BaseModel(**TestBaseModel.y)
        dummy_model.save()
        self.assertGreater(len(storage.all()), 0)

    def test_if_kwargs_modified_its_parent(self):
        """tests if kwargs-id and parents-id are similar
        """
        dummy = BaseModel(**TestBaseModel.y)
        self.assertEqual(TestBaseModel.my_model_1.id, dummy.id)

    def test_uuid(self):
        """test if different instances have unique ids
        """
        my_model_z = BaseModel()
        self.assertNotEqual(TestBaseModel.my_model_1.id, my_model_z.id)

    def test_type(self):
        """tests type of instance attributes
        """
        self.assertEqual(type(TestBaseModel.my_model_1.created_at), datetime)
        self.assertEqual(type(TestBaseModel.my_model_1.updated_at), datetime)
        self.assertEqual(type(TestBaseModel.my_model_1.id), str)
