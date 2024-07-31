from django.contrib import admin
from django.urls import path, include
from main import views as main_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # 包含 accounts 应用的 URL 配置
    path('dashboard/', main_views.dashboard_view, name='dashboard'),  # 可选，根路径已经指向 dashboard
    path('', main_views.dashboard_view, name='dashboard'),  # 根路径指向 dashboard
    path('main/', include('main.urls')),  # 包含 main 应用的 URL 配置
]
