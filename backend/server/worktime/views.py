from django.db import models
from django.http import JsonResponse

from rest_framework import generics
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from server.models import User, ApplyRecord, Project, JoinRecord
from server.utils import login_required

import xlrd

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


class importSerializer(serializers.Serializer): 
    project_id = serializers.IntegerField(max_value=None, min_value=1)
    import_file = serializers.FileField(required=True)
    
class importView(APIView): 
    def post(self, request):
        serializer = importSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project_id = serializer.validated_data['project_id']
        f = serializer.validated_data['import_file']
        project = get_object_or_404(Project, pk=project_id)
        records = project.joinrecord_set.all()
        work_time = {}
        try:
            wb = xlrd.open_workbook(filename=None, file_contents=f.read())
            table = wb.sheets()[0]
            nrows = table.nrows
            for i in range(1, nrows):
                id = int(table.cell(i, 0).value)
                value = float(table.cell(i,-1).value)
                work_time[id] = value
        except:
            return Response(status=400)
        for record in records:
            id = record.user.id
            record.work_time = work_time[id]
            record.save()
        return Response(status=200)