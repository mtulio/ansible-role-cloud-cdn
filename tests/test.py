import json
import sys

sys.path.insert(0, '../library/')

from service_azion import AzionAPI

api = AzionAPI()

res = api.cdn_config(cdn_id=1406490960)
#res = api.cdn_config()

print json.dumps(res, sort_keys=True, indent=4, separators=(',', ': '))
