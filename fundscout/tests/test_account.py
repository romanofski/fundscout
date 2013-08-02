from fundscout.models import Account
from fundscout.models import Session
import fundscout
import fundscout.testing
import unittest


class TestAccountFunctional(unittest.TestCase):

    layer = fundscout.testing.SQLLayer

    def test_create(self):
        session = Session()
        session.add(Account(description='Test Description'))

        account = session.query(Account).first()
        self.assertEqual('Test Description', account.description)
