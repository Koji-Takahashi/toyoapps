from django.urls import path
from slack import views
from django.contrib.auth import views as auth_views

app_name = 'slack'
urlpatterns = [
    # slack
    path('', views.index, name='index'),   # 一覧
    path('login/', auth_views.LoginView.as_view(template_name='slack/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('status/<int:user_id>/<str:status>/', views.status, name='status'),   # ステータス修正
    path('create_seat/<int:user_id>/', views.create_seat, name='create_seat'),   # 座席を発行する
    path('user_list/', views.user_list, name='user_list'),   # user一覧
    path('user/<int:pk>/', views.user_edit, name='user_edit'),  # 詳細
    path('user/del/<int:pk>/', views.user_del, name='user_del'),  # 削除
    path('comment/', views.comment_list, name='comment_list'),   # 一覧
    path('department_list/', views.department_list, name='department_list'),  # 一覧
    path('department/<int:pk>/', views.department_edit, name='department_edit'),  # 詳細
    path('department/add/', views.department_edit, name='department_add'),  # 詳細
    path('department/del/<int:pk>/', views.department_del, name='department_del'),  # 削除
    path('create_user/', views.create_slack_menber, name='create_slack_menber'),   # ユーザー作成
]
