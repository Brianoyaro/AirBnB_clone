#!/usr/bin/python3
"""""
Place class 
"""

from models.base_model import BaseModel

class Review(BaseModel):
    """class review """
    place_id = ""
    user_id = ""
    text = ""