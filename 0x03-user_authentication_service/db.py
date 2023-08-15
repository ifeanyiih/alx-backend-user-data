#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """saves a user to the database"""
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, *args, **kwargs) -> User:
        """Finds a user, based on the arguments passed"""
        session = self._session
        user = session.query(User).filter_by(**kwargs).one()
        return user

    def update_user(self, user_id: int, *args, **kwargs) -> None:
        """Finds and updates a user in the database"""
        session = self._session
        user = self.find_user_by(id=user_id)
        for key in kwargs.keys():
            user.key = kwargs[key]
        session.commit()
