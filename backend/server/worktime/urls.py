from server.worktime import views
from django.urls import path

urlpatterns = [
    path(r'ViewWorktime', views.ViewWorktime.as_view()),
]