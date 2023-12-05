#!/usr/bin/python3
"""file_storage engine module
"""
import os
import json


class FileStorage:
    """file_storage class
    """
    __file_path = "file.json"
    __objects = {}
    __mapping = {}

    def all(self):
        """returns the __objects dictionary
        """
        return self.__objects

    def new(self, obj):
        """adds an entry in __objects in the form:
        id-> <obj class_name>.id
        value->obj
        """
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """ serializes __objects to the JSON file
        """
        new_dict = {}
        for key, value in self.__objects.items():
            new_dict[key] = value.to_dict()
        with open(self.__file_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(new_dict))

    def reload(self):
        """ deserializes the JSON file to __objects.
        If json file doesn't exixt, do nothing
        """
        from models.base_model import BaseModel
        self.__mapping = {"BaseModel": BaseModel}
        if os.path.isfile(self.__file_path):
            with open(self.__file_path, 'r', encoding='utf-8') as f:
                temp1 = f.read()
            # self.__objects = json.loads(temp)
            temp = json.loads(temp1)
            for key, value in temp.items():
                specific_class = value["__class__"]
                if specific_class in self.__mapping.keys():
                    class_ = self.__mapping[specific_class]
                    object_ = class_(**value)
                self.__objects[key] = object_
        else:
            pass
