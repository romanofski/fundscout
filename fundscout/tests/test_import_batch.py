from fundscout.models import ImportBatch
import unittest
import StringIO


class TestImportBatch(unittest.TestCase):

    def test_from_csv(self):
        csvdata = StringIO.StringIO("""06/09/2013,"-400.00",description""")
        batch = ImportBatch.from_csv(csvdata)
        self.assertEqual(1, len(batch.transactions))

    def test_from_csv_invalid(self):
        self.assertIsNone(ImportBatch.from_csv(StringIO.StringIO("")))
        self.assertIsNone(ImportBatch.from_csv(StringIO.StringIO("sdfj, asdfakfvankvdsj")))
