import pandas as pd
import requests
import json
import our_secrets
import geopandas
from pathlib import Path

path_to_bezirksgrenzen = "bezirksgrenzen.geojson"
target_folder = "results"
retry_count = 5

def download_data(area, time):
  url = "https://telraam-api.net/v1/reports/traffic_snapshot"
  body = {
      "time":time,
      "contents":"minimal",
      "area":area
  }
  headers = {
    'X-Api-Key': our_secrets.telraamApiKey
  }
  payload = str(body)
  response = requests.request("POST", url, headers=headers, data=payload)
  if response.status_code == 200 :
    return response.json()
  else:
    # this is actually not true...but good enough
    print('error retrieving data for area {}'.format(area))
    return None

def get_gemeinde_boundaries():
  file = geopandas.read_file(path_to_bezirksgrenzen)
  for _, y in file.iterrows():
    yield y.Gemeinde_name, y.geometry.bounds


def get_normalized_boundary_string (a,b,c,d):
  """
    returnes a boundary string in the format that telraam uses: lon_ul,lat_ul,lon_br,lat_br

    whereas ul means upper left and br means bottom right.

    We asume the earth is not a sphere, which is sufficient true for small boundaries.
  """
  w = max(a,c)
  x = max(b,d)
  y = min(a,c)
  z = min(b,d)
  return ','.join(map(str, (w,x,y,z)))

def download_data_to_file(name, boundary, time, retry_count):
  print(name + " has boundaries {}".format(gemeinde_boundaries))
  a,b,c,d = gemeinde_boundaries
  formatted_boundaries = get_normalized_boundary_string(a,b,c,d)
  data = download_data(formatted_boundaries, time)
  if(data is not None):
 #   for feature in data["features"]:
 #       id = feature["properties"]["segment_id"]
    print("Found {} features.".format(len(data["features"])))
    with open(target_folder + "/" + name + ".json", 'w') as f:
      json.dump(data, f)

  else:
    # Sometimes the api just returns an error I do not understand, retry it sometimes succeeds
    if(retry_count > 1):
      print("retrying...trys remaining: {}".format(retry_count - 1))
      download_data_to_file(name, boundary, time, retry_count - 1)

def ensure_results_path_exists():
  Path(target_folder).mkdir(parents=True, exist_ok=True)

def test():
  url = "https://telraam-api.net/v1/reports/traffic"
  body = {
      "level":"segments",
      "format":"per-hour",
      "id": "9000001463",
  "time_start": "2024-03-12 07:00:00Z",
  "time_end": "2024-06-08 09:00:00Z"
  }
  headers = {
    'X-Api-Key': our_secrets.telraamApiKey
  }
  payload = str(body)
  response = requests.request("POST", url, headers=headers, data=payload)
  jsonObj = response.json()
  with open("test.json", 'w') as f:
    json.dump(jsonObj, f)

test()
# if __name__ == '__main__':
#   time = "2021-06-25 10:00:00Z"
#   ensure_results_path_exists()
#   for name, gemeinde_boundaries in get_gemeinde_boundaries():
#     download_data_to_file(name, gemeinde_boundaries, time, retry_count)