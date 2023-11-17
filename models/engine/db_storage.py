#!/usr/bin/python3
"""
Class DBStorage container
"""

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage():
    """Associates with MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """DBStorage object instantiator"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB,
                                             pool_pre_ping=True))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Dictionary returned with all objects depending
        of the class name (argument cls)"""
        if cls:
            if isinstance(cls, str):
                objs = self.__session.query(classes[cls])
            else:
                for key, value in classes.items():
                    if value == cls:
                        objs = self.__session.query(classes[key])
                        break
        else:
            objs = self.__session.query(State).all()
            objs += self.__session.query(City).all()
            objs += self.__session.query(User).all()
            objs += self.__session.query(Place).all()
            objs += self.__session.query(Amenity).all()
            objs += self.__session.query(Review).all()

        a_dict = {}
        for obj in objs:
            k = '{}.{}'.format(type(obj).__name__, obj.id)
            a_dict[k] = obj
        return a_dict

    def new(self, obj):
        """Object addedto the current database session"""
        self.__session.add(obj)

    def save(self):
        """All changes of the current database session commited"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletion from current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Data from the database reloaded"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """remove() method called on the private session attribute"""
        self.__session.close()
