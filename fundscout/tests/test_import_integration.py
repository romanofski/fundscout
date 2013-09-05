import unittest
from fundscout.testing import IntegrationLayer
import fundscout.importer.config
import ghost


class TestDownloadCSV(unittest.TestCase):

    layer = IntegrationLayer

    def test_basic(self):
        url = u'http://localhost:5000/login'
        step = fundscout.importer.config.open([url])
        browser = ghost.Ghost()
        page, resources = step(browser)
        self.assertTrue('User' in browser.content)
