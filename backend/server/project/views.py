from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from datetime import datetime, timezone


from server.models import *
from server.utils import login_required
from itertools import chain
from django.db.models import Q
import jieba

class detailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class detailView(GenericAPIView):
    serializer_class = detailSerializer

    @login_required(web=True)
    def post(self, request):
        serializer = detailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.save()
        return Response({'id': project.id})
    
    @login_required(wx=True)
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
    serializer_class = detailSerializer

    @login_required(wx=True, web=True)
    def get_queryset(self):
        return Project.objects.all()


class searchSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields='__all__'

class searchView(ListAPIView):
    serializer_class = searchSerializer

    @login_required(wx=True,web=True)
    def get_queryset(self):
        search = self.request.GET.get("search")

        key_iter=jieba.cut_for_search(search) #分词
        queryset = Project.objects.all()
        
        keywords=[]
        for i in key_iter:
            keywords.append(i)
        print(keywords)

        resultset=queryset.filter(title__icontains=search)

        for i in keywords:
            a_set=queryset.filter(title__icontains=i)
            resultset=chain(resultset, a_set)
            print(resultset)

        for i in keywords:
            a_set=queryset.filter(content__icontains=i)
            resultset=chain(resultset, a_set)
            print(resultset)
    
        resultlist=[]
        for i in resultset:
            if i not in resultlist:
                resultlist.append(i)
        return resultlist