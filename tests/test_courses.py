#!/usr/bin/python
# -*- coding: latin-1 -*-
'''
Created on Aug 26, 2018

@author: prem
'''
import unittest
import logging
import os
import responses
import re
from udemy.rest.client import UdemyApp, ApiClient, Course


class TestApiCourses(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = UdemyApp(log_level=logging.INFO)

    def tearDown(self):
        pass

    def test_get_all_courses(self):    	
    	
		mocked_good_json = '''{		  
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
		    }
    		'''
		
		with responses.RequestsMock() as rsps:
	   		url_re = re.compile(r'.*udemy.com/api-2.0/courses.*')
	    	rsps.add(responses.GET, url_re,
	    		body=mocked_good_json, status=200,
	    		content_type='application/json',
	    		match_querystring=True)
	    	courses = self.app.courses.get_all(page=1, page_size=2)
	    	for course in courses:	        	
	        	self.assertTrue(isinstance(course, Course))
	      		self.assertTrue(hasattr(course, 'id'))
	      		self.assertTrue(hasattr(course, 'title'))      		
	      		self.assertIsNotNone(course.id)        


if __name__ == "__main__":
    unittest.main()