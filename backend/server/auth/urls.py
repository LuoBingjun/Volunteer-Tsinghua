from server.auth import views
from django.urls import path

urlpatterns = [
    path(r'prelogin', views.preloginView.as_view()),
    path(r'login', views.loginView.as_view()),
    path(r'weblogin', views.webloginView.as_view()),
    path(r'user', views.userView.as_view()),
]