from fundscout.models import BankAccount
from fundscout.models import FundTransaction
from fundscout.models import ImportBatch
from fundscout.models import Institute
from fundscout.models import Session
import datetime
import fundscout
import fundscout.testing
import unittest


class TestAccountFunctional(unittest.TestCase):

    layer = fundscout.testing.SQLLayer

    def setUp(self):
        self.session = Session()

    def test_create(self):
        self.session.add(
            BankAccount(name='1231230-1', description='Test Description',
                        currency='AUD')
        )

        account = self.session.query(BankAccount).first()
        self.assertEqual('Test Description', account.description)
        self.assertEqual('AUD', account.currency)

    def test_import_rollback_batch(self):
        #
        # We split up two transactions into two batches. At some point
        # we figure out, that the last batch was faulty and revert it.
        #
        account = BankAccount(name='123-123', description='Test Description',
                              currency='EUR')
        b1 = [
            FundTransaction(description='first', amount=-2.30,
                            effective=datetime.date.today()),
        ]
        b2 = [
            FundTransaction(description='second', amount=10.02,
                            effective=datetime.date.today()),
        ]
        self.session.add(ImportBatch(bank_account=account, transactions=b1))
        self.session.add(ImportBatch(bank_account=account, transactions=b2))
        self.session.commit()

        self.assertEqual(2, self.session.query(ImportBatch).count())

        #
        # now roll back the last set of transactions
        #
        account.rollback_batch(self.session, 2)
        self.assertFalse(
            self.session.query(FundTransaction).filter_by(description='second').first()
        )
        self.assertEqual(1, self.session.query(ImportBatch).count())
