import json
import sys

sys.path.insert(0, '../library/')

from service_azion import AzionAPI

api = AzionAPI()

## All
res = api.cdn_config()

## by ID
#res, st = api.cdn_config(cdn_id=1449590219)

## by NAME
#res, st = api.cdn_config(cdn_name='test-ansible')


#print st
print json.dumps(res, sort_keys=True, indent=4, separators=(',', ': '))
