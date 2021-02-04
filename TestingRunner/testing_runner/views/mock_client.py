from django.core.exceptions import ObjectDoesNotExist
from django.db import DataError
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
import datetime

from testing_runner import serializers, models
from testing_runner.utils import response
from testing_runner.utils.decorator import request_log
from testing_runner.utils.mock import run_mock
from testing_runner.utils.parser import Format, Parse, ResponseFront


class MOCKClientTemplateView(GenericViewSet):
    """
    MOCK API操作视图
    """
    serializer_class = serializers.MockClientSerializer
    queryset = models.Mock.objects

    @method_decorator(request_log(level='INFO'))
    def add(self, request):
        """
        新增一个接口
        """

        api = Format(request.data)
        api.parse()

        api_body = {
            'name': api.name,
            'request_body': api.testcase,
            'url': api.url,
            'method': api.method,
            'project': models.Project.objects.get(id=api.project),
            'relation': api.relation,
            'description': api.description,
            'creator': request.user.username
        }

        if api.response_body:
            api_body.update({'response_body': api.response_body})

        try:
            models.Mock.objects.create(**api_body)
        except DataError:
            return Response(response.DATA_TO_LONG)

        return Response(response.API_ADD_SUCCESS)

    @method_decorator(request_log(level='DEBUG'))
    def list(self, request):
        """
        返回接口列表
        """

        node = request.query_params['node']
        project = request.query_params['project']
        search = request.query_params['search']
        queryset = self.get_queryset().filter(project__id=project).order_by('-create_time')

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
    def delete(self, request, **kwargs):
        """
        删除
        """

        try:
            if kwargs.get('pk'):
                models.Mock.objects.get(id=kwargs['pk']).delete()
            else:
                for content in request.data:
                    models.Mock.objects.get(id=content['id']).delete()

        except ObjectDoesNotExist:
            return Response(response.API_NOT_FOUND)

        return Response(response.API_DEL_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def single(self, request, **kwargs):
        """
        查询单个api，返回body信息
        """
        try:
            api = models.Mock.objects.get(id=kwargs['pk'])
        except ObjectDoesNotExist:
            return Response(response.API_NOT_FOUND)

        parse = Parse(eval(api.request_body))
        parse.parse_http()
        response_body = ResponseFront(eval(api.response_body))
        response_body.response_http()
        body = dict(parse.testcase, **response_body.response_body)
        resp = {
            'id': api.id,
            'body': body,
            'success': True,
        }

        return Response(resp)

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
            'request_body': api.testcase,
            'response_body': api.response_body,
            'url': api.url,
            'method': api.method,
            'description': api.description,
            'updater': request.user.username
        }

        try:
            models.Mock.objects.filter(id=pk).update(**api_body, update_time=datetime.datetime.now())
        except ObjectDoesNotExist:
            return Response(response.API_NOT_FOUND)

        return Response(response.API_UPDATE_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def copy(self, request, **kwargs):

        pk = kwargs['pk']
        name = request.data['name']
        api = models.Mock.objects.get(id=pk)
        body = eval(api.request_body)
        body['name'] = name
        api.request_body = body
        api.status = False
        api.id = None
        api.name = name
        api.creator = request.user.username
        api.updater = request.user.username
        api.save()
        return Response(response.API_ADD_SUCCESS)

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
            models.Mock.objects.filter(
                project=project,
                id__in=ids).update(
                relation=relation)
        except ObjectDoesNotExist:
            return Response(response.API_NOT_FOUND)

        return Response(response.API_UPDATE_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def up_switch(self, request, **kwargs):
        """
        更新接口的状态
        """
        if request.data['status'] and models.Mock.objects.filter(
                url=request.data['url'], status=True
        ):
            return Response(response.API_UPDATE_EXISTS)
        api_obj = self.get_queryset().get(pk=kwargs['pk'])
        api_obj.status = request.data['status']
        api_obj.save()
        return Response(response.API_UPDATE_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def run_mock(self, request, **kwargs):
        """
        测试MOCK 接口
        """
        pk = kwargs['pk']
        base_url = request.query_params['base_url']
        mock = models.Mock.objects.filter(id=pk).first()
        summary = run_mock(mock, base_url)
        return Response(summary)
