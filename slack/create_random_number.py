import numpy as np
from .models import Seat
import datetime
import requests
from django.http import HttpResponse

# d = 座席上限値
# user_id = アカウントと紐つける
def GetNumber(d, user_id):
    # 当日
    now = datetime.date.today()
    # 当日既に座席が発行されていたら既に決まった番号を返す
    if Seat.objects.filter(eventDate=now, user_id=user_id).exists():
        # データベースに保持された座席番号を返す
        d = Seat.objects.get(eventDate=now, user_id=user_id)
        ran = d.seat_number
    else:
        # ランダムの座席番号を生成する
        f = True
        while f == True :
            # ランダム整数を生成する
            ran = np.random.randint(d)
            # 生成された数字が既に誰かに取られていないか確認する
            f = Seat.objects.filter(eventDate=now, seat_number=ran).exists()
            if f == False :
                # 座席レコード作成する
                s = Seat(eventDate=now, user_id=user_id, seat_number=ran)
                s.save()
    # 在籍番号を返す。
    return (ran)

