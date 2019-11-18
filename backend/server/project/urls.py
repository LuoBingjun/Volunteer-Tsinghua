from server.project import views
from django.urls import path

urlpatterns = [
    path(r'detail', views.detailView.as_view()),
    path(r'list', views.listView.as_view()),
    path(r'search',views.searchView.as_view()),
]