import unittest
import StringIO
from fundscout.testing import IntegrationLayer
import fundscout.importer.config
import ghost


class TestDownloadCSV(unittest.TestCase):

    layer = IntegrationLayer

    def setUp(self):
        self.config = StringIO.StringIO("""
        open http://127.0.0.1:5000/
        fill "form" user:123456, password:1234566
        debug /tmp/foo.png
        """)

    def test_login_and_download(self):
        steps = fundscout.importer.config.lex_config(self.config)
        browser = ghost.Ghost()
        for s in steps:
            s(browser)
        assert 'Download' in browser.content
