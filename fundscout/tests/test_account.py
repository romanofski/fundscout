from fundscout.models import BankAccount
from fundscout.models import Currency
from fundscout.models import FundTransaction
from fundscout.models import ImportBatch
from fundscout.models import Session
import datetime
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
            BankAccount(name='1231230-1', description='Test Description',
                        currency=session.query(Currency).first())
        )

        account = session.query(BankAccount).first()
        self.assertEqual('Test Description', account.description)
        self.assertEqual('EUR', account.currency.isoname)

    def test_import_rollback_batch(self):
        session = Session()

        #
        # We split up two transactions into two batches. At some point
        # we figure out, that the last batch was faulty and revert it.
        #
        account = BankAccount(description='Test Description',
                              currency=session.query(Currency).first())
        b1 = [
            FundTransaction(description='first', amount=-2.30,
                            effective=datetime.date.today()),
        ]
        b2 = [
            FundTransaction(description='second', amount=10.02,
                            effective=datetime.date.today()),
        ]
        session.add(ImportBatch(bank_account=account, transactions=b1))
        session.add(ImportBatch(bank_account=account, transactions=b2))
        session.commit()

        self.assertEqual(2, session.query(ImportBatch).count())

        #
        # now roll back the last set of transactions
        #
        account.rollback_batch(session, 2)
        self.assertFalse(
            session.query(FundTransaction).filter_by(description='second').first()
        )
        self.assertEqual(1, session.query(ImportBatch).count())
