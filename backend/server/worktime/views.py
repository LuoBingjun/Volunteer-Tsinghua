from django.db import models
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

from rest_framework import generics
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response


from django.shortcuts import get_object_or_404
from server.models import *
from server.utils import login_required


import xlwt
from io import BytesIO
import time, datetime
import xlrd
import codecs
from django.utils.encoding import escape_uri_path
class ViewWorktimeSerializer(serializers.Serializer): 
    project_id = serializers.IntegerField(max_value=None, min_value=0)
    
class ViewWorktime(APIView): 
   
    @login_required(wx=True)
    def get(self, request):
        info = ViewWorktimeSerializer(data=self.request.query_params)
        if info.is_valid():
            _project_id=info.validated_data['project_id']
        #项目存在是否判断
            queryset = JoinRecord.objects.all()
            join_record=get_object_or_404(queryset, user=request.user, project__id=_project_id)
            
            return Response({'worktime':join_record.work_time}, status=200)
            
        else:
            return Response(info.errors, status=400) #数据格式错误



#导出名单
class ExportView(APIView):

    # 导出名单
    def get(self, request):

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path('workname.xls'))
        
        # 创建一个文件对象
        wb = xlwt.Workbook(encoding='utf-8')
        # 创建一个表
        sheet = wb.add_sheet('namelist',cell_overwrite_ok=True)

        # # project_id
        # p_id=request.GET.get('project_id')
        # # 根据projectid获取历次签到的title
        # signproject_set=SignProject.objects.filter(project__id=p_id).order_by('begin_time')

        # 构建表头
        sheet.write(0,0,'id')
        sheet.write(0,1,'姓名')

        # _row=0 # 行 
        # _column=2 # 列

        # # 存储title，便于后续输入
        # signproject_title_dict = {}

        # for i in signproject_set:
        #     sheet.write(_row,_column,i.title)
        #     signproject_title_dict[i.id]=_column
        #     _column=_column+1
    
        # sheet.write(_row,_column,'总工时')

        # # 参加项目的所有人
        # joinrecord_set=JoinRecord.objects.filter(project__id=p_id)

        # _row=1
        # for i in joinrecord_set:
        #     sheet.write(_row,0,i.user.id)
        #     sheet.write(_row,1,i.user.name)

        #     a_signrecord=SignRecord.objects.filter(join_record__id=i.id).order_by('sign_in_time')

        #     alltime=0
        #     for j in a_signrecord:
        #         signal_worktime=0
        #         if j.sign_in_time and j.sign_out_time:
        #             strtime_t1 = j.sign_in_time.strftime("%Y-%m-%d %H:%M:%S")
        #             datetime_t1 = time.strptime(strtime_t1, '%Y-%m-%d %H:%M:%S')
        #             t1 = time.mktime(datetime_t1)

        #             strtime_t2 = j.sign_out_time.strftime("%Y-%m-%d %H:%M:%S")
        #             datetime_t2 = time.strptime(strtime_t2, '%Y-%m-%d %H:%M:%S')
        #             t2 = time.mktime(datetime_t2)

        #             signal_worktime=round((t2-t1)/3600,2)
        #         else:
        #             signal_worktime=0
        #         alltime=alltime+signal_worktime
        #         sheet.write(_row, signproject_title_dict[j.sign_project.id], signal_worktime)

        #     sheet.write(_row, _column, alltime)
        #     _row=_row+1

        wb.save('test.xls')
        output = BytesIO()
        wb.save(output)
        output.seek(0)

        response.write(output.getvalue())
        return response
   


# # 导出名单

# def export_excel(request):

#     if request.method == 'GET':

#         response = HttpResponse(content_type='application/vnd.ms-excel')
#         response['Content-Disposition'] = 'attachment;filename=workname.xls'
    
#         # 创建一个文件对象
#         wb = xlwt.Workbook(encoding='utf8')
#         # 创建一个表
#         sheet = wb.add_sheet('namelist',cell_overwrite_ok=True)

#         # project_id
#         p_id=request.GET.get('project_id') 
#         # 根据projectid获取历次签到的title
#         signproject_set=SignProject.objects.filter(project__id=p_id).order_by('begin_time')

#         # 构建表头
#         sheet.write(0,0,'id')
#         sheet.write(0,1,'姓名')

#         _row=0 # 行 
#         _column=2 # 列

#         # 存储title，便于后续输入
#         signproject_title_dict = {}

#         for i in signproject_set:
#             sheet.write(_row,_column,i.title)
#             signproject_title_dict[i.id]=_column
#             _column=_column+1
    
#         sheet.write(_row,_column,'总工时')

#         # 参加项目的所有人
#         joinrecord_set=JoinRecord.objects.filter(project__id=p_id)

#         _row=1
#         for i in joinrecord_set:
#             sheet.write(_row,0,i.user.id)
#             sheet.write(_row,1,i.user.name)

#             a_signrecord=SignRecord.objects.filter(join_record__id=i.id).order_by('sign_in_time')

#             alltime=0
#             for j in a_signrecord:
#                 signal_worktime=0
#                 if j.sign_in_time and j.sign_out_time:
#                     strtime_t1 = j.sign_in_time.strftime("%Y-%m-%d %H:%M:%S")
#                     datetime_t1 = time.strptime(strtime_t1, '%Y-%m-%d %H:%M:%S')
#                     t1 = time.mktime(datetime_t1)

#                     strtime_t2 = j.sign_out_time.strftime("%Y-%m-%d %H:%M:%S")
#                     datetime_t2 = time.strptime(strtime_t2, '%Y-%m-%d %H:%M:%S')
#                     t2 = time.mktime(datetime_t2)

#                     signal_worktime=round((t2-t1)/3600,2)
#                 else:
#                     signal_worktime=0
#                 alltime=alltime+signal_worktime
#                 sheet.write(_row, signproject_title_dict[j.sign_project.id], signal_worktime)

#             sheet.write(_row, _column, alltime)
#             _row=_row+1


#         output = BytesIO()
#         wb.save(output)
#         output.seek(0)

#         response.write(output.getvalue())
#         return response
#     else:
#         return Response({"error": 'method wrong'},status=405)


class importSerializer(serializers.Serializer): 
    project_id = serializers.IntegerField(max_value=None, min_value=1)
    import_file = serializers.FileField(required=True)
    
class importView(APIView):
    @login_required(web=True)
    def post(self, request):
        serializer = importSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project_id = serializer.validated_data['project_id']
        f = serializer.validated_data['import_file']
        project = get_object_or_404(Project, pk=project_id)
        if not (request.user.is_superuser or request.user == project.webuser):
            raise PermissionDenied()
        records = project.joinrecord_set.all()
        work_time = {}
        try:
            wb = xlrd.open_workbook(filename=None, file_contents=f.read())
            table = wb.sheets()[0]
            nrows = table.nrows
            for i in range(1, nrows):
                id = int(table.cell(i, 0).value)
                value = float(table.cell(i,-1).value)
                work_time[id] = value
        except:
            return Response(status=400)
        for record in records:
            id = record.user.id
            record.work_time = work_time[id]
            record.save()
        return Response(status=200)
