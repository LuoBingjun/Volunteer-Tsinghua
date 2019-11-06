from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from datetime import datetime, timezone

from server.models import *
from server.utils import login_required

class detailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class detailView(GenericAPIView):
    serializer_class = detailSerializer

    @login_required
    def post(self, request):
        serializer = detailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.save()
        return Response({'id': project.id})
    
    @login_required
    def get(self, request):
        id = self.request.query_params.get('id')
        project = get_object_or_404(Project, id=id)
        serializer = self.get_serializer(project)
        res = dict(serializer.data)
        if project.finished:
            res['status'] = 'F'
        else:
            apply_records = ApplyRecord.objects.filter(user=request.user, project=project)
            if apply_records.exists():
                apply_record = apply_records[0]
                res['status'] = apply_record.status
            else:
                if project.deadline >= datetime.now(timezone.utc):
                    res['status'] = 'A'
                else:
                    res['status'] = 'N'
        return Response(res)

class listView(ListAPIView):
    queryset = Project.objects.all()
    serializer_class = detailSerializer