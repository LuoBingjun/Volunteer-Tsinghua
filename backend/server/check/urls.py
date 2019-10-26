from server.check import views
from django.urls import path

urlpatterns = [
    path(r'ViewApplyInfo', views.ViewApplyInfo.as_view()),
    path(r'CheckOp',views.CheckOp.as_view())
]