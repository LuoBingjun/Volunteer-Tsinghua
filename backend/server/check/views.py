
from django.db import models
from django.http import JsonResponse

from rest_framework import generics
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from server.models import User, ApplyRecord, Project

from django.shortcuts import get_object_or_404

class ViewApplyInfoSerializer(serializers.ModelSerializer): 
    #submit_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S") 
    
    class Meta: 
        model = ApplyRecord
        fields = "__all__"  #全部显示
        depth = 2 


class ViewApplyInfo(generics.ListAPIView): 
    serializer_class = ViewApplyInfoSerializer 

    def get_queryset(self):
        _project_id = self.request.GET.get("project_id")
        #项目存在是否判断
        queryset = Project.objects.all()
        _project = get_object_or_404(queryset, pk=_project_id)
        return _project.applyrecord_set.all()


class CheckSerializer(serializers.Serializer):  
    apply_id = serializers.IntegerField(max_value=None, min_value=0) 
    checked = serializers.BooleanField()

class CheckOp(APIView):

    def post(self, request):
        info = CheckSerializer(data=request.data) # 验证数据
        if info.is_valid():
            _apply_id = info.validated_data['apply_id']
            # 项目存在是否判断
            if ApplyRecord.objects.filter(id=_apply_id).exists():
                _apply = ApplyRecord.objects.filter(id=_apply_id)[0]
                _apply.checked = info.validated_data['checked']
                _apply.save()
                return Response(status=200)
            else:    
                return Response('applyinfo not be found', status=404)    
        else:
            return Response(info.errors, status=400) #数据格式错误