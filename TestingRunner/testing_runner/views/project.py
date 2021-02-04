import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from TestingRunner import pagination
from testing_runner import models, serializers
from testing_runner.utils import response, prepare
from testing_runner.utils.decorator import request_log
from testing_runner.utils.runner import DebugCode
from testing_runner.utils.tree import get_tree_max_id


class ProjectView(GenericViewSet):
    """
    项目CRUD
    """
    queryset = models.Project.objects.all().order_by('-update_time')
    serializer_class = serializers.ProjectSerializer
    pagination_class = pagination.MyCursorPagination

    @method_decorator(request_log(level='DEBUG'))
    def list(self, request):
        """
        查询项目信息
        """
        project_name = request.query_params['project']
        responsible_name = request.query_params['responsible']

        projects = self.get_queryset()

        if '' != project_name:
            projects = projects.filter(name__contains=project_name)
        if '' != responsible_name:
            projects = projects.filter(responsible__contains=responsible_name)

        page_projects = self.paginate_queryset(projects)
        serializer = self.get_serializer(page_projects, many=True)
        return self.get_paginated_response(serializer.data)

    @method_decorator(request_log(level='INFO'))
    def add(self, request):
        """添加项目
        """

        name = request.data['name']
        username = request.user.username

        if models.Project.objects.filter(name=name).first():
            response.PROJECT_EXISTS['name'] = name
            return Response(response.PROJECT_EXISTS)
        # 反序列化
        serializer = serializers.ProjectSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            project = models.Project.objects.get(name=name)
            prepare.project_init(project, username)
            return Response(response.PROJECT_ADD_SUCCESS)

        return Response(response.SYSTEM_ERROR)

    @method_decorator(request_log(level='INFO'))
    def update(self, request):
        """
        编辑项目
        """

        try:
            project = models.Project.objects.get(id=request.data['id'])
        except (KeyError, ObjectDoesNotExist):
            return Response(response.SYSTEM_ERROR)

        if request.data['name'] != project.name:
            if models.Project.objects.filter(name=request.data['name']).first():
                return Response(response.PROJECT_EXISTS)

        project.name = request.data['name']
        project.desc = request.data['desc']
        project.save()

        return Response(response.PROJECT_UPDATE_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def delete(self, request):
        """
        删除项目
        """
        try:
            if isinstance(request.data, dict):
                project = models.Project.objects.get(id=request.data['id'])
                project.delete()
                prepare.project_end(project)
            else:
                for project_data in request.data:
                    project = models.Project.objects.get(id=project_data['id'])
                    project.delete()
                    prepare.project_end(project)
            return Response(response.PROJECT_DELETE_SUCCESS)
        except ObjectDoesNotExist:
            return Response(response.SYSTEM_ERROR)

    @method_decorator(request_log(level='INFO'))
    def single(self, request, **kwargs):
        """
        得到单个项目相关统计信息
        """
        pk = kwargs.pop('pk')

        try:
            queryset = models.Project.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(response.PROJECT_NOT_EXISTS)

        serializer = self.get_serializer(queryset, many=False)

        project_info = prepare.get_project_detail(pk)
        project_info.update(serializer.data)

        return Response(project_info)


class DebugTalkView(GenericViewSet):
    """
    DebugTalk update
    """

    serializer_class = serializers.DebugTalkSerializer

    @method_decorator(request_log(level='INFO'))
    def debugtalk(self, request, **kwargs):
        """
        得到debugtalk
        """
        pk = kwargs.pop('pk')
        try:
            queryset = models.Debugtalk.objects.get(project__id=pk)
        except ObjectDoesNotExist:
            return Response(response.DEBUGTALK_NOT_EXISTS)

        serializer = self.get_serializer(queryset, many=False)

        return Response(serializer.data)

    @method_decorator(request_log(level='INFO'))
    def update(self, request):
        """
        编辑debugtalk.py 代码并保存
        """
        pk = request.data['id']
        username = request.user.username
        try:
            models.Debugtalk.objects.filter(id=pk). \
                update(code=request.data['code'], updater=username, update_time=datetime.datetime.now())

        except ObjectDoesNotExist:
            return Response(response.SYSTEM_ERROR)

        return Response(response.DEBUGTALK_UPDATE_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def run(self, request):
        """
        在线运行
        """
        try:
            code = request.data['code']
        except KeyError:
            return Response(response.KEY_MISS)
        debug = DebugCode(code)
        debug.run()
        resp = {
            'msg': debug.resp,
            'success': True,
            'code': '0001'
        }
        return Response(resp)


class TreeView(APIView):
    """
    树形结构操作
    """

    @method_decorator(request_log(level='INFO'))
    def get(self, request, **kwargs):
        """
        返回树形结构
        当前节点ID
        """

        try:
            tree_type = request.query_params['type']
            tree = models.Relation.objects.get(project__id=kwargs['pk'], type=tree_type)
        except KeyError:
            return Response(response.KEY_MISS)

        except ObjectDoesNotExist:
            return Response(response.SYSTEM_ERROR)

        body = eval(tree.tree)  # list
        tree = {
            'tree': body,
            'id': tree.id,
            'success': True,
            'max': get_tree_max_id(body)
        }
        return Response(tree)

    @method_decorator(request_log(level='INFO'))
    def patch(self, request, **kwargs):
        """
        修改树形结构，ID不能重复
        """
        try:
            body = request.data['body']
            mode = request.data['mode']

            relation = models.Relation.objects.get(id=kwargs['pk'])
            relation.tree = body
            relation.save()

        except KeyError:
            return Response(response.KEY_MISS)

        except ObjectDoesNotExist:
            return Response(response.SYSTEM_ERROR)

        #  mode -> True remove node
        if mode:
            prepare.tree_end(request.data, relation.project)

        response.TREE_UPDATE_SUCCESS['tree'] = body
        response.TREE_UPDATE_SUCCESS['max'] = get_tree_max_id(body)

        return Response(response.TREE_UPDATE_SUCCESS)

#
# class FileView(APIView):
#
#     def post(self, request):
#         """
#         接收文件并保存
#         """
#         file = request.FILES['file']
#
#         if models.FileBinary.objects.filter(name=file.name).first():
#             return Response(response.FILE_EXISTS)
#
#         body = {
#             'name': file.name,
#             'body': file.file.read(),
#             'size': get_file_size(file.size)
#         }
#
#         models.FileBinary.objects.create(**body)
#
#         return Response(response.FILE_UPLOAD_SUCCESS)
