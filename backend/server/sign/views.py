from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from server.models import *
from server.utils import login_required

from django.utils import timezone

from math import radians, cos, sin, asin, sqrt


class createSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignProject
        fields = '__all__'

# 发起签到
class projectView(CreateAPIView):
    @login_required(web=True, wx=False)
    def post(self, request):
        serializer = createSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sign_project = serializer.save()
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
        return SignProject.objects.filter(project=project)

class signinSerializer(serializers.Serializer):
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
    sign_project_id = serializers.IntegerField(max_value=None, min_value=0)

# 签到
class signinView(APIView):
    @login_required(wx=True)
    def post(self, request):
        print(request.data)
        serializer = signinSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
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
            return Response(status=409)
        
        # 判断job有没有交集

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
