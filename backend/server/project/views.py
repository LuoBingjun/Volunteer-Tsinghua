from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

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
class wx_detail_Serializer(serializers.ModelSerializer):
    webuser = serializers.ReadOnlyField(source='webuser.name')

    class Meta:
        model = Project
        fields = '__all__'
        extra_fields = ['job_set']
        depth = 1

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(wx_detail_Serializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields

class web_detail_Serializer(serializers.ModelSerializer):
    webuser = serializers.ReadOnlyField(source='webuser.name')

    class Meta:
        model = Project
        fields = '__all__'
        extra_fields = ['job_set', 'signproject_set']
        depth = 1

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(web_detail_Serializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields

        

class detailView(GenericAPIView):
    serializer_class = wx_detail_Serializer

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
        # serializer.save()

        # _title = serializer.validated_data['title']
        # _content = serializer.validated_data['content']
        # _cover = serializer.validated_data['cover']
        # _requirements=serializer.validated_data['requirements']
        # _form=serializer.validated_data['form']
        # _deadline=serializer.validated_data['deadline']
        # _begin_datetime=serializer.validated_data['begin_datetime']
        # _end_datetime=serializer.validated_data['end_datetime']
        _jobs=serializer.validated_data['jobs']
        del serializer.validated_data['jobs']
        # _introduction=serializer.validated_data['introduction']
        

        job_data = json.loads(_jobs)
        job_serializer = jobSerializer(data=job_data, many=True)
        job_serializer.is_valid(raise_exception=True)

        # print(job_serializer.validated_data)
        serializer.validated_data['webuser'] = request.user


        _project=Project(**serializer.validated_data)
        _project.save()

        for a_job in job_serializer.validated_data:
            new_job=Job(project=_project,
                job_name=a_job["job_name"],
                job_worktime=a_job["job_worktime"], 
                job_content=a_job["job_content"],
                job_require_num=a_job["job_require_num"])
            new_job.save()

        return Response({'id': _project.id})
    
    # 项目详情
    @login_required(wx=True, web=True)
    def get(self, request):
        id = self.request.query_params.get('id')
        project = get_object_or_404(Project, id=id)

        if request.session.get('wx_user'):
            serializer = self.get_serializer(data=project)
            res = dict(serializer.data)

            apply_records = ApplyRecord.objects.filter(user=request.user, project=project)
            applied_job = [record.job.id for record in apply_records]
            for item in res['job_set']:
                if item['id'] in applied_job:
                    item['job_status'] = apply_records.get(job=item['id']).status
                else:
                    item['job_status'] = 'A'
            return Response(res)
        else:
            serializer = web_detail_Serializer(project)
            return Response(serializer.data)


class listPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size = 10

class listSerializer(serializers.ModelSerializer):
    require_num = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = '__all__'
        extra_fields = ['require_num']
        depth = 0

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(listSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields

    def get_require_num(self,obj):
        jobs = obj.job_set.all()
        require_num = 0
        for i in jobs:
            require_num = require_num + i.job_require_num
        
        return require_num

# 查看项目列表
class listView(ListAPIView):
    serializer_class = listSerializer
    pagination_class = listPagination

    @login_required(wx=True, web=True)
    def get_queryset(self):
        queryset = Project.objects.filter(finished=False)
        search = self.request.GET.get("search")
        _type = self.request.GET.get('type')

        if _type:
            queryset = queryset.filter(type=_type)

        if search:
            key_iter=jieba.cut_for_search(search) #分词
            keywords=list(key_iter)

            resultset = queryset.filter(title__icontains=search)

            for i in keywords:
                resultset |= queryset.filter(title__icontains=i)

            for i in keywords:
                resultset |= queryset.filter(content__icontains=i)
        else:
            resultset = queryset
        return resultset


# class searchSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Project
#         fields='__all__'

# class searchView(ListAPIView):
#     serializer_class = listSerializer

#     @login_required(wx=True,web=True)
#     def get_queryset(self):
        

class cancelprojectSerializer(serializers.Serializer):
    project_id = serializers.IntegerField(max_value=None, min_value=1)

class cancelView(APIView):
    @login_required(web=True)
    def post(self, request):
        info = cancelprojectSerializer(data=request.data) # 验证数据
        info.is_valid(raise_exception=True)
        project_id = info.validated_data['project_id']  
        queryset = Project.objects.all()
        if request.user.is_superuser:
            _project = get_object_or_404(queryset, id=project_id)
            _project.delete()
        else:
            _project = get_object_or_404(queryset, id=project_id, webuser=request.user)
            _project.delete()
        return Response(status=200)