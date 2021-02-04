from django.utils.decorators import method_decorator
from djcelery import models
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from TestingRunner import pagination
from TestingRunner.celery import app
from testing_runner import serializers
from testing_runner.utils import response
from testing_runner.utils.decorator import request_log
from testing_runner.utils.task import Task


class ScheduleView(GenericViewSet):
    """
    定时任务增删改查
    """
    queryset = models.PeriodicTask.objects
    serializer_class = serializers.PeriodicTaskSerializer
    pagination_class = pagination.MyPageNumberPagination

    @method_decorator(request_log(level='DEBUG'))
    def list(self, request):
        """
        查询项目定时任务
        """
        project = request.query_params.get('project')
        search = request.query_params['search']

        schedule = self.get_queryset().filter(description=project).order_by('-date_changed')
        if '' != search:
            schedule = schedule.filter(name__contains=search)

        page_schedule = self.paginate_queryset(schedule)
        serializer = self.get_serializer(page_schedule, many=True)
        return self.get_paginated_response(serializer.data)

    @method_decorator(request_log(level='INFO'))
    def add(self, request):
        """新增定时任务
        """
        task = Task(**request.data)
        resp = task.add_task()
        return Response(resp)

    @method_decorator(request_log(level='INFO'))
    def update(self, request, **kwargs):
        """
        修改定时任务
        """
        task = Task(**request.data)
        resp = task.update_task(kwargs['pk'])
        return Response(resp)

    @method_decorator(request_log(level='INFO'))
    def delete(self, request, **kwargs):
        """
        删除任务
        """

        if kwargs.get('pk'):
            task = models.PeriodicTask.objects.get(id=kwargs['pk'])
            # 任务标记为 SKIPPED，直接跳过
            task.enabled = False
            task.delete()
        else:
            for content in request.data:
                task = models.PeriodicTask.objects.get(id=content['id'])
                task.enabled = False
                task.delete()

        return Response(response.TASK_DEL_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def run(self, request, **kwargs):
        """
        手动触发
        """
        task = models.PeriodicTask.objects.get(id=kwargs["pk"])
        task_name = 'testing_runner.tasks.schedule_debug_suite'
        args = eval(task.args)
        kwargs = eval(task.kwargs)
        app.send_task(name=task_name, args=args, kwargs=kwargs)
        return Response(response.TASK_RUN_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def up_switch(self, request, **kwargs):
        """
        更新任务的状态
        """
        task_obj = self.get_queryset().get(pk=kwargs['pk'])
        task_obj.enabled = request.data['switch']
        task_obj.save()
        return Response(response.TASK_UPDATE_SUCCESS)

