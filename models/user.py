#!/usr/bin/python3
"""
class user that inherits from BaseModel
"""

from models.base_model import BaseModel

class User(BaseModel):
    """user class"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""

    #def __init__(self, *args, **kwargs):
        #super().__init__(self, *args, **kwargs)
