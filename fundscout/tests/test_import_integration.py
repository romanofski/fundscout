from fundscout.importer import import_csv
from fundscout.models import FundTransaction
from fundscout.models import ImportBatch
from fundscout.models import Session
from fundscout.testing import IntegrationLayer
from fundscout.testing import SQLLayer
import StringIO
import fundscout.importer.config
import ghost
import os.path
import unittest


class TestDownloadCSV(unittest.TestCase):

    layer = IntegrationLayer

    def setUp(self):
        self.config = StringIO.StringIO("""
        open http://127.0.0.1:5000/
        fill "form" user:123456, password:1234566
        expect "h1"
        fill "form" daterange:1
        """)

    def test_login_and_download_csv(self):
        steps = fundscout.importer.config.lex_config(self.config)
        browser = ghost.Ghost()
        for s in steps:
            result = s(browser)
        assert 'foo,bar' in browser.content


class TestImportCSV(unittest.TestCase):

    layer = SQLLayer

    def test_import_csv(self):
        csvfile = os.path.join(os.path.dirname(__file__),
                               'testdata', 'anzexport.csv')
        import_csv(csvfile)

        session = Session()
        self.assertEqual(1, session.query(ImportBatch).count())
        self.assertEqual(4, session.query(FundTransaction).count())
