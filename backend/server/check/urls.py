from server.check import views
from django.urls import path

urlpatterns = [
    path(r'ViewApplyInfo', views.ViewApplyInfo.as_view()), # 查看报名信息 #管理员#
    path(r'CheckOp',views.CheckOp.as_view()), #管理员 审核通过#
    path(r'ViewResult',views.ViewResult.as_view()), #普通用户 查看报名的项目的审核情况# 
]