from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import DateTime
from sqlalchemy import Date
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import csv
import datetime
import pycountry
import re
import sqlalchemy.orm


Base = declarative_base()
Session = sqlalchemy.orm.sessionmaker()


class ImportBatch(Base):
    """A batch of transactions we're importing."""
    __tablename__ = 'importbatch'

    id = Column(Integer, primary_key=True)
    import_date = Column(DateTime, default=datetime.datetime.utcnow,
                         nullable=False)
    bank_account_id = Column(Integer, ForeignKey('bankaccount.id'))
    bank_account = sqlalchemy.orm.relationship(
        'BankAccount', backref='importbatch')

    transactions = sqlalchemy.orm.relationship(
        'FundTransaction', backref='importbatch',
        cascade='all, delete, delete-orphan')

    @classmethod
    def from_csv(klass, session, fp):
        """ Creates transactions and a single import batch from csv
            data.

            Returns None if no transactions can be imported.
        """
        transactions = []
        for row in csv.reader(fp):
            if not row:
                continue
            try:
                effective_date = datetime.datetime.strptime(row[0], '%d/%m/%Y')
            except ValueError:
                continue
            data = dict(description=row[-1],
                        amount=row[1],
                        effective=effective_date.date(),
                       )
            tx_count = session.query(FundTransaction).filter_by(**data).count()
            if not tx_count:
                tx = FundTransaction(**data)
                transactions.append(tx)

        if not transactions:
            return

        batch = klass(transactions=transactions)
        return batch


class FundTransaction(Base):
    """A simple transaction of funds."""
    __tablename__ = 'fundtransaction'

    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    amount = Column(Numeric, nullable=False)
    effective = Column(Date, nullable=False)

    import_batch_id = Column(Integer, ForeignKey('importbatch.id'))


class Institute(Base):
    """A user can have many accounts at an institute, like a bank.

       This is needed to be able to look dependent import mechanisms for
       each bank account.
    """
    __tablename__ = 'institute'

    id = Column(Integer, primary_key=True)
    shortname = Column(String, nullable=False)
    title = Column(String)

    bank_accounts = sqlalchemy.orm.relationship(
        'BankAccount', backref='bankaccount')


class BankAccount(Base):
    """A bank account"""
    __tablename__ = 'bankaccount'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    currency = Column(String, nullable=False)

    institute_id = Column(Integer, ForeignKey('institute.id'))

    @sqlalchemy.orm.validates('name')
    def validate_name(self, key, name):
        """ Refuse any name which does not consist of numbers and a
            dash.
        """
        assert re.match('[\d-]+', name), (
            "Valid account names should be account numbers! e.g.  12312-213123")
        return name

    @sqlalchemy.orm.validates('currency')
    def validate_currency(self, key, name):
        assert pycountry.currencies.get(letter=name), (
            "Currency should be the iso letter, e.g. EUR, AUD, USD")
        return name

    @classmethod
    def find_by_name(self, session, name):
        return session.query(BankAccount).filter_by(name=name).first()

    def rollback_batch(self, session, batchid):
        batch = session.query(ImportBatch).filter_by(id = batchid).first()
        if batch is not None:
            session.delete(batch)
