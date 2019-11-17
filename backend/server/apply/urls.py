from server.apply import views
from django.urls import path

urlpatterns = [
    path(r'fillform', views.fillformView.as_view()),
    path(r'cancelapply',views.cancelapplyView.as_view()),
]