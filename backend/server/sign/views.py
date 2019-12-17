from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.exceptions import PermissionDenied

import datetime
import json

from backend import settings
from server.models import *
from server.utils import login_required, send_wx_msg

from math import radians, cos, sin, asin, sqrt


class createSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignProject
        fields = '__all__'

# 发起签到
class projectView(CreateAPIView):
    @login_required(web=True)
    def post(self, request):
        serializer = createSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.validated_data['project']
        if not (request.user.is_superuser or request.user == project.webuser):
            raise PermissionDenied()
        sign_project = serializer.save()
        sign_project.longitude -= 0.006256
        sign_project.latitude -= 0.001276
        sign_project.save()
        jobs = sign_project.jobs.all()

        receivers = set()
        for job in jobs:
            users = set([i.user for i in job.joinrecord_set.all()])
            receivers = receivers | users

        for user in receivers:
            send_wx_msg.delay(user.openid, settings.SIGN_TEMPLATE_ID, '/pages/currentproject/currentproject?projectID={}'.format(project.id),
                    {
                        'thing1': {"value": sign_project.title},
                        "date2": {"value": datetime.datetime.strftime(sign_project.begin_time, "%Y-%m-%d")},
                        "thing4": {"value": '签到地点'},
                        "time3": {'value': datetime.datetime.strftime(sign_project.begin_time, "%H:%M")},
                    })
            Message.objects.create(type='M', sender=request.user, receiver=user, project=sign_project.project,
                                       title='签到活动通知', content=json.dumps([
                                           {'key':'活动名称', 'value': sign_project.title},
                                           {'key':'签到地点', 'value': sign_project.position},
                                           {'key':'开始时间', 'value': datetime.datetime.strftime(sign_project.begin_time, "%Y-%m-%d %H:%M")},
                                           {'key':'截止时间', 'value': datetime.datetime.strftime(sign_project.end_time, "%Y-%m-%d %H:%M")}
                                       ], ensure_ascii=False))
        return Response({'id': sign_project.id})

class listSerializer(serializers.ModelSerializer):
    # cover = serializers.ImageField(use_url=True)
    class Meta:
        model = SignProject
        exclude = ["project"]
        depth = 1

# 查看签到列表
class listView(ListAPIView):
    serializer_class = listSerializer
    @login_required(wx=True)
    def get_queryset(self):
        project = self.request.query_params.get('project')
        
        join_record = get_object_or_404(JoinRecord, user=self.request.user, project=project)
        join_record_jobs_set = join_record.job.all()
        result = []

        sign_project_set = SignProject.objects.filter(project=project)
        for i in sign_project_set:
            sign_project_jobs_set = i.jobs.all()
            if (sign_project_jobs_set & join_record_jobs_set):
                result.append(i)

        return result

class signinSerializer(serializers.Serializer):
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
    sign_project_id = serializers.IntegerField(max_value=None, min_value=0)

# 签到
class signinView(APIView):
    @login_required(wx=True)
    def post(self, request):
        serializer = signinSerializer(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        sign_project_id = serializer.validated_data['sign_project_id'] 
        longitude = serializer.validated_data['longitude']
        latitude = serializer.validated_data['latitude']
        
        sign_project = get_object_or_404(SignProject, id=sign_project_id)
        # 判断时间
        now = timezone.now()
        if sign_project.begin_time >= now:
            return Response({"error":"签到未开始"},status=406)
        elif sign_project.end_time <= now:
            return Response({"error":"签到已结束"},status=406)

        join_record = get_object_or_404(JoinRecord, user=request.user, project=sign_project.project)
        
        if SignRecord.objects.filter(join_record=join_record, sign_project=sign_project).exists():
            return Response({"error":"info already exists"},status=409)
        
        # 判断job有没有交集
        join_record_jobs_set = join_record.job.all()
        sign_project_jobs_set = sign_project.jobs.all()
        if not (sign_project_jobs_set & join_record_jobs_set):
            return Response({"error":"不可签到"},status=406)
        
        print(sign_project.longitude,sign_project.latitude,longitude,latitude)
        
        # 判断地理位置
        long1, la1, long2, la2 = map(radians, [float(sign_project.longitude), float(sign_project.latitude), float(longitude), float(latitude)]) # 经纬度转换成弧度
        
        dlon=long2-long1
        dlat=la2-la1
        a=sin(dlat/2)**2 + cos(la1) * cos(la2) * sin(dlon/2)**2 
        distance=2*asin(sqrt(a))*6371393 # 地球平均半径，6371km
        distance=round(distance,3)
        print(distance)
        if distance > 100:
            return Response({"error":"请前往指定地点签到"},status=406)

        _file = open("record.txt", 'a', encoding='utf-8')
        print('签到人:'+str(request.user.name)+'\n\r', file=_file)
        print('(sign_project.longitude,sign_project.latitude):('
            +str(sign_project.longitude)+','+str(sign_project.latitude)+')\n\r',file=_file)
        print('(longitude,latitude):('
            +str(longitude)+','+str(latitude)+')'+'\n\r',file=_file)
        print('distance:'+str(distance)+'\n\r',file=_file)
        print('\n\r',file=_file)
        _file.close()
        

        sign_record = SignRecord.objects.create(sign_project=sign_project,join_record=join_record)

        return Response({'sign_record_id': sign_record.id})

class signoutSerializer(serializers.Serializer):
    sign_record_id = serializers.IntegerField(max_value=None, min_value=0)

# 签退
class signoutView(APIView):
    @login_required(wx=True)
    def post(self,request):
        info = signoutSerializer(data=request.data)
        info.is_valid(raise_exception=True)

        _sign_record_id = info.validated_data['sign_record_id']
        queryset = SignRecord.objects.all()
        sign_record = get_object_or_404(queryset, id=_sign_record_id)

        if not sign_record.sign_out_time:
            sign_record.sign_out_time = timezone.now()
            sign_record.save()
        else:
            return Response({'error':'already signout'},status=409) 
        return Response(status=200)
