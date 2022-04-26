# import requests
# import json
# response_API = requests.get('https://api.openalex.org/authors?filter=display_name.search:kavé-salamatian')
# #print(response_API.status_code)
# data = response_API.text
# parse_json = json.loads(data)

# for result in parse_json['results']:
#     print(result['ids'])

# ##https://api.openalex.org/works?filter=authorships.author.id:A166706192

from DB import DB
import configparser

if __name__ == "__main__":
    DB().getCursor()