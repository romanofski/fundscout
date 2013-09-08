from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import Date
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.orm
import datetime


Base = declarative_base()
Session = sqlalchemy.orm.sessionmaker()


class Currency(Base):
    __tablename__ = 'currency'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    isoname = Column(String(3))

    transaction_id = Column(Integer, ForeignKey('bankaccount.id'))


class ImportBatch(Base):
    """A batch of transactions we're importing."""
    __tablename__ = 'importbatch'

    id = Column(Integer, primary_key=True)
    import_date = Column(Date, default=datetime.date.today())
    bank_account_id = Column(Integer, ForeignKey('bankaccount.id'))

    transactions = sqlalchemy.orm.relationship(
        'FundTransaction', backref='importbatch')


class FundTransaction(Base):
    """A simple transaction of funds."""
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    amount = Column(Numeric)

    import_batch_id = Column(Integer, ForeignKey('importbatch.id'))


class BankAccount(Base):
    """A bank account"""
    __tablename__ = 'bankaccount'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    currency = sqlalchemy.orm.relationship(
        'Currency', uselist=False, backref='bankaccount')

    import_batches = sqlalchemy.orm.relationship(
        'ImportBatch', backref='bankaccount')

    def import_transactions(self, list_of_transactions):
        """Wraps the list of transactions in an ImportBatch in order to
           allow easy importing/rolling back of transactions.

           Note: This should not be confused
        """
        batch = ImportBatch(transactions=list_of_transactions)
        self.import_batches.append(batch)
