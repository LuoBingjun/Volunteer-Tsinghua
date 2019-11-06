from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from server.models import *
from server.utils import login_required

class createSerializer(serializers.ModelSerializer):
    # cover = serializers.ImageField(use_url=True)
    class Meta:
        model = SignProject
        fields = '__all__'

class projectView(CreateAPIView):
    @login_required
    def post(self, request):
        serializer = createSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sign_project = serializer.save()
        return Response({'id': sign_project.id})

class listSerializer(serializers.ModelSerializer):
    # cover = serializers.ImageField(use_url=True)
    class Meta:
        model = SignProject
        fields = '__all__'

class listView(ListAPIView):
    serializer_class = listSerializer
    def get_queryset(self):
        project = self.request.query_params.get('project')
        return SignProject.objects.filter(project=project)

class signinSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignRecord
        fields = ['sign_project']

class signinView(APIView):
    @login_required
    def post(self, request):
        serializer = signinSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.validated_data['sign_project'].project
        join_record = get_object_or_404(JoinRecord, user=request.user, project=project)
        serializer.validated_data['join_record'] = join_record
        sign_record = serializer.save()
        return Response({'id': sign_record.id})