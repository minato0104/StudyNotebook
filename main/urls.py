from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),  # メニュー
    path('study-group/', views.study_group_view, name='study_group'),  # 勉強グループ
    path('create-group/', views.create_group_view, name='create_group'),  # 勉強グループを作る
    path('study-group/<int:group_id>/', views.study_group_detail_view, name='study_group_detail'),
    path('join-group/', views.join_group_view, name='join_group'),  # 勉強グループに参加する
    path('study-goals/', views.study_goals_view, name='study_goals'),  # 学習目標
    path('study-history/', views.study_history_view, name='study_history'),  # 学習履歴
]
