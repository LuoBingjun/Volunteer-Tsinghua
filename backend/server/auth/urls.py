from server.auth import views
from django.urls import path

urlpatterns = [
    path(r'login', views.loginView.as_view()),
    path(r'userinfo', views.userView.as_view()),
]