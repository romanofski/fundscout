from fundscout.models import BankAccount
from fundscout.models import Currency
from fundscout.models import Session
from fundscout.models import FundTransaction
import fundscout
import fundscout.testing
import unittest


class TestAccountFunctional(unittest.TestCase):

    layer = fundscout.testing.SQLLayer

    def setUp(self):
        session = Session()
        session.add(Currency(name='Euro', isoname='EUR'))
        session.flush()

    def test_create(self):
        session = Session()
        session.add(
            BankAccount(description='Test Description',
                        currency=session.query(Currency).first())
        )

        account = session.query(BankAccount).first()
        self.assertEqual('Test Description', account.description)
        self.assertEqual('EUR', account.currency.isoname)

    def test_import_rollback_batch(self):
        session = Session()
        account = BankAccount(description='Test Description',
                              currency=session.query(Currency).first())
        transactions = [
            FundTransaction(description='first', amount=-2.30),
            FundTransaction(description='second', amount=10.02),
        ]
        account.import_transactions(transactions)

        self.assertEqual(1, len(account.import_batches))
