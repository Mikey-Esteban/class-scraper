import os
import csv
import requests
from helpers import *
from datetime import datetime, timedelta
from json import dumps

path = f'./csv/{get_date()}/social'
files = os.listdir(path)

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

date = dumps(datetime.now()+timedelta(1), default=json_serial)
prod_url = 'https://community-artistry-api.fly.dev/api/v1/social_media_classes'
local_url = 'http://127.0.0.1:3000/api/v1/social_media_classes'


for f in files:
    print(f)

    with open(f'{path}/{f}', newline='') as csvfile:

        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

        for i, row in enumerate(spamreader):
            if i == 0: continue
        
            data = {
                'studio': row[0],
                'start_time': row[1],
                'name': row[2],
                'instructor': row[3],
                'date': date
            }

            x = requests.post(prod_url, json = data)
            print(x)
        
