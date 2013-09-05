import unittest
from fundscout.testing import IntegrationLayer
import fundscout.importer.config
import ghost


URL = u'http://localhost:5000/'


class TestDownloadCSV(unittest.TestCase):

    layer = IntegrationLayer

    def test_login_and_download(self):
        step = fundscout.importer.config.open([URL])
        browser = ghost.Ghost()
        page, resources = step(browser)
        self.assertTrue('User' in browser.content)
