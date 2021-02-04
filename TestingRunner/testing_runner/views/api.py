from django.core.exceptions import ObjectDoesNotExist
from django.db import DataError
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
import datetime

from testing_runner import serializers, models
from testing_runner.utils import response
from testing_runner.utils.decorator import request_log
from testing_runner.utils.parser import Format, Parse


class APITemplateView(GenericViewSet):
    """
    API操作视图
    """
    serializer_class = serializers.APISerializer
    queryset = models.API.objects

    @method_decorator(request_log(level='DEBUG'))
    def list(self, request):
        """
        返回接口列表 ==>
        http://127.0.0.1:8000/api/runner/api/?token=90d9a73dce44a8c0233be73db975adba&node=1&project=4&search=
        node 树形节点ID
        """

        node = request.query_params['node']
        project = request.query_params['project']
        search = request.query_params['search']
        queryset = self.get_queryset().filter(project__id=project).order_by('-update_time')

        # 精确大小写，根据接口名查询
        if search != '':
            queryset = queryset.filter(name__contains=search)

        # 根据树ID查询
        if node != '':
            queryset = queryset.filter(relation=node)

        pagination_queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(pagination_queryset, many=True)

        return self.get_paginated_response(serializer.data)

    @method_decorator(request_log(level='INFO'))
    def add(self, request):
        """
        新增一个接口
        """

        api = Format(request.data)
        api.parse()

        api_body = {
            'name': api.name,
            'body': api.testcase,
            'url': api.url,
            'method': api.method,
            'project': models.Project.objects.get(id=api.project),
            'relation': api.relation,
            'creator': request.user.username
        }

        try:
            models.API.objects.create(**api_body)
        except DataError:
            return Response(response.DATA_TO_LONG)

        return Response(response.API_ADD_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def update(self, request, **kwargs):
        """
        更新接口
        """
        pk = kwargs['pk']
        api = Format(request.data)
        api.parse()

        api_body = {
            'name': api.name,
            'body': api.testcase,
            'url': api.url,
            'method': api.method,
            'updater': request.user.username
        }

        try:
            models.API.objects.filter(id=pk).update(**api_body, update_time=datetime.datetime.now())
        except ObjectDoesNotExist:
            return Response(response.API_NOT_FOUND)

        return Response(response.API_UPDATE_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def copy(self, request, **kwargs):
        """
        {
            'name': '12'
        } ==> /api/runner/api/8/?token=90d9a73dce44a8c0233be73db975adba
        """
        pk = kwargs['pk']
        name = request.data['name']
        api = models.API.objects.get(id=pk)
        body = eval(api.body)
        body['name'] = name
        api.body = body
        api.id = None
        api.name = name
        api.creator = request.user.username
        api.updater = request.user.username
        api.save()
        return Response(response.API_ADD_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def delete(self, request, **kwargs):
        """
        删除
        """

        try:
            if kwargs.get('pk'):
                models.API.objects.get(id=kwargs['pk']).delete()
            else:
                for content in request.data:
                    models.API.objects.get(id=content['id']).delete()

        except ObjectDoesNotExist:
            return Response(response.API_NOT_FOUND)

        return Response(response.API_DEL_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def single(self, request, **kwargs):
        """
        查询单个api，返回body信息
        """
        try:
            api = models.API.objects.get(id=kwargs['pk'])
        except ObjectDoesNotExist:
            return Response(response.API_NOT_FOUND)

        parse = Parse(eval(api.body))
        parse.parse_http()

        resp = {
            'id': api.id,
            'body': parse.testcase,
            'success': True,
        }

        return Response(resp)

    @method_decorator(request_log(level='INFO'))
    def sync_case(self, request, **kwargs):
        """
        api同步至用例
        """
        pk = kwargs['pk']
        source_api = models.API.objects.filter(pk=pk).values("name", "body", "url", "method").first()
        case_steps = models.CaseStep.objects.filter(source_api_id=pk)
        case_steps.update(**source_api, updater=request.user.username)
        case_ids = case_steps.values('case')
        models.Case.objects.filter(pk__in=case_ids).update(updater=request.user.username)
        return Response(response.API_SYNC_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def move(self, request):
        """
        移动api到指定目录
        """
        project = request.data.get('project')
        relation = request.data.get('relation')
        apis = request.data.get('api')
        ids = [api['id'] for api in apis]

        try:
            models.API.objects.filter(
                project=project,
                id__in=ids).update(
                relation=relation)
        except ObjectDoesNotExist:
            return Response(response.API_NOT_FOUND)

        return Response(response.API_UPDATE_SUCCESS)
