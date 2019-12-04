from django.db import models
from django.http import JsonResponse

from rest_framework import generics
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from server.models import *
from server.utils import login_required

class filterbydate(serializers.Serializer):
    begin_time = serializers.DateField()
    end_time = serializers.DateField()

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
        if self.request.query_params.get('begin_time') and self.request.query_params.get('end_time'):
            filterinfo = filterbydate(data=self.request.query_params)
            filterinfo.is_valid(raise_exception=True)
            _begin_time = filterinfo.validated_data['begin_time']
            _end_time = filterinfo.validated_data['end_time']

            _end_time = _end_time.replace(day=_end_time.day+1)
            return JoinRecord.objects.filter(user=self.request.user, project__finished=True, 
                    project__begin_datetime__gte=_begin_time, project__end_datetime__lte=_end_time)
        else:
            return JoinRecord.objects.filter(user=self.request.user, project__finished=True)
        
class processSerializer(serializers.ModelSerializer):     
    class Meta: 
        model = JoinRecord
        fields = ['project']
        depth = 1

class processView(generics.ListAPIView):
    serializer_class = processSerializer
    
    @login_required(wx=True)
    def get_queryset(self):
        if self.request.query_params.get('begin_time') and self.request.query_params.get('end_time'):
            filterinfo = filterbydate(data=self.request.query_params)
            filterinfo.is_valid(raise_exception=True)
            _begin_time = filterinfo.validated_data['begin_time']
            _end_time = filterinfo.validated_data['end_time']

            _end_time = _end_time.replace(day=_end_time.day+1)
            return JoinRecord.objects.filter(user=self.request.user, project__finished=False, 
                    project__begin_datetime__gte=_begin_time, project__end_datetime__lte=_end_time)
            
        else:
            return JoinRecord.objects.filter(user=self.request.user, project__finished=False)

# 已报名项目
class applySerializer(serializers.ModelSerializer):     
    class Meta: 
        model = Project
        fields = "__all__"
        depth = 0

class applyView(generics.ListAPIView):
    serializer_class = applySerializer
    
    @login_required(wx=True)
    def get_queryset(self):
        
        if self.request.query_params.get('begin_time') and self.request.query_params.get('end_time'):
            filterinfo = filterbydate(data=self.request.query_params)
            filterinfo.is_valid(raise_exception=True)
            _begin_time = filterinfo.validated_data['begin_time']
            _end_time = filterinfo.validated_data['end_time']

            _end_time = _end_time.replace(day=_end_time.day+1)
            project_set = ApplyRecord.objects.filter(user=self.request.user, project__finished=False, 
                                project__begin_datetime__gte=_begin_time, project__end_datetime__lte=_end_time).exclude(status='P')
        else:
            project_set = ApplyRecord.objects.filter(user=self.request.user, project__finished=False).exclude(status='P')

        # 上一步有可能出现重复的结果，筛除重复
        result_set=set()

        for i in project_set:
            result_set.add(i.project)
        return result_set

# 我的所有项目
class allSerializer(serializers.ModelSerializer):     
    class Meta: 
        model = Project
        fields = "__all__"
        depth = 0

class allView(generics.ListAPIView):
    serializer_class = allSerializer
    
    @login_required(wx=True)
    def get_queryset(self):
        if self.request.query_params.get('begin_time') and self.request.query_params.get('end_time'):
            filterinfo = filterbydate(data=self.request.query_params)
            filterinfo.is_valid(raise_exception=True)
            _begin_time = filterinfo.validated_data['begin_time']
            _end_time = filterinfo.validated_data['end_time']
            _end_time = _end_time.replace(day=_end_time.day+1)
            project_set = ApplyRecord.objects.filter(user=self.request.user, project__finished=False, 
                                project__begin_datetime__gte=_begin_time, project__end_datetime__lte=_end_time).exclude(status='P')
        else:
            project_set = ApplyRecord.objects.filter(user=self.request.user)

        # 上一步有可能出现重复的结果，筛除重复
        result_set=set()

        for i in project_set:
            result_set.add(i.project)
        return result_set

# 签到记录
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
        
        
# 管理员查询自己发起的项目
class allprojectSerializer(serializers.ModelSerializer):
    require_num = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = ['id', 'title', 'content', 'cover', 'requirements',
            'form', 'time', 'deadline', 'finished', 'require_num','job_set','begin_datetime','end_datetime']
        
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
        if self.request.query_params.get('begin_time') and self.request.query_params.get('end_time'):
            filterinfo = filterbydate(data=self.request.query_params)
            filterinfo.is_valid(raise_exception=True)
            _begin_time = filterinfo.validated_data['begin_time']
            _end_time = filterinfo.validated_data['end_time']
            _end_time = _end_time.replace(day=_end_time.day+1)
            return Project.objects.filter(webuser=self.request.user, begin_datetime__gte=_begin_time, end_datetime__lte=_end_time)
        else:
            return Project.objects.filter(webuser=self.request.user)


class processdetailinSerializer(serializers.Serializer):
    project_id = serializers.IntegerField(max_value=None, min_value=0)

class signprojectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignProject
        exclude = ['project']
        depth = 0

class processdetailSerializer(serializers.ModelSerializer):
    signproject=serializers.ListField(child=signprojectSerializer())
    class Meta: 
        model = JoinRecord
        fields = ['project','job','signrecord_set','signproject']
        depth = 1

class processdetailView(GenericAPIView):
    serializer_class = processdetailSerializer
    
    @login_required(wx=True)
    def get(self,request):
        serializer = processdetailinSerializer(data=request.query_params)
        
        serializer.is_valid(raise_exception=True)
        project_id = serializer.validated_data['project_id']

        join_record = get_object_or_404(JoinRecord, user=self.request.user, project__id=project_id, project__finished=False)
        
        
        signproject_set=SignProject.objects.none()
        for i in join_record.job.all():
            signproject_set=signproject_set|i.signproject_set.all()

        join_record.signproject = signproject_set.distinct()
        result = self.get_serializer(join_record)
        
        return Response(result.data)
