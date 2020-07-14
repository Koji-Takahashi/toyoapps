from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import SlackMemberForm, DepartmentForm
from django.db.models import Q
from django.contrib.auth.models import User
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from slack.get_slack_message import get_slack
from slack.create_random_number import GetNumber
from slack.get_slackuser_list import create_user
from slack.seat_json import GetSeat
from slack.models import Message, SlackMember, Department, Seat
from slack.update_status import update_status
# from .get_googleEvent import getGoogleEvent
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import(LoginView, LogoutView)


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = 'slack/login.html'

@login_required()
def index(request):
    """TOPメニュー"""
    return render(request,
                  'slack/index.html',  # 使用するテンプレート
                    )  # テンプレートに渡すデータ

@login_required()
def status(request, user_id, status):
    if SlackMember.objects.filter(account=user_id).exists():
        time_now = datetime.datetime.now()
        messages.add_message(request, messages.INFO, "ステータスが" + status + "に変更されました。 ( " + str(time_now) + " )")
        status = 'システム打刻　' + status
        user = SlackMember.objects.get(account=user_id)
        m = Message(user_code=user.slack_id, message=status,
                    encode_time=time_now)
        m.save()
        update_status();

    """TOPメニュー"""
    return render(request,
                  'slack/index.html',  )  # テンプレートに渡すデータ

@login_required()
def user_list(request):
    """User List"""
    users = SlackMember.objects.all()
    return render(request,
                  'slack/user_list.html',  # 使用するテンプレート
                  {'users': users}, )  # テンプレートに渡すデータ

@login_required()
def user_edit(request, pk):
    if pk:  # idがあるとき（編集の時）
        # idで検索して、結果を戻すか、404エラー
        member = get_object_or_404(SlackMember, pk=pk)
    else:  # idが無いとき（新規の時）
        # Memberを作成
        member = SlackMember()

    # POSTの時（新規であれ編集であれ登録ボタンが押されたとき）
    if request.method == 'POST':
        # フォームを生成
        form = SlackMemberForm(request.POST, instance=member)
        if form.is_valid():  # バリデーションがOKなら保存
            member = form.save(commit=False)
            member.save()
            return redirect('slack:user_list')
    else:  # GETの時（フォームを生成）
        form = SlackMemberForm(instance=member)
        slack_id = SlackMember.objects.get(pk=pk).slack_id
        messages = Message.objects.filter(user_code=slack_id).order_by("encode_time").reverse()

    # 新規・編集画面を表示
    return render(request, 'slack/member_edit.html', dict(form=form, id=id, messages=messages))

@login_required()
def department_list(request):
    """Department List"""
    departments = Department.objects.all()
    return render(request,
                  'slack/department_list.html',  # 使用するテンプレート
                  {'departments': departments}, )  # テンプレートに渡すデータ

@login_required()
def department_edit(request, pk=None):
    if pk:  # idがあるとき（編集の時）
        # idで検索して、結果を戻すか、404エラー
        member = get_object_or_404(Department, pk=pk)
    else:  # idが無いとき（新規の時）
        # Memberを作成
        member = Department()

    # POSTの時（新規であれ編集であれ登録ボタンが押されたとき）
    if request.method == 'POST':
        # フォームを生成
        form = DepartmentForm(request.POST, instance=member)
        if form.is_valid():  # バリデーションがOKなら保存
            member = form.save(commit=False)
            member.save()
            return redirect('slack:department_list')
    else:  # GETの時（フォームを生成）
        form = DepartmentForm(instance=member)
    # 新規・編集画面を表示
    return render(request, 'slack/department_edit.html', dict(form=form, id=id))

@login_required()
def comment_list(request):
    """メッセージの一覧"""
    # salckメッセージ取込
    get_slack();
    # ステータス更新
    update_status();
    # Google Event 取得
    # getGoogleEvent();

    departments = Department.objects.all()

    slacks = SlackMember.objects.all()
    keyword = request.GET.get('query')
    key = request.GET.get('key')
    print(key)
    if keyword:
        slacks = slacks.filter(
            Q(name__contains=keyword)
        )
    if key:
        slacks = slacks.filter(
            Q(department_id=key)
        )

    return render(request,
                  'slack/slack_index.html',  # 使用するテンプレート
                  {'slacks': slacks,
                   'departments': departments},)  # テンプレートに渡すデータ


def create_slack_menber(request):
    create_user();
    return HttpResponse('Create User')

@login_required()
def user_del(request, pk):
    """削除"""
    user_id=pk
    # return HttpResponse('削除')
    user = get_object_or_404(SlackMember, pk=user_id)
    user.delete()

    return redirect('slack:user_list')

@login_required()
def department_del(request, pk):
    """削除"""
    department_id=pk
    # return HttpResponse('削除')
    dp = get_object_or_404(Department, pk=department_id)
    dp.delete()

    return redirect('slack:department_list')

@login_required()
def create_seat(request ,user_id=None):
    user_id = user_id
    d = 52
    num = ''
    seat=''
    if user_id:
        num = GetNumber(d, user_id)
    if Seat.objects.filter(eventDate=now):
        seat=GetSeat(d)
    dict = {'num':num,'seat':seat}
    return render(request,
                  'slack/seat.html', dict )  # テンプレートに渡すデータ
