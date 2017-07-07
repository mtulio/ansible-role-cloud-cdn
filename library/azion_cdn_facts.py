#!/usr/bin/env python
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
module: azion_cdn_facts
version_added: "0.1"
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
    import os, sys
    sys.path.append(os.path.join(os.path.dirname(__file__)))

    from service_azion import AzionAPI
    HAS_AZION_LIB = True
except ImportError:
    HAS_AZION_LIB = False
    if __name__ == '__main__':
        raise

def azion_cdn_config_by_name(cdn_name):
    """ TODO """
    update_result = namedtuple('update_result', ('success', 'changed', 'message'))
    changed = False
    return update_result(success=True, changed=changed, message={'name': cdn_name})
    return update_result

def azion_cdn_config_by_id(cdn_id):
    update_result = namedtuple('update_result', ('success', 'changed', 'message'))
    changed = False

    api = AzionAPI()
    res = api.cdn_config(cdn_id=cdn_id)

    return update_result(success=True, changed=changed, message={'cdn': res})
    return cdn_id

def main():

    module = AnsibleModule(argument_spec = dict(name = dict(type='str'),id = dict(type='int')) )

    if not HAS_AZION_LIB:
        module.fail_json(msg='azion lib is required for this module')

    if module.params.get('name') is None and module.params.get('id') is None:
        module.fail_json(msg='You should set name or id argument')

    try:
        azion_api = AzionAPI()
    except Exception as e:
        module.fail_json(msg="Can't stablish connection - %s " % str(e))

    if module.params.get('name'):
        is_success, has_changed, msg = azion_cdn_config_by_name(module.params.get('name'))
    else:
        is_success, has_changed, msg = azion_cdn_config_by_id(module.params.get('id'))

    if is_success:
        module.exit_json(changed=has_changed, meta=msg)
    else:
        module.fail_json(msg=msg)

if __name__ == '__main__':
    main()
