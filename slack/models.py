from django.db import models

# Create your models here.
class Message(models.Model):
    """Message"""
    user_code = models.CharField('code', max_length=255)
    post_time =  models.CharField('postTime', max_length=255)
    message = models.TextField('message', max_length=50000, blank=True)
    slack_comment_id = models.CharField('message', max_length=255, blank=True)
    encode_time =  models.DateTimeField('postTimes', blank=True, null=True )

    def __str__(self):
        return self.message

class SlackMember(models.Model):
    """Message"""
    name = models.CharField('名前', max_length=255, null=True, blank=True)
    slack_name =  models.CharField('slack名', max_length=255)
    slack_id = models.CharField('slackId', max_length=255)
    status = models.CharField('ステータス', max_length=255, null=True, blank=True)
    update_time = models.DateTimeField('投稿時間', null=True, blank=True)
    department = models.ForeignKey('Department', verbose_name='部署',on_delete=models.SET_NULL, blank=True, null=True, related_name='department_name')
    account = models.CharField('アカウント', max_length=255, null=True, blank=True)
    flg_seat = models.CharField('座席不要フラグ', max_length=255, null=True, blank=True, default=0)

    def __str__(self):
        return self.name

class Department(models.Model):
    """部署"""
    BRANCH = (
        (10 , '本社'),
        (20 , '滋賀支店'),
        (30 , '舞鶴支店'),
    )

    name = models.CharField('部署名', max_length=255)
    branch = models.IntegerField('支店', choices=BRANCH, blank=True, null=True)

    def __str__(self):
        return self.name

class Events(models.Model):
    """Evens"""
    summary = models.TextField('summary', max_length=5000, blank=True, null=True)
    location = models.CharField('location', max_length=255, null=True, blank=True)
    startDate = models.CharField('startDate', max_length=255, null=True, blank=True)
    endDate = models.CharField('endDate', max_length=255, null=True, blank=True)
    iCalUID = models.TextField('iCalUID', blank=True, null=True, max_length=5000 )
    etag = models.CharField('etag', max_length=255, null=True, blank=True)
    googleEventId = models.CharField('etag', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.summary

class Seat(models.Model):
    """Seats"""
    seat_number = models.CharField('座席番号', max_length=255, null=True, blank=True)
    user_id = models.CharField('社員Id', blank=True, null=True, max_length=255 )
    eventDate = models.DateField('eventDate', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.seat_number
