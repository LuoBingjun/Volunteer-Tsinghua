from django.db import models
from django.http import JsonResponse

from rest_framework import generics
from rest_framework import serializers
from rest_framework.views import APIView

from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from server.models import *
from server.utils import login_required

class historySerializer(serializers.ModelSerializer):     
    class Meta: 
        model = JoinRecord
        # fields = ['project', 'job', 'work_time', 'signrecord_set']
        exclude = ["user"]
        depth = 1

class historyView(generics.ListAPIView):
    serializer_class = historySerializer
    
    @login_required(wx=True)
    def get_queryset(self):
        return JoinRecord.objects.filter(user=self.request.user, project__finished=True)

class processSerializer(serializers.ModelSerializer):     
    class Meta: 
        model = JoinRecord
        exclude = ['user']
        depth = 1

class processView(generics.ListAPIView):
    serializer_class = processSerializer
    
    @login_required(wx=True)
    def get_queryset(self):
        return JoinRecord.objects.filter(user=self.request.user, project__finished=False)

class applySerializer(serializers.ModelSerializer):     
    class Meta: 
        model = ApplyRecord
        exclude = ['user']
        depth = 1

class applyView(generics.ListAPIView):
    serializer_class = applySerializer
    
    @login_required(wx=True)
    def get_queryset(self):
        return ApplyRecord.objects.filter(user=self.request.user, project__finished=False).exclude(status='P')

class allSerializer(serializers.ModelSerializer):     
    class Meta: 
        model = ApplyRecord
        exclude = ['user']
        depth = 1

class allView(generics.ListAPIView):
    serializer_class = allSerializer
    
    @login_required(wx=True)
    def get_queryset(self):
        return ApplyRecord.objects.filter(user=self.request.user)

class signrecordSerializer(serializers.ModelSerializer):     
    class Meta: 
        model = SignRecord
        fields = '__all__'

class signrecordView(generics.RetrieveAPIView):    
    serializer_class = signrecordSerializer
    @login_required(wx=True)
    def get_object(self):
        id = self.request.query_params.get('signproject')
        sign_project = get_object_or_404(SignProject, pk=id)
        return get_object_or_404(sign_project.signrecord_set, join_record__user=self.request.user)
        

class allprojectSerializer(serializers.ModelSerializer):
    require_num = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = ['id', 'title', 'content', 'cover', 'requirements',
            'form', 'time', 'deadline', 'finished', 'require_num','job_set']
        
        depth = 1

    def get_require_num(self,obj):
        jobs = obj.job_set.all()
        require_num = 0
        for i in jobs:
            require_num = require_num + i.job_require_num
        return require_num

class allprojectView(generics.ListAPIView):
    serializer_class = allprojectSerializer
    @login_required(web=True)
    def get_queryset(self):
        return Project.objects.filter(webuser=self.request.user)

    