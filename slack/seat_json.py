import numpy as np
from .models import Seat, SlackMember
import datetime
import requests
from django.http import HttpResponse
import json

# d = 座席上限値
# user_id = アカウントと紐つける
def GetSeat(d):
    # 当日
    now = datetime.date.today()
    seat = []
    i = 1
    while i <= d:
        if Seat.objects.filter(eventDate=now, seat_number=i).exists():
            user_id = Seat.objects.filter(eventDate=now, seat_number=i)[0].user_id
            user = SlackMember.objects.filter(account=user_id).distinct()[0].name
            display = user
        else:
            display = i
        seat.append(display)
        i += 1

    # 在籍番号を返す。
    return (seat)

