import time
from datetime import datetime

import requests


def print_message(message):
    dt = datetime.fromtimestamp(message['time'])
    dt_str = dt.strftime('%d %b %H:%M:%S')
    print(dt_str, message['name'])
    print(message['text'])
    print()


after = 0

while True:
    response = requests.get(
        'http://127.0.0.1:5000/messages',
        params={'after': after}
    )
    messages = response.json()['messages']
    for message in messages:
        print_message(message)
        after = message['time']

    time.sleep(1)
