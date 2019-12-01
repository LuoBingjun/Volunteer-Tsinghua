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
        exclude = ['user']
        depth = 2 

class historyView(generics.ListAPIView):
    serializer_class = historySerializer
    
    @login_required(wx=True)
    def get_queryset(self):
        return JoinRecord.objects.filter(user=self.request.user, project__finished=True)

class processSerializer(serializers.ModelSerializer):     
    class Meta: 
        model = JoinRecord
        exclude = ['user']
        depth = 2

class processView(generics.ListAPIView):
    serializer_class = processSerializer
    
    @login_required(wx=True)
    def get_queryset(self):
        return JoinRecord.objects.filter(user=self.request.user, project__finished=False)

class applySerializer(serializers.ModelSerializer):     
    class Meta: 
        model = ApplyRecord
        exclude = ['user']
        depth = 2 

class applyView(generics.ListAPIView):
    serializer_class = applySerializer
    
    @login_required(wx=True)
    def get_queryset(self):
        return ApplyRecord.objects.filter(user=self.request.user, project__finished=False).exclude(status='P')

class allSerializer(serializers.ModelSerializer):     
    class Meta: 
        model = ApplyRecord
        exclude = ['user']
        depth = 2 

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

class messagesSerializer(serializers.ModelSerializer):     
    class Meta: 
        model = Message
        exclude = ['receiver']
        depth = 1

class messagesView(generics.ListAPIView):
    serializer_class = messagesSerializer
    @login_required(wx=True)
    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user)
        