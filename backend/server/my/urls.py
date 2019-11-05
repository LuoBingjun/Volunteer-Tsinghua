from server.my import views
from django.urls import path

urlpatterns = [
    path(r'historyrecord', views.historyView.as_view()), 
    path(r'processrecord', views.processView.as_view()), 
    path(r'applyrecord', views.applyView.as_view()), 
]