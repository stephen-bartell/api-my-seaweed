import unittest

from app import create_app


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('config.test')
        self.client = self.app.test_client()

    def tearDown(self):
        pass
