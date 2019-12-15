from server.worktime import views
from django.urls import path

urlpatterns = [
    path(r'ViewWorktime', views.ViewWorktime.as_view()),
    path(r'Export',views.ExportView.as_view()),
    path(r'import', views.importView.as_view()),
]

