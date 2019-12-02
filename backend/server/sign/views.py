from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.utils import timezone

import datetime
import json

from backend import settings
from server.models import *
from server.utils import login_required, send_wx_msg

class createSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignProject
        fields = '__all__'

class projectView(CreateAPIView):
    @login_required(web=True, wx=False)
    def post(self, request):
        serializer = createSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sign_project = serializer.save()
        
        jobs = sign_project.jobs.all()

        receivers = set()
        for job in jobs:
            users = set([i.user for i in job.joinrecord_set.all()])
            receivers = receivers | users

        for user in receivers:
            send_wx_msg.delay(user.openid, settings.SIGN_TEMPLATE_ID, '',
                    {
                        'thing1': {"value": sign_project.title},
                        "date2": {"value": datetime.datetime.strftime(sign_project.begin_time, "%Y-%m-%d")},
                        "thing4": {"value": '签到地点'},
                        "time3": {'value': datetime.datetime.strftime(sign_project.begin_time, "%H:%M")},
                    })
            Message.objects.create(type='M', sender=request.user, receiver=user, project=sign_project.project,
                                       title='签到活动通知', content=json.dumps([
                                           {'key':'活动名称', 'value': sign_project.title},
                                           {'key':'签到开始时间', 'value': datetime.datetime.strftime(sign_project.begin_time, "%Y-%m-%d %H:%M")},
                                           {'key':'签到截止时间', 'value': datetime.datetime.strftime(sign_project.end_time, "%Y-%m-%d %H:%M")}
                                       ], ensure_ascii=False))
        return Response({'id': sign_project.id})

class listSerializer(serializers.ModelSerializer):
    # cover = serializers.ImageField(use_url=True)
    class Meta:
        model = SignProject
        exclude = ["project"]
        depth = 1

class listView(ListAPIView):
    serializer_class = listSerializer
    @login_required(wx=True)
    def get_queryset(self):
        project = self.request.query_params.get('project')
        return SignProject.objects.filter(project=project)

class signinSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignRecord
        fields = ['sign_project']

class signinView(APIView):
    @login_required(wx=True)
    def post(self, request):
        serializer = signinSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        project = serializer.validated_data['sign_project'].project
        join_record = get_object_or_404(JoinRecord, user=request.user, project=project)
        
        if SignRecord.objects.filter(join_record=join_record, sign_project=serializer.validated_data['sign_project']).exists():
            return Response(status=409)
        serializer.validated_data['join_record'] = join_record
        sign_record = serializer.save()
        return Response({'sign_record_id': sign_record.id})

class signoutSerializer(serializers.Serializer):
    sign_record_id = serializers.IntegerField(max_value=None, min_value=0)

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
