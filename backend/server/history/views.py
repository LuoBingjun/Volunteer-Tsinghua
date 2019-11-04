from django.db import models
from django.http import JsonResponse

from rest_framework import generics
from rest_framework import serializers
from rest_framework.views import APIView

from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from server.models import User, ApplyRecord, Project, JoinRecord
from server.utils import login_required

class HistoryRecordSerializer(serializers.ModelSerializer): 
    #submit_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S") 
    
    class Meta: 
        model = JoinRecord
        fields = "__all__"  #全部显示
        depth = 2 

# 用户查看参加活动的历史记录
class HistoryRecord(generics.ListAPIView):
    serializer_class = HistoryRecordSerializer
    
    @login_required
    def get_queryset(self):

        history_set = JoinRecord.objects.filter(user=self.request.user, project__finished=True)
        return history_set.all()