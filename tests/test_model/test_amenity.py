#!/usr/bin/python3
"""test_base_model module
"""
import unittest
from models.amenity import Amenity
import uuid
from datetime import datetime
import os
from models import storage


class TestAmenity(unittest.TestCase):
    """class testing base_model module
    """
    my_model_1 = Amenity()
    x = my_model_1.to_dict()
    my_model_1.save()
    y = my_model_1.to_dict()
    my_model_2 = Amenity(**x)

    def test_updated_at(self):
        """save method modifies updated_at instance attribute
        thus x and y should not be similar at updated_at values
        """
        self.assertNotEqual(TestAmenity.x['updated_at'], TestAmenity.y['updated_at'])
        self.assertEqual(TestAmenity.x['created_at'], TestAmenity.y['created_at'])

    def test_to_dict(self):
        """tests if to_dict method returns a dictionary
        """
        self.assertEqual(type(TestAmenity.x), dict)
        self.assertEqual(type(TestAmenity.y), dict)

    def test_kwargs(self):
        """tests if kwargs changes created_at and updated_at times
        from string to datetime
        """
        self.assertEqual(type(TestAmenity.my_model_2.created_at), datetime)
        self.assertEqual(type(TestAmenity.my_model_2.updated_at), datetime)

    def test_if_kwargs_works(self):
        """tests whether kwargs actually creates an object from scratch
        """
        if os.path.isfile("file.json"):
            os.remove("file.json")
        dummy_model = Amenity(**TestAmenity.y)
        dummy_model.save()
        self.assertGreater(len(storage.all()), 0)

    def test_if_kwargs_modified_its_parent(self):
        """tests if kwargs-id and parents-id are similar
        """
        dummy = Amenity(**TestAmenity.y)
        self.assertEqual(TestAmenity.my_model_1.id, dummy.id)

    def test_uuid(self):
        """test if different instances have unique ids
        """
        my_model_z = Amenity()
        self.assertNotEqual(TestAmenity.my_model_1.id, my_model_z.id)

    def test_type(self):
        """tests type of instance attributes
        """
        self.assertEqual(type(TestAmenity.my_model_1.created_at), datetime)
        self.assertEqual(type(TestAmenity.my_model_1.updated_at), datetime)
        self.assertEqual(type(TestAmenity.my_model_1.id), str)
