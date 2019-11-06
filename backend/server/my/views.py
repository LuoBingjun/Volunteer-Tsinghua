from django.db import models
from django.http import JsonResponse

from rest_framework import generics
from rest_framework import serializers
from rest_framework.views import APIView

from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from server.models import User, ApplyRecord, Project, JoinRecord
from server.utils import login_required

class historySerializer(serializers.ModelSerializer):     
    class Meta: 
        model = JoinRecord
        exclude = ['user']
        depth = 2 

# 用户查看参加活动的历史记录
class historyView(generics.ListAPIView):
    serializer_class = historySerializer
    
    @login_required
    def get_queryset(self):
        return JoinRecord.objects.filter(user=self.request.user, project__finished=True)

class processSerializer(serializers.ModelSerializer):     
    class Meta: 
        model = JoinRecord
        exclude = ['user']
        depth = 2

# 用户查看正在参加活动的记录
class processView(generics.ListAPIView):
    serializer_class = processSerializer
    
    @login_required
    def get_queryset(self):
        return JoinRecord.objects.filter(user=self.request.user, project__finished=False)

class applySerializer(serializers.ModelSerializer):     
    class Meta: 
        model = ApplyRecord
        exclude = ['user']
        depth = 2 

# 用户查看正在待审核的记录
class applyView(generics.ListAPIView):
    serializer_class = applySerializer
    
    @login_required
    def get_queryset(self):
        return ApplyRecord.objects.filter(user=self.request.user, project__finished=False).exclude(status='P')

class allSerializer(serializers.ModelSerializer):     
    class Meta: 
        model = ApplyRecord
        exclude = ['user']
        depth = 2 

# 用户查看正在待审核的记录
class allView(generics.ListAPIView):
    serializer_class = allSerializer
    
    @login_required
    def get_queryset(self):
        return ApplyRecord.objects.filter(user=self.request.user)