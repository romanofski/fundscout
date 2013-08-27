import doctest
import fundscout.importer.config
import ghost
import os.path
import tempfile
import unittest


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(fundscout.importer.config))
    return tests
