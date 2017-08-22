#!/usr/bin/env python
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
module: azion_cdn
version_added: "0.1.0"
short_description: Obtain facts about an AZION Content Delivery
description:
     - Describe AZION Content Delivery configuration
options:
  name:
    description:
      - the Name of CDN
    required: true
  state:
    description:
      - create (no destroy yet) the CDN configuration
    required: true
    choices: [present, absent]
    default: 'present'
  payload:
    description:
      - payload to create CDN request
    required: no
requirements: [ "azion" ]
author: Marco Tulio R Braga
'''

EXAMPLES = '''
# check facts for an CDN
- azion_cdn:
    name: test-ansible
    state: preset
    payload: |
        {
              "name": "teste-ansible",
              "origin_address": "domain.teste-ansible.com",
              "cname_access_only": true,
              "cname": ["www1.teste-ansible.com"],
              "delivery_protocol": "http",
              "cdn_cache_settings": "override",
              "cdn_cache_settings_minimum_ttl": 2592000,
              "origin_protocol_policy": "preserve",
         }
'''

from collections import namedtuple
from ansible.module_utils.basic import AnsibleModule


try:
    import azion
    HAS_AZION_LIB = True
except ImportError:
    HAS_AZION_LIB = False


def azion_cdn_result(res, status):
    update_result = namedtuple('update_result', ('success', 'changed', 'message'))
    changed = False

    if status != 200:
        if 'name' in res:
            success = True
            message = { "CDN exists": res }

        elif not bool(res):
            success = True
            message = { "CDN": 'Not Found. {} {}'.format(status, repr(res)) }

        else:
            success = False
            message = { "CDN": 'Error {}: {}'.format(status, res) }
    else:
        success = True
        message = { "CDN": res }

    return update_result(success=success, changed=changed, message=message)


def azion_cdn_create(api, cdn_name, cdn_payload=None):
    """Call to library SDK to create CDN."""
    res, status = api.create_cdn(cdn_name, cdn_payload=cdn_payload)
    return azion_cdn_result(res, status)


def main():

    module = AnsibleModule(argument_spec = dict(
                                    name = dict(type='str'),
                                    state = dict(type='str'),
                                    payload = dict(type='str')
                                )
                            )

    if not HAS_AZION_LIB:
        module.fail_json(msg='azion lib is required for this module')

    if module.params.get('name') is None:
        module.fail_json(msg='You should set the name of CDN configuration')
    if module.params.get('state') is None:
        module.fail_json(msg='You should set the state of CDN configuration')
    if module.params.get('state') != 'present':
        module.fail_json(msg='The state can be "present"')

    try:
        azion_api = azion.AzionAPI()
    except Exception as e:
        module.fail_json(msg="Can't stablish connection - %s " % str(e))

    is_success, has_changed, msg = azion_cdn_create(azion_api,
                                    module.params.get('name'),
                                    module.params.get('payload'))

    if is_success:
        module.exit_json(changed=has_changed, meta=msg)
    else:
        module.fail_json(msg=msg)


if __name__ == '__main__':
    main()
