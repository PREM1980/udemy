'''
Created on Aug 26, 2018

@author: prem
'''
import unittest
import logging
import os
from udemy.rest.client import UdemyApp, ApiClient


class TestApiClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = UdemyApp(log_level=logging.INFO)

    def tearDown(self):
        pass

    def test_api_init(self):
        api = ApiClient()
        if os.environ.get('UDEMY_CLIENT_ID') and os.environ.get('UDEMY_CLIENT_SECRET'):
            client_id = os.environ['UDEMY_CLIENT_ID']
            client_secret = os.environ['UDEMY_CLIENT_SECRET']

            api = ApiClient(client_id=client_id, client_secret=client_secret)

        if os.environ.get('UDEMY_BASE_URL'):
            api_base = os.environ['UDEMY_BASE_URL']
            api = ApiClient(client_id=client_id, client_secret=client_secret, base_url=api_base)



if __name__ == "__main__":
    unittest.main()