from django.db import models

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from server.models import User, ApplyRecord, Project
from server.utils import login_required

import datetime

class applySerializer(serializers.Serializer):  
    form = serializers.CharField(max_length=None, min_length=None, allow_blank=False, trim_whitespace=True)
    project_id = serializers.IntegerField(max_value=None, min_value=0)
    

# 用户报名接口 需要注意：不能重复报名 返回报名编号便于前端查询报名信息
class fillformView(APIView):
    @login_required
    def post(self, request):
        info = applySerializer(data=request.data) # 验证数据
        if info.is_valid():
            _form = info.validated_data['form']
            project_id = info.validated_data['project_id']

            # 项目存在是否判断
            if Project.objects.filter(id=project_id, deadline__gt=datetime.datetime.now()).exists():
                _project = Project.objects.filter(id=project_id, deadline__gt=datetime.datetime.now())[0]
            else:    
                return Response('project not be found', status=404)

            # 验证重复报名 需要使用user和prject来在applyRecord中检索
            if ApplyRecord.objects.filter(user=request.user, project__id=project_id).exists():
                return Response('applyinfo already exists', status=401)

            # 项目存在且从未报名,则有下列操作

            _checked = False  # 初始设定为未审核通过

            # 建立新数据
            apply_record = ApplyRecord(user=request.user, project=_project,
                        form=_form, checked=_checked)
            apply_record.save()
            return Response(status=200)
        else:
            return Response(info.errors, status=400) #数据格式错误


