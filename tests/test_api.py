#!/usr/bin/python
# -*- coding: latin-1 -*-
'''
Created on Aug 26, 2018

@author: prem
'''
import unittest
import logging
import responses
import re
import os
import json
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

class TestApiExceptions(unittest.TestCase):
  """ test api errors """

  @classmethod
  def setUpClass(cls):
    cls.app = UdemyApp()

  def test_bad_gateway_error(self):
    """ test bad gateway error
    """    

    mocked_obj = {
      u'status':
        {
          u'code': 10020,
          u'description': u'Bad gateway'
        }
    }
    mocked_json = json.dumps(mocked_obj)

    mocked_good_json = '''{
  "count": 10000,
  "next": "https://www.udemy.com/api-2.0/courses/?page=2&page_size=2",
  "previous": null,
  "results": [
    {
      "_class": "course",
      "id": 567828,
      "title": "Complete Python Bootcamp: Go from zero to hero in Python 3",
      "url": "/complete-python-bootcamp/",
      "is_paid": true,
      "price": "$194.99",
      "price_detail": {
        "currency": "USD",
        "amount": 194.99,
        "price_string": "$194.99",
        "currency_symbol": "$"
      },
      "visible_instructors": [
        {
          "name": "Jose",
          "url": "/user/joseportilla/",
          "display_name": "Jose Portilla",
          "image_50x50": "https://udemy-images.udemy.com/user/50x50/9685726_67e7_4.jpg",
          "initials": "JP",
          "_class": "user",
          "job_title": "Data Scientist",
          "image_100x100": "https://udemy-images.udemy.com/user/100x100/9685726_67e7_4.jpg",
          "title": "Jose Portilla"
        },
        {
          "name": "Pierian Data International",
          "url": "/user/pierian-data-international/",
          "display_name": "Pierian Data International by Jose Portilla",
          "image_50x50": "https://udemy-images.udemy.com/user/50x50/38701326_414a.jpg",
          "initials": "PB",
          "_class": "user",
          "job_title": "Jose Portilla's Pierian Data Inc. International Translations",
          "image_100x100": "https://udemy-images.udemy.com/user/100x100/38701326_414a.jpg",
          "title": "Pierian Data International by Jose Portilla"
        }
      ],
      "image_125_H": "https://udemy-images.udemy.com/course/125_H/567828_67d0.jpg",
      "image_240x135": "https://udemy-images.udemy.com/course/240x135/567828_67d0.jpg",
      "is_practice_test_course": false,
      "image_480x270": "https://udemy-images.udemy.com/course/480x270/567828_67d0.jpg",
      "published_title": "complete-python-bootcamp",
      "predictive_score": null,
      "relevancy_score": 110.99998,
      "input_features": null,
      "lecture_search_result": null,
      "curriculum_lectures": []
    },
    {
      "_class": "course",
      "id": 362328,
      "title": "AWS Certified Solutions Architect - Associate 2018",
      "url": "/aws-certified-solutions-architect-associate/",
      "is_paid": true,
      "price": "$179.99",
      "price_detail": {
        "currency": "USD",
        "amount": 179.99,
        "price_string": "$179.99",
        "currency_symbol": "$"
      },
      "visible_instructors": [
        {
          "name": "Ryan",
          "url": "/user/ryankroonenburg/",
          "display_name": "Ryan Kroonenburg",
          "image_50x50": "https://udemy-images.udemy.com/user/50x50/646294_3e1d_3.jpg",
          "initials": "RK",
          "_class": "user",
          "job_title": "Solutions Architect",
          "image_100x100": "https://udemy-images.udemy.com/user/100x100/646294_3e1d_3.jpg",
          "title": "Ryan Kroonenburg"
        },
        {
          "name": "Faye",
          "url": "/user/faye-ellis-2/",
          "display_name": "Faye Ellis",
          "image_50x50": "https://udemy-images.udemy.com/user/50x50/44848936_b7c8_2.jpg",
          "initials": "FE",
          "_class": "user",
          "job_title": "Instructor at A Cloud Guru",
          "image_100x100": "https://udemy-images.udemy.com/user/100x100/44848936_b7c8_2.jpg",
          "title": "Faye Ellis"
        }
      ],
      "image_125_H": "https://udemy-images.udemy.com/course/125_H/362328_91f3_10.jpg",
      "image_240x135": "https://udemy-images.udemy.com/course/240x135/362328_91f3_10.jpg",
      "is_practice_test_course": false,
      "image_480x270": "https://udemy-images.udemy.com/course/480x270/362328_91f3_10.jpg",
      "published_title": "aws-certified-solutions-architect-associate",
      "predictive_score": null,
      "relevancy_score": 110.99998,
      "input_features": null,
      "lecture_search_result": null,
      "curriculum_lectures": []
    }
  ],
  "aggregations": [
    {
      "options": [
        {
          "count": 10000,
          "value": "price-paid",
          "title": "Paid",
          "key": "price"
        },
        {
          "count": 6961,
          "value": "price-free",
          "title": "Free",
          "key": "price"
        }
      ],
      "title": "Price",
      "id": "price"
    },
    {
      "options": [
        {
          "count": 10000,
          "value": "all",
          "title": "All Levels",
          "key": "instructional_level"
        },
        {
          "count": 10000,
          "value": "beginner",
          "title": "Beginner",
          "key": "instructional_level"
        },
        {
          "count": 10000,
          "value": "intermediate",
          "title": "Intermediate",
          "key": "instructional_level"
        },
        {
          "count": 1606,
          "value": "expert",
          "title": "Expert",
          "key": "instructional_level"
        }
      ],
      "title": "Level",
      "id": "instructional_level"
    },
    {
      "options": [
        {
          "count": 10000,
          "value": "true",
          "title": "Captions",
          "key": "has_closed_caption"
        },
        {
          "count": 10000,
          "value": "true",
          "title": "Quizzes",
          "key": "has_simple_quiz"
        },
        {
          "count": 342,
          "value": "true",
          "title": "Coding Exercises",
          "key": "has_coding_exercises"
        }
      ],
      "title": "Features",
      "id": "features"
    },
    {
      "options": [
        {
          "count": 10000,
          "value": "en",
          "title": "English",
          "key": "language"
        },
        {
          "count": 5671,
          "value": "es",
          "title": "Español",
          "key": "language"
        },

        {
          "count": 1,
          "value": "tt",
          "title": "татарча / Tatarça / تاتارچا",
          "key": "language"
        }
      ],
      "title": "Language",
      "id": "language"
    },
    {
      "options": [
        {
          "count": 10000,
          "value": "4.5",
          "title": "4.5 & up",
          "key": "ratings"
        },
        {
          "count": 10000,
          "value": "4.0",
          "title": "4.0 & up",
          "key": "ratings"
        },
        {
          "count": 10000,
          "value": "3.5",
          "title": "3.5 & up",
          "key": "ratings"
        },
        {
          "count": 10000,
          "value": "3.0",
          "title": "3.0 & up",
          "key": "ratings"
        }
      ],
      "title": "Ratings",
      "id": "ratings"
    },
    {
      "options": [
        {
          "count": 10000,
          "value": "short",
          "title": "0-2 Hours",
          "key": "duration"
        },
        {
          "count": 10000,
          "value": "medium",
          "title": "3-6 Hours",
          "key": "duration"
        },
        {
          "count": 9723,
          "value": "long",
          "title": "7-16 Hours",
          "key": "duration"
        },
        {
          "count": 2349,
          "value": "extraLong",
          "title": "17+ Hours",
          "key": "duration"
        }
      ],
      "title": "Duration",
      "id": "duration"
    }
  ]
    }
    '''

    status_codes = [500, 502, 503]

    for status_code in status_codes:
      with responses.RequestsMock() as rsps:        
        url_re = re.compile(r'.*udemy.com/api-2.0/courses.*')
        rsps.add(responses.GET, url_re,
                 body=mocked_json, status=status_code,
                 content_type='application/json',
                 match_querystring=True)
        rsps.add(responses.GET, url_re,
                 body=mocked_json, status=status_code,
                 content_type='application/json',
                 match_querystring=True)
        rsps.add(responses.GET, url_re,
                 body=mocked_good_json, status=200,
                 content_type='application/json',
                 match_querystring=True)        
        res = self.app.courses.get_all(page=1, page_size=2)
        self.assertEqual(sum(1 for _ in res), 2)    

        


if __name__ == "__main__":
    unittest.main()