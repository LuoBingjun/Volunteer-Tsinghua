from server.sign import views
from django.urls import path

urlpatterns = [
    path(r'project', views.projectView.as_view()),
    path(r'list', views.listView.as_view()),
    path(r'signin', views.signinView.as_view()),
    path(r'signout',views.signoutView.as_view()),
]