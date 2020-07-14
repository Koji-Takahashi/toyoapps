from datetime import datetime
from slack.models import Message, SlackMember
from django.conf import settings

import requests
import json

from django.http import HttpResponse

url = "https://slack.com/api/users.list"
token = settings.SLACK_API_TOKEN
channel_id = settings.SLACK_CHANNEL_TOKEN


def create_user():
    payload = {
        "token": token,
        "channel": channel_id
        }
    response = requests.get(url, params=payload)
    json_data = response.json()
    members = json_data["members"]
    for i in members:
        if i["is_bot"] == True:
            continue
        if i["profile"]["real_name"] == 'Slackbot':
            continue

        if SlackMember.objects.filter(slack_id=i["id"]).exists():
            m = SlackMember.objects.get(slack_id=i["id"])
            m.slack_name = i["name"]
            # m.name = i["profile"]["real_name"]
        else:
            m = SlackMember(slack_id=i["id"], slack_name=i["name"], name=i["profile"]["real_name"])

        m.save()

    return 'OK'