from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.orm


Base = declarative_base()
Session = sqlalchemy.orm.sessionmaker()


class Transaction(Base):
    """A simple transaction of funds."""
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    amount = Column(Numeric)


class Account(Base):
    """A bank account"""
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    description = Column(String)
