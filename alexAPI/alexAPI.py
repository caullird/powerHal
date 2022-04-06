import requests
import json
response_API = requests.get('https://api.openalex.org/authors?filter=display_name.search:salamatian')
#print(response_API.status_code)
data = response_API.text
parse_json = json.loads(data)

for result in parse_json['results']:
    print(result['display_name'])

