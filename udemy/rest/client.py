# -*- coding: utf-8 -*-
"""
UdemyApp API Python Client
"""

import logging
import os
import json
import requests
import time
import base64
from pprint import pformat
from posixpath import join as urljoin
# from udemy.dto import Course

logger = logging.getLogger('udemy')
logger.handlers = []
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.ERROR)

CLIENT_VERSION = '2.2.3'
OS_VER = os.sys.platform
PYTHON_VERSION = '.'.join(
    map(str, [os.sys.version_info.major, os.sys.version_info.minor,
              os.sys.version_info.micro]))

RETRIES = 2  # if connections fail retry couple of times
CONNECTIONS = 20  # Number of connections to maintain in Pool


class UdemyApp(object):
    ''' UdemyApp Application object
        This is the entry point of the Udemy Client Api.
        With authentication to an application, you can access
        all the coursesreviews-list, courses-detail,
        courses-list and publiccurriculum-list
    '''

    def __init__(self,
                 client_id=None,
                 client_secret=None,
                 base_url=None,
                 quiet=True,
                 log_level=None
                 ):

        self.api = ApiClient(
                    client_id=None,
                    client_secret=None,
                    base_url=None,
                    quiet=True,
                    log_level=log_level)
        self.courses = Courses(self.api)


class Courses(object):
    """
    Handles all requests related to courses.
    ie; gets the courses-list, courses-detail, coursesreviews-list
    """

    def __init__(self, api):
        self.api = api        

    def get_all(self, page, page_size):        
        no_of_page = 1        
        while True and page >= no_of_page:
            
            res = self._get_courses_detail(page, page_size)            
            if not res['results']:
                break            
            for one in res['results']:                
                course = self._to_obj(one)
                yield course

            no_of_page += 1

    def _get_courses_detail(self, page, page_size):
        resource = "courses"
        params = {'page': page, 'page_size': page_size,
#                   'fields[course]': '@all'
                  }
        res = self.api.get(resource, params)
        return res

    def _to_obj(self, item):
        return Course(item)

class ApiClient(object):
    """
    Handles auth making requests.
    The constructor for api access.
    Args:
        self: instance of Apiclient
        api_key: the API key used, used for authentication.
        quiet: if True the silence debug prints.
        log_level: log level for logging module.
    """
    def __init__(self,
                 client_id=None,
                 client_secret=None,
                 base_url=None,
                 quiet=True,
                 log_level=None
                 ):
        if not log_level:
            if quiet:
                log_level = logging.ERROR
            else:
                log_level = logging.DEBUG
        logger.setLevel(log_level)

        if not client_id:
            client_id = self._read_client_id_from_env_or_os()
        self.client_id = client_id

        if not client_secret:
            client_secret = self._read_client_secret_from_env_or_os()
        self.client_secret = client_secret

        if not base_url:
            base_url = self._read_base_from_env_or_os()
        self.basev2 = base_url

        self.session = requests.Session()
        http_adapter = requests.adapters.HTTPAdapter(
                        max_retries=RETRIES, pool_connections=CONNECTIONS,
                        pool_maxsize=CONNECTIONS)
        self.session.mount('http://', http_adapter)
        self.session.mount('https://', http_adapter)

        usrPass = self.client_id+":"+self.client_secret
        b64Val = base64.b64encode(usrPass)
        self.headers = {"Authorization": "Basic %s" % b64Val}
        logger.debug('Headers')

    def _read_client_id_from_env_or_os(self):
        env_client_id = os.environ.get('UDEMY_CLIENT_ID')
        if env_client_id:
            logger.debug("Using env variable UDEMY_CLIENT_ID for CLIENT ID")
            return env_client_id
        else:
            raise Exception("CLIENT ID not set in the environment variable")

    def _read_client_secret_from_env_or_os(self):
        env_client_secret = os.environ.get('UDEMY_CLIENT_SECRET')
        if env_client_secret:
            logger.debug("Using env variable UDEMY_CLIENT_SECRET for CLIENT SECRET")
            return env_client_secret
        else:
            raise Exception("CLIENT SECRET not set in the environment "
                            "variable")

    def _read_base_from_env_or_os(self):
        base_url = os.environ.get('UDEMY_BASE_URL')
        if base_url:
            logger.debug("Using env variable UDEMY_BASE_URL for Base URL")
            return base_url
        else:
            raise Exception("BASE URL not set in the environment variable")

    def _requester(self, resource, params, method, version="v2"):
        """ Obtains info and verifies user via Token Decorator

        Args:
          resource:
          params: parameters passed to the request
          version: v1 or v2
          method: GET or POST or DELETE or PATCH
    
        Returns:
          JSON from user request
        """

#     self._check_token()
        url = urljoin(self.basev2, resource)        
    
        # only retry under when status_code is non-200, under max-tries
        # and under some circumstances
        status_code = 199
        retry = True
        max_attempts = attempts = 3
        headers = {}
    
        while status_code != 200 and attempts > 0 and retry is True:
    
          logger.debug("=" * 100)
        
          logger.debug("%s %s\nHEADERS:\n%s\nPAYLOAD:\n%s", method, url,
                       pformat(self.headers), pformat(params))          
          if method == 'GET':
#             headers = {
#                 'Content-Type': 'application/json',
#                 'X-Udemy-Client': 'python:%s' % CLIENT_VERSION,
#                 'Python-Client': '%s:%s' % (OS_VER, PYTHON_VERSION),
#                 'Authorization': self.headers['Authorization']
#             }            
            res = self.session.get(url, params=params, headers=self.headers)
          elif method == "POST":
#             headers = {
#                 'Content-Type': 'application/json',
#                 'X-Udemy-Client': 'python:%s' % CLIENT_VERSION,
#                 'Python-Client': '%s:%s' % (OS_VER, PYTHON_VERSION),
#                 'Authorization': self.headers['Authorization']
#             }
            res = self.session.post(url, data=json.dumps(params), headers=headers)
          elif method == "DELETE":
#             headers = {
#                 'Content-Type': 'application/json',
#                 'X-Udemy-Client': 'python:%s' % CLIENT_VERSION,
#                 'Python-Client': '%s:%s' % (OS_VER, PYTHON_VERSION),
#                 'Authorization': self.headers['Authorization']
#             }
            res = self.session.delete(url, data=json.dumps(params), headers=headers)          
          else:
            raise UserError("Unsupported request type: '%s'" % method)
    
          try:
            js = res.json()
          except Exception:
            logger.exception("Could not get valid JSON from server response.")
            logger.debug("\nRESULT:\n%s", pformat(res.content.decode('utf-8')))
            return res

          logger.debug("\nRESULT:\n%s", pformat(json.loads(res.content.decode('utf-8'))))
    
          status_code = res.status_code          
          attempts -= 1
    
          # allow retry when token expires
          # normally, this should be solved in one retry
          if status_code == 401 and isinstance(js, dict) and js.get('status', {}).get('details',
                                                                                      '') == \
              "expired token":
            logger.warn("%s", str(ApiError(resource, params, method, res, self)))
#             self.get_token()
            retry = True
            continue

          # handle Gateway Error, normally retry will solve the problem
          if int(status_code / 100) == 5:
            logger.warn("%s", str(ApiError(resource, params, method, res, self)))
            retry = True
            continue

          # handle throttling
          # back off with 2/4/8 seconds
          # normally, this will be settled in 1 or 2 retries
          if status_code == 429:
            logger.warn("%s", str(ApiError(resource, params, method, res, self)))
            retry = True
            time.sleep(pow(2, max_attempts - attempts - 1))
            continue

          # in other cases, error out without retrying
          retry = False

        if res.status_code != 200:
          logger.debug("Failed after %d retrie(s)" % (max_attempts - attempts))
          raise ApiError(resource, params, method, res, self)

        return res.json()

    def get(self, resource, params=None, version="v2"):
        """ Authorized get from Udemy's API. """
        return self._requester(resource, params, 'GET', version)



class Course(object):
    def __init__(self, item=None):        
        self._class = item['_class']
        self.id = item['id']        
        self.title = item['title']
        self.url = item['url']
        self.is_paid = item['is_paid']
        self.price = item['price']
        self.price_detail = PriceDetail(item=item['price_detail'])
        self.visible_instructors = []
        for each in item['visible_instructors']:
          self.visible_instructors.append(Instructor(item=each))     
        self.image_125_H = item['image_125_H']             
        self.image_240x135 = item['image_240x135']
        self.is_practice_test_course = item['is_practice_test_course']
        self.image_480x270 = item['image_480x270']
        self.published_title = item['published_title']
        self.predictive_score = item['predictive_score']
        self.relevancy_score = item['relevancy_score']
        self.input_features = item['input_features']                                
        self.lecture_search_result = item['lecture_search_result']        


class Instructor(object):
    def __init__(self, item=None):
        self.name = item['name']
        self.url = item['url']
        self.display_name = item['display_name']        
        self.image_50x50 = item['image_50x50']
        self.initials = item['initials']
        self._class = item['_class']
        self.job_title = item['job_title']
        self.image_100x100 = item['image_100x100']        
        self.title = item['title']                                        


class PriceDetail(object):
    def __init__(self, item):
        self.price_string = None
        self.amount = None
        self.currency_symbol = None
        self.currency = None


class TokenError(Exception):
  pass


class ApiError(Exception):
  """ API Server error """

  def __init__(self, resource, params, method, response, api):
    self.resource = resource
    self.params = params
    self.method = method
    self.response = response
    self.api = api

    self.error_code = response.json().get('status', {}).get('code', None)
    self.error_desc = response.json().get('status', {}).get('description', None)
    self.error_details = response.json().get('status', {}).get('details', None)

    current_ts_str = str(time.time())

    msg = """%(method)s %(baseurl)s%(resource)s FAILED(%(time_ts)s). status_code: %(status_code)d, reason: %(reason)s, error_code: %(error_code)s, error_description: %(error_desc)s, error_details: %(error_details)s
 >> Python client %(client_version)s with Python %(python_version)s on %(os_version)s
 >> %(method)s %(baseurl)s%(resource)s
 >> REQUEST(%(time_ts)s) %(request)s
 >> RESPONSE(%(time_ts)s) %(response)s""" % {
        'baseurl': '%s/v2/' % self.api.basev2,
        'method': method,
        'resource': resource,
        'status_code': response.status_code,
        'reason': response.reason,
        'error_code': self.error_code,
        'error_desc': self.error_desc,
        'error_details': self.error_details,
        'request': json.dumps(params, indent=2),
        'response': json.dumps(response.json(), indent=2),
        'time_ts': current_ts_str,
        'client_version': CLIENT_VERSION,
        'python_version': PYTHON_VERSION,
        'os_version': OS_VER
    }

    super(ApiError, self).__init__(msg)

    # def __str__(self):
    #   parent_str = super(ApiError, self).__str__()
    #   return parent_str + str(self.json)


class ApiClientError(Exception):
  """ API Client Error """


class UserError(Exception):
  """ User Error """        

