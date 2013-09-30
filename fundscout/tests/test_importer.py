from fundscout.importer import guess_account_from_filename
import mock
import unittest


class TestImporter(unittest.TestCase):

    def test_guess_account_from_filename(self):
        class FakeAccount(object):
            def __init__(self, name):
                self.name = name

        accounts = [FakeAccount('foo'), FakeAccount('bar')]
        session = mock.Mock()
        session.query.return_value.all.return_value = accounts

        self.assertEqual(accounts[0],
                         guess_account_from_filename(session, 'foo.frob.bar'))
        self.assertEqual(accounts[0],
                         guess_account_from_filename(session, 'FOO'))
        self.assertIsNone(guess_account_from_filename(session, ''))


class TestImportCSV(unittest.TestCase):

    layer = SQLLayer

    def setUp(self):
        self.csvfile = os.path.join(os.path.dirname(__file__),
                                    'testdata', 'anzexport.csv')
        self.session = Session()

    def test_import_csv(self):
        import_csv(self.csvfile)

        self.assertEqual(1, self.session.query(ImportBatch).count())
        self.assertEqual(5, self.session.query(FundTransaction).count())

    def test_avoid_duplicates(self):
        import_csv(self.csvfile)
        import_csv(self.csvfile)

        self.assertEqual(1, self.session.query(ImportBatch).count())
