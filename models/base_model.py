#!/usr/bin/python3
"""base_model template for all classes
"""
import uuid
from datetime import datetime
from models.engine.file_storage import FileStorage
from models import storage

class BaseModel:
    """BaseModel class
    """
    class_name = 'BaseModel'

    def __init__(self, *args, **kwargs):
        """initialises each unique instance with a different
        unique Id, created_at time and updated_at time
        """
        if kwargs:
             for key, value in kwargs.items():
                if key != '__class__':
                    if key in ['created_at', 'updated_at']:
                        value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                    setattr(self, key, value)
                    if 'created_at' not in kwargs:
                        self.created_at = datetime.now()
                    if 'id' not in kwargs:
                        self.id = str(uuid.uuid4())
           
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """returns a nicely printable instance
        """
        return "[{}] ({}) {}".format(self.class_name, self.id, self.__dict__)

    def save(self):
        """updates the instance variable when saving the instance
        e.g before exiting the program
        """
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        return obj_dict