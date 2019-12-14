from server.my import views
from django.urls import path

urlpatterns = [
    path(r'historyrecord', views.historyView.as_view()), 
    path(r'processrecord', views.processView.as_view()),
    path(r'processrecorddetail', views.processdetailView.as_view()),
    path(r'applyrecord', views.applyView.as_view()), 
    path(r'allrecord', views.allView.as_view()), 
    path(r'signrecord', views.signrecordView.as_view()), 
    path(r'messages', views.messagesView.as_view()),
    path(r'allproject',views.allprojectView.as_view()),
    path(r'comment',views.commentView.as_view()),
]