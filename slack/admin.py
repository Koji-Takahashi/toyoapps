from django.contrib import admin
from .models import Department, Message, SlackMember, Seat
# Register your models here.

admin.site.register(Department)
admin.site.register(Message)
admin.site.register(SlackMember)
admin.site.register(Seat)

