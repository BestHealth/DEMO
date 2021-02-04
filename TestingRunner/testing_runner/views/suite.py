import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from testing_runner import models, serializers
from testing_runner.utils import response, prepare
from testing_runner.utils.decorator import request_log


class TestCaseView(GenericViewSet):
    """
    测试用例CRUD
    """
    queryset = models.Case.objects
    serializer_class = serializers.CaseSerializer
    tag_options = {
        '冒烟用例': 1,
        '集成用例': 2,
        '监控脚本': 3
    }

    @method_decorator(request_log(level='INFO'))
    def get(self, request):
        """
        查询指定CASE列表
        """
        node = request.query_params['node']
        project = request.query_params['project']
        search = request.query_params['search']
        # update_time 降序排列
        queryset = self.get_queryset().filter(project__id=project).order_by('-update_time')

        if search != '':
            queryset = queryset.filter(name__contains=search)

        if node != '':
            queryset = queryset.filter(relation=node)

        pagination_query = self.paginate_queryset(queryset)
        serializer = self.get_serializer(pagination_query, many=True)

        return self.get_paginated_response(serializer.data)

    @method_decorator(request_log(level='INFO'))
    def copy(self, request, **kwargs):

        pk = kwargs['pk']
        name = request.data['name']
        relation = request.data.pop('relation')
        project = request.data['project']
        username = request.user.username

        if models.Case.objects.filter(name=name, project_id=project, relation=relation).first():
            return Response(response.CASE_EXISTS)

        case = models.Case.objects.get(id=pk)
        case.id = None
        case.name = name
        case.creator = username
        case.updater = username
        case.save()

        case_step = models.CaseStep.objects.filter(case__id=pk)

        for step in case_step:
            step.id = None
            step.case = case
            step.creator = username
            step.updater = username
            step.save()

        return Response(response.CASE_ADD_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def patch(self, request, **kwargs):
        """
        更新测试用例集,如果是新的接口则没有case节点
        """

        pk = kwargs['pk']
        project = request.data.pop('project')
        body = request.data.pop('body')
        relation = request.data.pop('relation')
        username = request.user.username

        if models.Case.objects.exclude(id=pk). \
                filter(name=request.data['name'],
                       project__id=project,
                       relation=relation).first():
            return Response(response.CASE_EXISTS)

        case = models.Case.objects.get(id=pk)

        prepare.update_casestep(body, case, username)

        request.data['tag'] = self.tag_options[request.data['tag']]
        models.Case.objects.filter(id=pk).update(**request.data, updater=username, update_time=datetime.datetime.now())

        return Response(response.CASE_UPDATE_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def post(self, request):
        """
        新增测试用例集
        """

        try:
            pk = request.data['project']
            relation = request.data['relation']
            name = request.data['name']
            request.data['project'] = models.Project.objects.get(id=pk)
            username = request.user.username

            if models.Case.objects.filter(name=name, project=request.data['project'], relation=relation).first():
                return Response(response.CASE_EXISTS)

        except KeyError:
            return Response(response.KEY_MISS)

        except ObjectDoesNotExist:
            return Response(response.PROJECT_NOT_EXISTS)

        body = request.data.pop('body')

        request.data['tag'] = self.tag_options[request.data['tag']]
        models.Case.objects.create(**request.data, creator=username)

        case = models.Case.objects.filter(**request.data).first()

        prepare.generate_casestep(body, case, username)

        return Response(response.CASE_ADD_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def put(self, request, **kwargs):
        pk = kwargs['pk']

        api_id_list_of_dict = list(
            models.CaseStep.objects.filter(case_id=pk).exclude(method='config').values('source_api_id', 'step'))

        for item in api_id_list_of_dict:
            source_api_id = item['source_api_id']
            if source_api_id == 0:
                continue
            step = item['step']
            source_api = models.API.objects.filter(pk=source_api_id).values("name", "body", "url", "method").first()
            if source_api is not None:
                models.CaseStep.objects.filter(case_id=pk, source_api_id=source_api_id, step=step).update(**source_api)
        models.Case.objects.filter(pk=pk).update(update_time=datetime.datetime.now())
        return Response(response.CASE_STEP_SYNC_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def delete(self, request, **kwargs):

        pk = kwargs.get('pk')

        try:
            if pk:
                prepare.case_end(pk)
            else:
                for content in request.data:
                    prepare.case_end(content['id'])

        except ObjectDoesNotExist:
            return Response(response.SYSTEM_ERROR)

        return Response(response.CASE_DELETE_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def move(self, request):
        project = request.data.get('project')
        relation = request.data.get('relation')
        cases = request.data.get('case')
        ids = [case['id'] for case in cases]
        try:
            models.Case.objects.filter(
                project=project,
                id__in=ids).update(
                relation=relation)
        except ObjectDoesNotExist:
            return Response(response.CASE_NOT_EXISTS)

        return Response(response.CASE_UPDATE_SUCCESS)


class CaseStepView(APIView):
    """
    测试用例step操作视图
    """

    @method_decorator(request_log(level='INFO'))
    def get(self, request, **kwargs):
        """
        返回用例集信息
        """
        pk = kwargs['pk']

        queryset = models.CaseStep.objects.filter(case__id=pk).order_by('step')

        serializer = serializers.CaseStepSerializer(instance=queryset, many=True)

        resp = {
            'case': serializers.CaseSerializer(instance=models.Case.objects.get(id=pk), many=False).data,
            'step': serializer.data
        }
        return Response(resp)

