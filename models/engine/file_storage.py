#!/usr/bin/python3
"""file_storage engine module
"""


import json
#from models.base_model import BaseModel
#from models.user import User

class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self):
        return self.__objects

    def new(self, obj):
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        serialized_objects = {key: obj.to_dict() for key, obj in self.__objects.items()}
        with open(self.__file_path, 'w') as file:
            json.dump(serialized_objects, file)

    def reload(self):
        from models.base_model import BaseModel
        from models.user import User
        classes = {
           "BaseModel": BaseModel,
            "User": User,
        }
        try:
            with open(self.__file_path, 'r') as file:
                data = json.load(file)
                for key, value in data.items():
                    class_name, obj_id = key.split('.')
                    if class_name in classes:
                        obj = classes[class_name](**value)
                        self.__objects[key] = obj
        except FileNotFoundError:
            pass  # If file doesn't exist, do nothing