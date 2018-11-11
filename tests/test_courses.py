'''
Created on Aug 26, 2018

@author: prem
'''
import unittest
import logging
from udemy.rest.client import UdemyApp


class Test(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.app = UdemyApp(log_level=logging.WARNING)

    def tearDown(self):
        pass

    def test_get_all_courses(self):
        print('start')
#         self.app.courses.get_all()
        print('Complete')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()