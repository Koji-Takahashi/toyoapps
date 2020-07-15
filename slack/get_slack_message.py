from datetime import datetime
from slack.models import Message
from django.conf import settings

import requests
import json

from django.http import HttpResponse

url = "https://slack.com/api/channels.history"
token = settings.SLACK_API_TOKEN
channel_id = settings.SLACK_CHANNEL_TOKEN


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
            m.save()
        elif i.get("user"):
            m = Message(post_time=i["ts"], user_code=i["user"], message=i["text"], encode_time=datetime.fromtimestamp(float(i["ts"])))
            m.save()

    return 'OK'
