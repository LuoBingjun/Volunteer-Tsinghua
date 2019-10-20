from server.auth import views
from django.urls import path

urlpatterns = [
    path(r'bind', reserve.bindView.as_view()),
]