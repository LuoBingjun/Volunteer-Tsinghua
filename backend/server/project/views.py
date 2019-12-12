from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from datetime import datetime, timezone


from server.models import *
from server.utils import login_required
from itertools import chain
from django.db.models import Q
import jieba

class detailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = ['webuser']
        # fields = ['title','content','requirements','form','deadline','jobs']

# 用于返回项目详情
class detail_Serializer(serializers.ModelSerializer):
    webuser = serializers.ReadOnlyField(source='webuser.name')
    class Meta:
        model = Project
        fields = ['id', 'title', 'webuser', 'content', 'introduction', 'cover', 'requirements',
            'form', 'time', 'deadline', 'finished', 'job_set', 'begin_datetime', 'end_datetime']
        # fields = ['__all__', 'job_set'] #failed
        depth = 1

class detailView(GenericAPIView):
    serializer_class = detailSerializer

    @login_required(web=True)
    def post(self, request):
        serializer = detailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.save()
        return Response({'id': project.id})
    
    @login_required(wx=True)
    def get(self, request):
        id = self.request.query_params.get('id')
        project = get_object_or_404(Project, id=id)
        serializer = self.get_serializer(project)
        res = dict(serializer.data)

        if request.session.get('wx_user'):
            apply_records = ApplyRecord.objects.filter(user=request.user, project=project)
            applied_job = [record.job.id for record in apply_records]
            for item in res['job_set']:
                if item['id'] in applied_job:
                    item['job_status'] = apply_records.get(job=item['id']).status
                else:
                    item['job_status'] = 'A'

        return Response(res)


class listSerializer(serializers.ModelSerializer):
    require_num = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = ['id', 'title', 'webuser', 'content', 'introduction', 'cover', 'requirements',
            'form', 'time', 'deadline', 'finished', 'require_num', 'begin_datetime', 'end_datetime']
        depth = 0

    def get_require_num(self,obj):
        jobs = obj.job_set.all()
        require_num = 0
        for i in jobs:
            require_num = require_num + i.job_require_num
        
        return require_num

# 查看项目列表
class listView(ListAPIView):
    serializer_class = detailSerializer

    @login_required(wx=True, web=True)
    def get_queryset(self):
        return Project.objects.all()


class searchSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields='__all__'

class searchView(ListAPIView):
    serializer_class = searchSerializer

    @login_required(wx=True,web=True)
    def get_queryset(self):
        search = self.request.GET.get("search")

        key_iter=jieba.cut_for_search(search) #分词
        queryset = Project.objects.all()
        
        keywords=[]
        for i in key_iter:
            keywords.append(i)
        print(keywords)

        resultset=queryset.filter(title__icontains=search)

        for i in keywords:
            a_set=queryset.filter(title__icontains=i)
            resultset=chain(resultset, a_set)
            print(resultset)

        for i in keywords:
            a_set=queryset.filter(content__icontains=i)
            resultset=chain(resultset, a_set)
            print(resultset)
    
        resultlist=[]
        for i in resultset:
            if i not in resultlist:
                resultlist.append(i)
        return resultlist