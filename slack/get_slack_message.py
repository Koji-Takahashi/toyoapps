from datetime import datetime
from slack.models import Message
from django.conf import settings

import requests
import json

from django.http import HttpResponse

url = "https://slack.com/api/channels.history"
token = settings.SLACK_API_TOKEN
channel_id = settings.SLACK_CHANNEL_TOKEN
# token = "xoxp-847976834466-864385061718-1190486323670-4e330cad7028f9239fde01b40dcf7d74"
# channel_id = "C014TTRGNN4"

def get_slack():
    payload = {
        "token": token,
        "channel": channel_id
        }
    response = requests.get(url, params=payload)
    json_data = response.json()
    messages = json_data["messages"]
    for i in messages:
        # m = Message(post_time=i["ts"])
        if Message.objects.filter(post_time=i["ts"]).exists():
            # print(datetime.fromtimestamp(int(i["ts"])))
            m = Message.objects.get(post_time=i["ts"])
            m.user_code = i["user"]
            m.message = i["text"]
            m.encode_time = datetime.fromtimestamp(float(i["ts"]))
        else:
            m = Message(post_time=i["ts"], user_code=i["user"], message=i["text"], encode_time=datetime.fromtimestamp(float(i["ts"])))

        m.save()

    return 'OK'