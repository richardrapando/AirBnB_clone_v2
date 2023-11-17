#!/usr/bin/python3
import models
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
import uuid
from os import getenv
from datetime import datetime
"""Module defining base class for all models in the hbnb clone
   with base_model having class BaseModel that defines all
   common attributes other class methods
"""


time = "%Y-%m-%dT%H:%M:%S.%f"
if getenv("HBNB_TYPE_STORAGE") == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """Attributes of public instance:
       id, created_at, updated_at
    """
    if getenv("HBNB_TYPE_STORAGE") == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow())
        updated_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Initialization
        id uses uuid.uuid4(). Unique id for each BaseModel regenerated.
        updated_at -> datetime updates enytime an object is changed.
        *args and **kwargs are constructors
        """
        if kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            for k, v in kwargs.items():
                if k == "created_at" or k == "updated_at":
                    v = datetime.strptime(v, time)
                if k != "__class__":
                    setattr(self, k, v)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            """ models.storage.new(self)"""

    def __str__(self):
        """String representation of BaseModel class returned
           Prints: "(class name) (self.id) (self.__dict__)"
       """
        return ("[{}] ({}) {}".format(self.__class__.__name__,
                self.id, self.__dict__))

    def __repr__(self):
        """
        String representation of BaseModel return 
        calls __str__()
        """
        return (self.__str__())

    def save(self):
        """Updates updated_at with current time when an instance is changed
            calls save(self) method of storage
        """
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Instance converted into dict format"""
        dictionary = self.__dict__.copy()
        if "created_at" in dictionary:
            dictionary["created_at"] = dictionary["created_at"].strftime(time)
        if "updated_at" in dictionary:
            dictionary["updated_at"] = dictionary["updated_at"].strftime(time)
        dictionary["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in dictionary:
            del dictionary["_sa_instance_state"]
        return dictionary

    def delete(self):
        """
        Instance deleted from storage
        """
        models.storage.delete(self)
