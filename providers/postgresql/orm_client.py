"""
Copyright © 2024 [tranandeveloper@gmail.com]
All Rights Reserved.

Licensed under the MIT License. You may obtain a copy of the License at:
    https://opensource.org/licenses/MIT

Author: TranAn
"""

import logging
from collections.abc import Generator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import (DeclarativeBase, Session, declarative_base,
                            scoped_session, sessionmaker)
from sqlalchemy.orm.scoping import QueryPropertyDescriptor

from providers.designpatterns.sigleton import SingletonMeta


class DeclarativeBaseQ:
    """_summary_
    Class used to extend the declarative base class for query property

    Args:
        DeclarativeBase (_type_): _description_
    """

    query: QueryPropertyDescriptor


class SqlalChemyClient(metaclass=SingletonMeta):

    _engine: Engine | None = None
    _session_local: scoped_session | None = None
    _base: DeclarativeBase | None = None

    def __init__(
        self,
        database_uri: str,
        pool_recycle: int = 3600,
        pool_size: int = 20,
        max_overflow: int = 0,
    ) -> None:
        self.database_uri: str = database_uri
        self.pool_recycle: int = pool_recycle
        self.pool_size: int = pool_size
        self.max_overflow: int = max_overflow

    def _init_class_instance(self):
        try:
            self._engine = create_engine(
                self.database_uri,
                pool_pre_ping=True,
                pool_recycle=self.pool_recycle,
                pool_size=self.pool_recycle,
                max_overflow=self.max_overflow,
            )
            self._session_local = scoped_session(
                sessionmaker(bind=self._engine, autocommit=False, autoflush=False)
            )
            self._base: DeclarativeBase = declarative_base(cls=DeclarativeBase)
            self._base.query = self._session_local.query_property()
        except Exception as e:
            logging.error(f"Cannot connect to database: {e}")

    @classmethod
    def get_instance(cls, database_uri: str) -> "SqlalChemyClient":
        if not cls._engine:
            return cls(database_uri)
        return cls

    def get_engine(self) -> Engine:
        if not self._engine:
            self._engine = create_engine(
                self.database_uri,
                pool_pre_ping=True,
                pool_recycle=self.pool_recycle,
                pool_size=self.pool_recycle,
                max_overflow=self.max_overflow,
            )
        return self._engine

    def get_session_local(self) -> scoped_session:
        if not self._session_local:
            self._session_local = scoped_session(
                sessionmaker(bind=self.get_engine(), autocommit=False, autoflush=False)
            )
        return self._session_local

    def get_base(self) -> DeclarativeBase:
        if not self._base:
            self._base: DeclarativeBase = declarative_base(cls=DeclarativeBaseQ)
            self._base.query = self.get_session_local().query_property()
        return self._base

    def get_session(self) -> Generator[Session]:
        """
        Function to get session for database operations

        Yields:
            Generator: _description_
        """
        session = self.get_session_local()
        try:
            yield session
        finally:
            session.close()

    @classmethod
    def create_url(
        cls,
        user: str,
        password: str,
        host: str,
        port: int,
        database: str,
    ) -> str:
        return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
