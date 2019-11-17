from django.db import models

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from server.models import *
from server.utils import login_required

from django.shortcuts import get_object_or_404
import datetime

class applySerializer(serializers.Serializer):
    form = serializers.CharField(max_length=None, min_length=None, allow_blank=False, trim_whitespace=True)
    project_id = serializers.IntegerField(max_value=None, min_value=0)
    

# 用户报名接口 需要注意：不能重复报名 返回报名编号便于前端查询报名信息
class fillformView(APIView):
    @login_required(wx=True)
    def post(self, request):
        info = applySerializer(data=request.data) # 验证数据
        if info.is_valid():
            _form = info.validated_data['form']
            project_id = info.validated_data['project_id']

            # 项目存在是否判断
            _a_record_for_project = Project.objects.filter(id=project_id, deadline__gt=datetime.datetime.now(), finished=False)
            if _a_record_for_project.exists():
                _project = _a_record_for_project[0]
            else:    
                return Response({'error':'project not be found'}, status=404)

            # 验证重复报名 需要使用user和prject来在applyRecord中检索
            if ApplyRecord.objects.filter(user=request.user, project__id=project_id).exists():
                return Response({'error':'applyinfo already exists'}, status=400)

            # 项目存在且从未报名,则有下列操作

            # 建立新数据
            apply_record = ApplyRecord(user=request.user, project=_project,
                        form=_form)
            apply_record.save()
            return Response({'apply_id':apply_record.id},status=200)
        else:
            return Response(info.errors, status=400) #数据格式错误


class cancelapplySerializer(serializers.Serializer):
    apply_id = serializers.IntegerField(max_value=None, min_value=1)
    

class cancelapplyView(APIView):
    @login_required(wx=True)
    def post(self, request):
        info = cancelapplySerializer(data=request.data) # 验证数据
        if info.is_valid():
            apply_id = info.validated_data['apply_id']  
            queryset = ApplyRecord.objects.all()
            apply_record = get_object_or_404(queryset, id=apply_id)
            apply_record.delete()
            return Response(status=200)     
        else:
            return Response(info.errors, status=400) #数据格式错误