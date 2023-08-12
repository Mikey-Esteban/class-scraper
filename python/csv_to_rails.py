import os
import csv
import requests
from helpers import *
from datetime import datetime, timedelta
from json import dumps

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

test_path = f'./csv/22_03_2023/styles'
test_date = dumps(datetime.now()-timedelta(1), default=json_serial)

path = f'./csv/{get_date()}/styles'
files = os.listdir(path)

date = dumps(datetime.now()+timedelta(1), default=json_serial)
prod_url = 'https://community-artistry-api.fly.dev/api/v1/social_media_classes'
local_url = 'http://127.0.0.1:3000/api/v1/social_media_classes'


studio_dict = {
    'contemporary_modern': 'Contemporary/Modern',
    'theater': 'Theater',
    'jazz': 'Jazz',
    'tap': 'Tap',
    'additional_disciplines': 'Additional Disciplines',
    'world': 'World',
    'street_styles_choreography': 'Street Styles/Choreography',
    'ballet': 'Ballet',
}

for f in files:
    f_name = os.path.splitext(f)[0]
    print(f_name)

    with open(f'{path}/{f}', newline='') as csvfile:

        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

        for i, row in enumerate(spamreader):
            if i == 0: continue

            time = datetime.timestamp(datetime.strptime(row[1].lower(), '%I:%M%p'))

            data = {
                'studio': row[0],
                'start_time': int(time),
                'name': row[2],
                'instructor': row[3],
                'date': date,
                'style': studio_dict[f_name],
                'sign_up': row[4]
            }

            x = requests.post(local_url, json = data)
            print(x)
        
