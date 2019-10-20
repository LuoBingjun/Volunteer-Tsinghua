from server.auth import views
from django.urls import path

urlpatterns = [
    path(r'login', reserve.loginView.as_view()),
]