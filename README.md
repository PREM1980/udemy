[![Build Status](https://travis-ci.org/PREM1980/udemy.svg?branch=master)](https://travis-ci.org/PREM1980/udemy)
[![Coverage Status](https://coveralls.io/repos/github/PREM1980/udemy/badge.svg?branch=master)](https://coveralls.io/github/PREM1980/udemy?branch=master)


# Udemy app

This package calls the REST end-points given in this page, and
tries to loads the data into a SQL-lite database. 


	
	
# Setup

First, generate a API key as provided in this link - 

https://www.udemy.com/developers/affiliate/

Then to authenticate, either

1. Set the following environment variables - 
```
	UDEMY_CLIENT_ID='XXXXXXXXXXXXXXXXX'
	UDEMY_CLIENT_SECRET='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
	UDEMY_BASE_URL='https://www.udemy.com/api-2.0/'
```

2. initialize the UdemyApp with client id, secret and base url.

```
from udemy.rest.client import UdemyApp, ApiClient, Course
app=UdemyApp(client_id='xxxx', client_secret='xxxx', base_url='xxxxx')

```

# Getting started

The following example will setup the client and displays all the courses.

```
from udemy.rest.client import UdemyApp, ApiClient, Course
app=UdemyApp()
for course in app.courses.get_all(page=1,page_size=10):
	print(course.id, course.title)
```

Note:- You can change the page parameter and page_size according to your needs.

The response is a Python object.
```
(567828, u'Complete Python Bootcamp: Go from zero to hero in Python 3')
(362328, u'AWS Certified Solutions Architect - Associate 2018')
(625204, u'The Web Developer Bootcamp')
(756150, u'Angular 7 (formerly Angular 2) - The Complete Guide')
(950390, u'Machine Learning A-Z\u2122: Hands-On Python & R In Data Science')
(533682, u'Java Programming Masterclass for Software Developers')
(874012, u'The Ultimate Drawing Course - Beginner to Advanced')
(258316, u'Complete C# Unity Developer 2D: Learn to Code Making Games')
(764164, u'The Complete Web Developer Course 2.0')
(793796, u'Microsoft Excel - Excel from Beginner to Advanced')
```
