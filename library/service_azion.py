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
#
# Azion API documentation:
# https://www.azion.com.br/developers/api/

# from __future__ import print_function
import os
import sys
import logging
import time

# from .version import __version__
from service_api import APIService, ServiceException


logger = logging.getLogger(__name__)


class AzionAPI(APIService):
    """
    Generic implementation of Azion API to manage main configs.
    """
    # __version__ = __version__

    def __init__(self, url_api=None, token=None, token_type='session'):
        """ Construct generic object """

        if url_api is None:
            url_api = 'https://api.azion.net'

        self.routes = {
            'cdn_config': '/content_delivery/configurations'
        }

        # throtle defined by API - HTTP 429 https://www.azion.com.br/developers/api/
        self.throtle_limit_min = 20

        if token_type == 'session':
            if token is None:
                try:
                    token = os.getenv("AZION_TOKEN") or None
                except:
                    raise ('Unable to get Session token AZION_TOKEN from env')

        #TODO
        elif token_type == 'auth':
            if token is None:
                try:
                    token = os.getenv("AZION_BASE64") or None
                except:
                    raise ('Unable to get Base64 auth token AZION_BASE64 from env')
            raise ('Unable to get Base64 auth token AZION_BASE64 from env'
            sys.exit(1)

        # force use session token
        APIService.__init__(self, url_api, token_sess=token)


    # AZION CDN Operations / abstraction
    # CDN abstraction
    def cdn_config_expanded(self, cdn_config):
        """
        Expand all config in a dict. The config available are:
        * digital_certificate
        * origin - /content_delivery/configurations/:conf_id/origins
        * cache_settings - /content_delivery/configurations/:conf_id/cache_settings
        * rules_engine /content_delivery/configurations/:conf_id/rules_engine
        """
        # print repr(cdn_config)
        path = '{}/{}/origins'.format(self.routes['cdn_config'], cdn_config['id'])
        cdn_config['origins'] = self.get_all(path)

        path = '{}/{}/cache_settings'.format(self.routes['cdn_config'], cdn_config['id'])
        cdn_config['cache_settings'] = self.get_all(path)

        path = '{}/{}/rules_engine'.format(self.routes['cdn_config'], cdn_config['id'])
        cdn_config['rules_engine'] = self.get_all(path)

        return cdn_config

    def cdn_config(self, cdn_id=None):
        """
        Get all resources from item_name.
        cdn_id is a ID for CDN and if is None, will return config from all CDNs
        """
        try:
            if not self.api_has_session():
                self.init_api()

            if cdn_id is None:
                cfg_all = self.get_all(self.routes['cdn_config'])
                total = len(cfg_all)
                count = 1
                for c in cfg_all:
                    print "expanding config for ", repr(c)
                    if count > (self.throtle_limit_min - 3):
                        print ("Avoiding Throtle {} of {}. Waiting 50s".format(count,
                                                        self.throtle_limit_min))
                        time.sleep(50)
                        count = 0

                    cfg.append(self.cdn_config_expanded(c))
                    count += 3
                return cfg
            else:
                path = '{:s}/{:d}'.format(self.routes['cdn_config'], cdn_id)
                c = self.get_all(path)
                return self.cdn_config_expanded(c)

        except ServiceException as e:
            return {'{}'.format(e)}
