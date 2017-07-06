# Copyright 2017 MTOps All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# from __future__ import print_function

import logging
import requests
# from requests.structures import CaseInsensitiveDict
# from .version import __version__

logger = logging.getLogger(__name__)

def _remove_null_values(dictionary):
    if isinstance(dictionary, dict):
        return dict([(k, v) for k, v in dictionary.items() if v is not None])
    return dictionary


def _cleanup_param_value(value):
    if isinstance(value, bool):
        return 'true' if value else 'false'
    return value


def _cleanup_param_values(dictionary):
    if isinstance(dictionary, dict):
        return dict(
            [(k, _cleanup_param_value(v)) for k, v in dictionary.items()])
    return dictionary


class ServiceException(Exception):
    pass


class ServiceInvalidArgument(ServiceException):
    pass


class APIService(object):
    """ Polymorphic class of API REST Service. """
    # __version__ = __version__

    def __init__(self, url_api, token_auth=None, token_sess=None,
                 username=None, password=None):
        """
        You can choose in setup initial authentication using username and
        password, or setup with Authorization HTTP token. If token_auth is set,
        username and password credentials must be ignored.
        """
        # self.__version__ = __version__
        self.url = url_api

        self.token_auth = token_auth
        self.token_sess = token_sess

        self.username = username
        self.password = password


    def set_token_auth(self, token_auth):
        if token_auth == 'YOUR AUTH TOKEN':
            token_auth = None

        self.token_auth = token_auth

    def set_uri(self, uri):
        self.uri = uri

    def get_version(self):
        return self.__version__

    def get_config(self):
        config = {
            'url': self.url,
            'token_auth': self.token_auth,
            'token_sess': self.token_sess,
            'username': self.username,
            'password': self.password
        }
        return config

    """
    Session Token (#TODO)
    """
    def api_has_session(self):
        """ #TODO: Ping session to check if token is not expired """
        return True

    """ Request """
    def request(self, method, url, accept_json=True, headers={},
                params=None, json=None, data=None, files=None, **kwargs):
        """
        Make a request to Rest API.
        @return Return response object.
        """

        # base API URL + path
        full_url = '%s/%s' % (self.url, url.strip('/'))
        input_headers = _remove_null_values(headers) if headers else {}

        # headers = CaseInsensitiveDict(
        #      {'user-agent': 'glpi-sdk-python-' + __version__})

        # TODO: make optional the version of json
        if accept_json:
            headers['accept'] = 'application/json; version=1'

        try:
            #if self.session is None:
            #    self.set_session_token()
            if self.token_sess is not None:
                headers.update({'Authorization':  "Token {}".format(self.token_sess)})
        except ServiceException as e:
            raise ServiceException("Unable to get Session token. ERROR: {}".format(e))

        # if self.token_auth is not None:
        #     headers.update({'App-Token': self.app_token})

        headers.update(input_headers)

        # Remove keys with None values
        params = _remove_null_values(params)
        params = _cleanup_param_values(params)
        json = _remove_null_values(json)
        data = _remove_null_values(data)
        files = _remove_null_values(files)

        try:
            response = requests.request(method=method, url=full_url,
                                        headers=headers, params=params,
                                        data=data, **kwargs)
        except Exception:
            logger.error("ERROR requesting uri(%s) payload(%s)" % (url, data))
            raise

        return response

    """ Generic Items methods """
    # [C]REATE - Create an Item
    def create(self, path, data_json=None):
        """ Create an object Item. """

        if (data_json is None):
            return "{ 'error_message' : 'Payload not found.'}"

        payload = '{}'.format(data_json)

        response = self.request('POST', path, data=payload, accept_json=True)

        return response.json()

    # [R]EAD - GET config
    def get_all(self, path):
        """ Return all content of Path in JSON format. """

        res = self.request('GET', path)
        return res.json()

    def get(self, path, item_id):
        """ Return the JSON item from path with ID item_id. """

        if isinstance(item_id, int):
            uri = '%s/%d' % (path, item_id)
            response = self.request('GET', uri)
            return response.json()
        else:
            return {'error_message': 'Unale to get %s ID [%s]' % (path,
                                                                  item_id)}

    def get_path(self, path=''):
        """ Return the JSON from path """
        response = self.request('GET', path)
        return response.json()

    # [U]PDATE - config
    ## Update fields
    def update(self, path, data):
        """ Update an object Item. """

        payload = '{}'.format(data)
        new_url = "%s/%d" % (path, data['id'])

        response = self.request('PATCH', new_url, data=payload)

        return response.json()

    ## Override config
    def override(self, path, data):
        """ Update an object Item. """

        payload = '{}'.format(data)
        new_url = "%s/%d" % (self.uri, data['id'])

        response = self.request('PUT', new_url, data=payload)

        return response.json()


    # [D]ELETE an Item
    def delete(self, path, item_id, force_purge=False):
        """ Delete an object Item. """

        if not isinstance(item_id, int):
            return {"message_error": "Please define item_id to be deleted."}

        if force_purge:
            payload = '{ "id": %d , "force_purge": true }' % (item_id)
        else:
            payload = '{ "id": %d }' % (item_id)

        response = self.request('DELETE', path, data=payload)
        return response.json()
