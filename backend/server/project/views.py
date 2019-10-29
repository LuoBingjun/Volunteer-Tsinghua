from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from server.models import *
from server.utils import login_required

class detailSerializer(serializers.ModelSerializer):
    # cover = serializers.ImageField(use_url=True)
    class Meta:
        model = Project
        fields = '__all__'

class detailView(APIView):
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
        serializer = detailSerializer(project)
        return Response(serializer.data)

class listView(ListAPIView):
    queryset = Project.objects.all()
    serializer_class = detailSerializer