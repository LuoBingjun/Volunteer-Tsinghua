from django.db import models
from django.http import JsonResponse

from rest_framework import generics
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from server.models import User, ApplyRecord, Project, JoinRecord
from server.utils import login_required

class ViewWorktimeSerializer(serializers.Serializer): 
    project_id = serializers.IntegerField(max_value=None, min_value=0)
    
class ViewWorktime(APIView): 
   
    @login_required
    def get(self, request):
        info = ViewWorktimeSerializer(data=self.request.query_params)
        if info.is_valid():
            _project_id=info.validated_data['project_id']
        #项目存在是否判断
            queryset = JoinRecord.objects.all()
            join_record=get_object_or_404(queryset, user=request.user, project__id=_project_id)
            
            return Response({'worktime':join_record.work_time}, status=200)
            
        else:
            return Response(info.errors, status=400) #数据格式错误
