from fundscout.testing import IntegrationLayer
import StringIO
import fundscout.importer.config
import ghost
import unittest


class TestDownloadCSV(unittest.TestCase):

    layer = IntegrationLayer

    def setUp(self):
        self.config = StringIO.StringIO("""
        open http://127.0.0.1:5000/
        fill "form" user:123456, password:1234566
        validate "h1"
        fill "form" daterange:1
        """)

    def test_login_and_download(self):
        steps = fundscout.importer.config.lex_config(self.config)
        browser = ghost.Ghost()
        for s in steps:
            result = s(browser)
        assert 'foo,bar' in browser.content
