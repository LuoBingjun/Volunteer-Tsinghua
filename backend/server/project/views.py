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
import json


class jobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        exclude = ['project']

# 用于发起项目
class detailSerializer(serializers.ModelSerializer):
    jobs = serializers.CharField()
    class Meta:
        model = Project
        exclude = ['webuser']
        # fields = ['title','content','requirements','form','deadline','jobs']

# 用于返回项目详情
class detail_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'webuser', 'content', 'cover', 'requirements',
            'form', 'time', 'deadline', 'finished', 'job_set']
        # fields = ['__all__', 'job_set'] #failed
        depth = 1

class detailView(GenericAPIView):
    serializer_class = detail_Serializer

    @login_required(web=True)
    def post(self, request):
        # 图片问题
        # _data=request.POST.copy()
        
        # print(_data["jobs"])

        # job_dict = eval(_data["jobs"])
        # print(job_dict)

        # #_data["jobs"] = json.loads(job_dict)
        # _data["jobs"]=job_dict
        # print(_data["jobs"])

        # print(dict(_data["jobs"]))

        serializer = detailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        _title = serializer.validated_data['title']
        _content = serializer.validated_data['content']
        _requirements=serializer.validated_data['requirements']
        _form=serializer.validated_data['form']
        _deadline=serializer.validated_data['deadline']
        _jobs=serializer.validated_data['jobs']

        job_data = json.loads(_jobs)
        job_serializer = jobSerializer(data=job_data, many=True)
        job_serializer.is_valid(raise_exception=True)

        # print(job_serializer.validated_data)


        _project=Project(title=_title, content=_content, requirements=_requirements, 
                form=_form, deadline=_deadline, webuser=request.user)
        
        _project.save()

        for a_job in job_serializer.validated_data:
            new_job=Job(project=_project,
                job_name=a_job["job_name"],
                job_worktime=a_job["job_worktime"], 
                job_content=a_job["job_content"],
                job_require_num=a_job["job_require_num"])
            new_job.save()

        return Response({'id': _project.id})
    
    @login_required(wx=True, web=True)
    def get(self, request):
        id = self.request.query_params.get('id')
        project = get_object_or_404(Project, id=id)
        
        serializer = self.get_serializer(project)
        res = dict(serializer.data)

        # 项目的状态有待改正
        # if project.finished:
        #     res['status'] = 'F'
        # else:
        #     apply_records = ApplyRecord.objects.filter(user=request.user, project=project)
        #     if apply_records.exists():
        #         apply_record = apply_records[0]
        #         res['status'] = apply_record.status
        #     else:
        #         if project.deadline >= datetime.now(timezone.utc):
        #             res['status'] = 'A'
        #         else:
        #             res['status'] = 'N'
        return Response(res)


class listSerializer(serializers.ModelSerializer):
    require_num = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = ['id', 'title', 'webuser', 'content', 'cover', 'requirements',
            'form', 'time', 'deadline', 'finished', 'require_num']
        depth = 0

    def get_require_num(self,obj):
        jobs = obj.job_set.all()
        require_num = 0
        for i in jobs:
            require_num = require_num + i.job_require_num
        
        return require_num


class listView(ListAPIView):
    serializer_class = listSerializer

    @login_required(wx=True, web=True)
    def get_queryset(self):
        return Project.objects.all()


# class searchSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Project
#         fields='__all__'

class searchView(ListAPIView):
    serializer_class = listSerializer

    @login_required(wx=True,web=True)
    def get_queryset(self):
        search = self.request.GET.get("search")

        key_iter=jieba.cut_for_search(search) #分词
        queryset = Project.objects.all()
        
        keywords=[]
        for i in key_iter:
            keywords.append(i)

        resultset=queryset.filter(title__icontains=search)

        for i in keywords:
            a_set=queryset.filter(title__icontains=i)
            resultset=chain(resultset, a_set)

        for i in keywords:
            a_set=queryset.filter(content__icontains=i)
            resultset=chain(resultset, a_set)
    
        resultlist=[]
        for i in resultset:
            if i not in resultlist:
                resultlist.append(i)
        return resultlist