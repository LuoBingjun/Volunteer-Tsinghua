from server.history import views
from django.urls import path

urlpatterns = [
    path(r'HistoryRecord', views.HistoryRecord.as_view()), 
]