from django.db import models

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from server.models import User, ApplyRecord, Project
from server.utils import login_required

class applySerializer(serializers.Serializer):  
    form = serializers.CharField(max_length=None, min_length=None, allow_blank=False, trim_whitespace=True)
    project_id = serializers.IntegerField(max_value=None, min_value=0)
    


class fillformView(APIView):
    @login_required
    def post(self, request):
        info = applySerializer(data=request.data) # 验证数据
        if info.is_valid():
            _form = info.validated_data['form']
            project_id = info.validated_data['project_id']

            # 项目存在是否判断
            if Project.objects.filter(id=project_id).exists():
                _project = Project.objects.filter(id=project_id)[0]
            else:    
                return Response('project not be found', status=404)

            #if(!request.user.applyrecord_set)
            _checked = False


            apply_record = ApplyRecord(project=_project,  #request.session['user']#
                        form=_form, checked=_checked)
            apply_record.user_id = 3
            apply_record.save()
            return Response(status=200)
        else:
            return Response(info.errors, status=400) #数据格式错误


