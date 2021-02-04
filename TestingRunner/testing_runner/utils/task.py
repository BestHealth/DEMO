import json
import logging
from djcelery import models as celery_models

from testing_runner.utils import response
from testing_runner.utils.parser import format_json

logger = logging.getLogger('TestingRunner')


class Task(object):
    """
    定时任务操作
    """

    def __init__(self, **kwargs):
        logger.info('before process task data:\n {kwargs}'.format(kwargs=format_json(kwargs)))
        self.__name = kwargs['name']
        self.__data = kwargs['data']
        self.__corntab = kwargs['corntab']
        self.__switch = kwargs['switch']
        self.__task = 'testing_runner.tasks.schedule_debug_suite'
        self.__project = kwargs['project']
        self.__email = {
            "task_name": self.__name,
            'strategy': kwargs['strategy'],
            'copy': kwargs['copy'],
            'receiver': kwargs['receiver'],
            'corntab': self.__corntab,
            'project': self.__project,
            'webhook': kwargs['webhook']
        }
        self.__corntab_time = None

    def format_corntab(self):
        """
        格式化时间
        说明：
        *    *    *    *    *
        -    -    -    -    -
        |    |    |    |    |
        |    |    |    |    +----- day of week (0 - 7) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
        |    |    |    +---------- month (1 - 12) OR jan,feb,mar,apr ...
        |    |    +--------------- day of month (1 - 31)
        |    +-------------------- hour (0 - 23)
        +------------------------- minute (0 - 59)
        minute：分钟，范围0-59；
        hour：小时，范围0-23；
        day_of_week：星期几，范围0-6。以星期天为开始，即0为星期天。这个星期几还可以使用英文缩写表示，例如“sun”表示星期天；
        day_of_month：每月第几号，范围1-31；
        month_of_year：月份，范围1-12。
        """
        corntab = self.__corntab.split(' ')
        if len(corntab) > 5:
            return response.TASK_TIME_ILLEGAL
        try:
            self.__corntab_time = {
                'day_of_week': corntab[4],
                'month_of_year': corntab[3],
                'day_of_month': corntab[2],
                'hour': corntab[1],
                'minute': corntab[0]
            }
        except Exception:
            return response.TASK_TIME_ILLEGAL

        return response.TASK_ADD_SUCCESS

    def add_task(self):
        """
        add tasks
        """
        if celery_models.PeriodicTask.objects.filter(name__exact=self.__name).count() > 0:
            logger.info('{name} tasks exist'.format(name=self.__name))
            return response.TASK_HAS_EXISTS

        if self.__email['strategy'] == '始终发送' or self.__email['strategy'] == '仅失败发送':
            if self.__email['receiver'] == '':
                return response.TASK_EMAIL_ILLEGAL

        resp = self.format_corntab()
        if resp['success']:
            task, created = celery_models.PeriodicTask.objects.get_or_create(name=self.__name, task=self.__task)
            crontab = celery_models.CrontabSchedule.objects.filter(**self.__corntab_time).first()
            if crontab is None:
                crontab = celery_models.CrontabSchedule.objects.create(**self.__corntab_time)
            task.crontab = crontab
            task.enabled = self.__switch
            task.args = json.dumps(self.__data, ensure_ascii=False)
            task.kwargs = json.dumps(self.__email, ensure_ascii=False)
            task.description = self.__project
            task.save()
            logger.info('{name} tasks save success'.format(name=self.__name))
            return response.TASK_ADD_SUCCESS
        else:
            return resp

    def update_task(self, pk):
        resp = self.format_corntab()
        if resp["success"]:
            task = celery_models.PeriodicTask.objects.get(id=pk)
            crontab = celery_models.CrontabSchedule.objects.filter(**self.__corntab_time).first()
            if crontab is None:
                crontab = celery_models.CrontabSchedule.objects.create(**self.__corntab_time)
            task.crontab = crontab
            task.enabled = self.__switch
            task.args = json.dumps(self.__data, ensure_ascii=False)
            task.kwargs = json.dumps(self.__email, ensure_ascii=False)
            task.description = self.__project
            task.name = self.__name
            task.save()
            logger.info("{name} tasks save success".format(name=self.__name))
            return response.TASK_UPDATE_SUCCESS
        else:
            return resp


