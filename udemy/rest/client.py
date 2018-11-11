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
        logger.debug("courses initialized")

    def get_all(self):
        print("I'm here")
        logger.debug("courses initialized")
        page = 1
        per_page = 20

        while True:
            res = self.api.get_courses(page, per_page)
            print 'res = ', res
            if not res['results']:
                break

            try:
                for one in res['results']:
                    print 'hello'
                    yield one
            except Exception  as e:
                print(e)
            break

        page += 1


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
    
    #       # mangle the base64 because it is too long
    #       if params and params.get('inputs') and len(params['inputs']) > 0:
    #         params_copy = copy.deepcopy(params)
    #         for data in params_copy['inputs']:
    #           data = data['data']
    #           if data.get('image') and data['image'].get('base64'):
    #             base64_bytes = data['image']['base64'][:10] + '......' + data['image']['base64'][-10:]
    #             data['image']['base64'] = base64_bytes
    #           if data.get('video') and data['video'].get('base64'):
    #             base64_bytes = data['video']['base64'][:10] + '......' + data['video']['base64'][-10:]
    #             data['video']['base64'] = base64_bytes
    #       elif params and params.get('query') and params['query'].get('ands'):
    #         params_copy = copy.deepcopy(params)
    # 
    #         queries = params_copy['query']['ands']
    # 
    #         for query in queries:
    #           if query.get('output') and query['output'].get('input') and \
    #               query['output']['input'].get('data') and \
    #               query['output']['input']['data'].get('image') and \
    #               query['output']['input']['data']['image'].get('base64'):
    #             data = query['output']['input']['data']
    #             base64_bytes = data['image']['base64'][:10] + '......' + data['image']['base64'][-10:]
    #             data['image']['base64'] = base64_bytes
    #       else:
    #         params_copy = params
          # mangle the base64 because it is too long
    
          logger.debug("%s %s\nHEADERS:\n%s\nPAYLOAD:\n%s", method, url,
                       pformat(self.headers), pformat(params))
    
          if method == 'GET':
#             headers = {
#                 'Content-Type': 'application/json',
#                 'X-Clarifai-Client': 'python:%s' % CLIENT_VERSION,
#                 'Python-Client': '%s:%s' % (OS_VER, PYTHON_VERSION),
#                 'Authorization': self.headers['Authorization']
#             }            
            res = self.session.get(url, params=params, headers=self.headers)
          elif method == "POST":
#             headers = {
#                 'Content-Type': 'application/json',
#                 'X-Clarifai-Client': 'python:%s' % CLIENT_VERSION,
#                 'Python-Client': '%s:%s' % (OS_VER, PYTHON_VERSION),
#                 'Authorization': self.headers['Authorization']
#             }
            res = self.session.post(url, data=json.dumps(params), headers=headers)
          elif method == "DELETE":
#             headers = {
#                 'Content-Type': 'application/json',
#                 'X-Clarifai-Client': 'python:%s' % CLIENT_VERSION,
#                 'Python-Client': '%s:%s' % (OS_VER, PYTHON_VERSION),
#                 'Authorization': self.headers['Authorization']
#             }
            res = self.session.delete(url, data=json.dumps(params), headers=headers)
          elif method == "PATCH":
#             headers = {
#                 'Content-Type': 'application/json',
#                 'X-Clarifai-Client': 'python:%s' % CLIENT_VERSION,
#                 'Python-Client': '%s:%s' % (OS_VER, PYTHON_VERSION),
#                 'Authorization': self.headers['Authorization']
#             }
            res = self.session.patch(url, data=json.dumps(params), headers=headers)
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
        """ Authorized get from Clarifai's API. """
        return self._requester(resource, params, 'GET', version)

    def get_courses(self, page, per_page):
        resource = "courses"
        params = {'page': page, 'per_page': per_page,
#                   'fields[course]': '@all'
                  }

        res = self.get(resource, params)
        return res

