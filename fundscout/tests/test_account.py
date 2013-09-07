from fundscout.models import BankAccount
from fundscout.models import Currency
from fundscout.models import Session
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
