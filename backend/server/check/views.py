
from django.db import models
from django.http import JsonResponse

from rest_framework import generics
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from server.models import User, ApplyRecord, Project

from django.shortcuts import get_object_or_404

from server.utils import login_required

# 管理员查看报名信息
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


# 管理员做审核操作
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

# 普通用户查看自己某个项目的审核结果
# 问题：客户端必须发送请求，才会发送给客户端信息吗？
# 还是更新check的状态后可以直接发送给客户端
# 问题 get的时候需不需要验证客户端传来的信息的正确性
class ViewResultSerializer(serializers.Serializer): 
    apply_id = serializers.IntegerField(max_value=None, min_value=0)
    
class ViewResult(APIView): 
   
    @login_required
    def get(self, resquest):
        _apply_id = self.request.GET.get("apply_id")
        #项目存在是否判断
        if ApplyRecord.objects.filter(id=_apply_id).exists():
            return Response({"checked":ApplyRecord.objects.filter(id=_apply_id)[0].checked}, status=200)
        else:
            return Response('applyinfo not be found', status=404)