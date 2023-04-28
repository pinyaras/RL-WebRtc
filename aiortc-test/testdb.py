from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from datetime import datetime
token= "-F9itUm-zql_WrCDiBJuVRYBZd3O64jd2j71T2rnqb_x8-goHkjJ7NGt6u6CZiX0U0A5S6XjHwODC1NRq6eMCQ=="
org="winslab"
client = InfluxDBClient(url="http://localhost:8086", token=token, org=org)

# write_api = client.write_api()
write_api = client.write_api(write_options=SYNCHRONOUS)

# data =     {
#         "measurement": "MSFT_2021-11-07_Dictionary_Method", 
#         "tags": {"stock": "MSFT"}, 
#         "fields": {
#                 "Open": 66,
#                 "High": 63.38,
#                 "Low": 62.13,
#                 }, 
#         "time": int(datetime.strptime('2021-11-07','%Y-%m-%d').timestamp())
#     }
# write_api.write("webrtc", org, [data])


data = [
    {
        "measurement": "temperature",
        "tags": {
            "location": "room1"
        },
        "fields": {
            "value": 999
        }
    },
    {
        "measurement": "humidity",
        "tags": {
            "location": "room1"
        },
        "fields": {
            "value": 888
        }
    },
        {
        "measurement": "humidity",
        "tags": {
            "location": "room1"
        },
        "fields": {
            "value": 777
        }
    }
]
records = [
    {
        "measurement": "cpu",
        "tags": {"core": "0"},
        "fields": {"temp": 25.3},
        "time": 1657729063
    },
    {
        "measurement": "cpu",
        "tags": {"core": "0"},
        "fields": {"temp": 25.4},
        "time": 1657729078
    },
    {
        "measurement": "cpu",
        "tags": {"core": "0"},
        "fields": {"temp": 25.2},
        "time": 1657729093
    },
]

write_api.write("webrtc", org, records)

# client.write_api(write_options={"org": org}).write(bucket=bucket, record=data)

# write_api.write_data([
#     {
#         "measurement": "MSFT_2021-11-07_Dictionary_Method", 
#         "tags": {"stock": "MSFT"}, 
#         "fields": {
#                 "Open": 66,
#                 "High": 63.38,
#                 "Low": 62.13,
#                 }, 
#         "time": int(datetime.strptime('2021-11-07','%Y-%m-%d').timestamp())
#     },
#     {
#         "measurement": "MSFT_DATE", 
#         "tags": {"stock": "MSFT"}, 
#         "fields": {
#                 "Open": 67,
#                 "High": 63.38,
#                 "Low": 62.13,
#                 }, 
#     }
# ],write_option=ASYNCHRONOUS)