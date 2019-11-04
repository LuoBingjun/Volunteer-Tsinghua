from server.sign import views
from django.urls import path

urlpatterns = [
    path(r'manage', views.manageView.as_view()),
    path(r'signin', views.signinView.as_view()),
]