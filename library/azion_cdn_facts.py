#!/usr/bin/env python
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
module: azion_cdn_facts
version_added: "0.1.0"
short_description: Obtain facts about an AZION Content Delivery
description:
     - Describe AZION Content Delivery configuration
options:
  id:
    description:
      - the ID of CDN.
    required: true
  name:
    description:
      - the Name of CDN
    required: true
requirements: [ "azion" ]
author: Marco Tulio R Braga
'''

EXAMPLES = '''
# check facts for an CDN
- azion_cdn_facts:
    id: 128192381
'''

from collections import namedtuple
from ansible.module_utils.basic import AnsibleModule


try:
    import azion
    HAS_AZION_LIB = True
except ImportError:
    HAS_AZION_LIB = False
    # if __name__ == '__main__':
    #     raise


def azion_cdn_config(res, status):
    update_result = namedtuple('update_result', ('success', 'changed', 'message'))
    changed = False

    if status != 200:
        if not bool(res):
            success = True
            message = { "CDN": 'Not Found' }
        else:
            success = False
            message = { "CDN": 'Error: {}'.format(res) }
    else:
        success = True
        message = { "CDN": res }

    return update_result(success=success, changed=changed, message=message)


def azion_cdn_config_by_name(api, cdn_name):
    res, status = api.get_cdn_config(cdn_name=cdn_name)
    return azion_cdn_config(res, status)


def azion_cdn_config_by_id(api, cdn_id):
    res, status = api.get_cdn_config(cdn_id=cdn_id)
    return azion_cdn_config(res, status)


def main():

    module = AnsibleModule(argument_spec = dict(name = dict(type='str'),id = dict(type='int')) )

    if not HAS_AZION_LIB:
        module.fail_json(msg='azion lib is required for this module')

    if module.params.get('name') is None and module.params.get('id') is None:
        module.fail_json(msg='You should set name or id argument')

    try:
        azion_api = azion.AzionAPI()
    except Exception as e:
        module.fail_json(msg="Can't stablish connection - %s " % str(e))

    if module.params.get('name'):
        is_success, has_changed, msg = azion_cdn_config_by_name(azion_api, module.params.get('name'))
    else:
        is_success, has_changed, msg = azion_cdn_config_by_id(azion_api, module.params.get('id'))

    if is_success:
        module.exit_json(changed=has_changed, meta=msg)
    else:
        module.fail_json(msg=msg)


if __name__ == '__main__':
    main()
