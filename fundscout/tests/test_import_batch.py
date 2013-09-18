from fundscout.models import ImportBatch
from fundscout.models import Session
import unittest
import mock
import StringIO


class TestImportBatch(unittest.TestCase):

    def setUp(self):
        self.session = mock.Mock()

    def tearDown(self):
        self.session.reset_mock()

    def test_from_csv(self):
        self.session.query.return_value.filter_by.return_value.count.return_value = 0

        csvdata = StringIO.StringIO("""06/09/2013,"-400.00",description""")
        batch = ImportBatch.from_csv(self.session, csvdata)
        self.assertEqual(1, len(batch.transactions))

    def test_from_csv_invalid(self):
        self.assertIsNone(ImportBatch.from_csv(self.session, StringIO.StringIO("")))
        self.assertIsNone(ImportBatch.from_csv(self.session, StringIO.StringIO("sdfj, asdfakfvankvdsj")))

