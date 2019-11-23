
from django.db import models
from django.http import JsonResponse

from rest_framework import generics
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from server.models import *

from django.shortcuts import get_object_or_404

from server.utils import login_required

# 管理员查看报名信息
class ViewApplyInfoSerializer(serializers.ModelSerializer): 
    #submit_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S") 
    
    class Meta: 
        model = ApplyRecord
        fields = "__all__"
        depth = 1


class ViewApplyInfo(generics.ListAPIView): 
    serializer_class = ViewApplyInfoSerializer 

    @login_required(web=True)
    def get_queryset(self):
        _project_id = self.request.GET.get("project_id")
        #项目存在是否判断
        queryset = Project.objects.all()
        _project = get_object_or_404(queryset, pk=_project_id)
        return _project.applyrecord_set.all()


# 管理员做审核操作
class CheckSerializer(serializers.Serializer):
    apply_id = serializers.IntegerField(max_value=None, min_value=0)
    checked = serializers.BooleanField(default=True)

class CheckOp(APIView):
    @login_required(web=True)
    def post(self, request):
        info = CheckSerializer(data=request.data) #验证数据
        if info.is_valid():
            _apply_id = info.validated_data['apply_id']
            # 项目存在是否判断
            _a_record_for_id = ApplyRecord.objects.filter(id=_apply_id)
            if _a_record_for_id.exists():
                _apply = _a_record_for_id[0]
            else:    
                return Response({'error':'applyinfo not be found'}, status=404)

            if(info.validated_data['checked']): # 审核通过
                _apply.status = 'P'
                # 审核通过添加到joinRecord
                _join = JoinRecord.objects.filter(user=_apply.user, project=_apply.project)

                # 重复处理
                if not _join.exists():
                    join_record = JoinRecord(user=_apply.user, project=_apply.project, work_time=0)
                    join_record.save()
                    join_record.job.add(_apply.job)
                    join_record.save()
                else:
                    a_job = _join[0].job.filter(id=_apply.job.id)
                    if a_job.exists():
                        return Response({"error":"check already pass"},status=409)
                    else:

                        _join[0].job.add(_apply.job)
                        _join[0].save() 
            else:
                _apply.status = 'N'

                _join = JoinRecord.objects.filter(user=_apply.user, project=_apply.project)

                if _join.exists():
                    a_job=_join[0].job.filter(id=_apply.job.id)
                    if a_job.exists():
                        _join[0].job.remove(_apply.job)
                        if not _join[0].job:
                            _join[0].delete()
            _apply.save() # 存储审核状态
            
            return Response(status=200)
        else:
            return Response(info.errors, status=400) #数据格式错误

# 普通用户查看自己某个项目的审核结果
# 问题：客户端必须发送请求，才会发送给客户端信息吗？
# 还是更新check的状态后可以直接发送给客户端
# 问题 get的时候需不需要验证客户端传来的信息的正确性
# class ViewResultSerializer(serializers.Serializer): 
#     apply_id = serializers.IntegerField(max_value=None, min_value=0)
    
# class ViewResult(APIView):
#     @login_required(wx=True)
#     def get(self, request):
#         info = ViewResultSerializer(data=self.request.query_params)
#         if info.is_valid():
#             _apply_id = info.validated_data["apply_id"]
#             #项目存在是否判断
#             _set = ApplyRecord.objects.filter(id=_apply_id)
#             if _set.exists():
#                 return Response({"审核状态":_set[0].status}, status=200)
#             else:
#                 return Response({'error':'applyinfo not be found'}, status=404)
#         else:
#             return Response(info.errors, status=400) #数据格式错误