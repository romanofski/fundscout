from fundscout.importer import guess_account_from_filename
from fundscout.importer import import_csv
from fundscout.models import BankAccount
from fundscout.models import Currency
from fundscout.models import FundTransaction
from fundscout.models import ImportBatch
from fundscout.models import Session
from fundscout.testing import SQLLayer
import mock
import os.path
import unittest


class TestImporter(unittest.TestCase):

    def test_guess_account_from_filename(self):
        class FakeAccount(object):
            def __init__(self, name):
                self.name = name

        account = FakeAccount('foo')
        session = mock.Mock()
        session.query.return_value.filter_by.return_value.first.return_value = account

        self.assertEqual(account,
                         guess_account_from_filename(session, 'foo'))
        self.assertEqual(account,
                         guess_account_from_filename(session, 'FOO'))

    def test_guess_account_from_filename_no_existing_account(self):
        session = mock.Mock()
        session.query.return_value.filter_by.return_value.first.return_value = None

        self.assertIsNone(guess_account_from_filename(session, ''))


class TestImportCSV(unittest.TestCase):

    layer = SQLLayer

    def setUp(self):
        self.csvfile = os.path.join(os.path.dirname(__file__),
                                    'testdata', '123-123.csv')
        self.session = Session()

    def test_import_csv(self):
        import_csv(self.csvfile)

        self.assertEqual(1, self.session.query(ImportBatch).count())
        self.assertEqual(5, self.session.query(FundTransaction).count())

    def test_avoid_duplicates(self):
        import_csv(self.csvfile)
        import_csv(self.csvfile)

        self.assertEqual(1, self.session.query(ImportBatch).count())
