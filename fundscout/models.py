from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.orm


Base = declarative_base()
Session = sqlalchemy.orm.sessionmaker()


class Currency(Base):
    __tablename__ = 'currency'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    isoname = Column(String(3))

    transaction_id = Column(Integer, ForeignKey('bankaccount.id'))


class Transaction(Base):
    """A simple transaction of funds."""
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    amount = Column(Numeric)



class BankAccount(Base):
    """A bank account"""
    __tablename__ = 'bankaccount'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    currency = sqlalchemy.orm.relationship(
        'Currency', uselist=False, backref='bankaccount')
