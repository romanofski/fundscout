from fundscout.importer import import_csv
from fundscout.models import BankAccount
from fundscout.models import FundTransaction
from fundscout.models import ImportBatch
from fundscout.models import Session
from fundscout.testing import SQLLayer
import mock
import os.path
import unittest


class TestImportCSV(unittest.TestCase):

    layer = SQLLayer

    def setUp(self):
        self.csvfile = os.path.join(os.path.dirname(__file__),
                                    'testdata', '123-123.csv')
        self.account = BankAccount(name='123-123', description='Test Description',
                                   currency='AUD')
        self.session = Session()
        self.session.add(self.account)
        self.session.flush()

    def test_import_csv(self):
        import_csv(self.session, self.csvfile, self.account)

        self.assertEqual(1, self.session.query(ImportBatch).count())
        self.assertEqual(5, self.session.query(FundTransaction).count())

    def test_avoid_duplicates(self):
        import_csv(self.session, self.csvfile, self.account)
        import_csv(self.session, self.csvfile, self.account)

        self.assertEqual(1, self.session.query(ImportBatch).count())
