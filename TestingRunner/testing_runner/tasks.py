from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from testing_runner import models
from testing_runner.utils import message
from testing_runner.utils.loader import save_summary, debug_suite, debug_api


@shared_task
def async_debug_api(api, project, name, config=None):
    """异步执行api
    """
    summary = debug_api(api, project, config=config, save=False)
    save_summary(name, summary, project)


@shared_task
def async_debug_suite(suite, project, obj, report, config):
    """异步执行suite
    """
    summary = debug_suite(suite, project, obj, config=config, save=False)
    save_summary(report, summary, project)


@shared_task
def schedule_debug_suite(*args, **kwargs):
    """
    定时任务
    """

    project = kwargs['project']
    suite = []
    test_sets = []
    config_list = []
    for pk in args:
        try:
            name = models.Case.objects.get(id=pk).name
            suite.append({
                'name': name,
                'id': pk
            })
        except ObjectDoesNotExist:
            pass

    for content in suite:
        test_list = models.CaseStep.objects. \
            filter(case__id=content['id']).order_by('step').values('body')

        testcase_list = []
        config = None
        for content in test_list:
            body = eval(content['body'])
            if 'base_url' in body['request'].keys():
                config = eval(models.Config.objects.get(name=body['name'], project__id=project).body)
                continue
            testcase_list.append(body)
        config_list.append(config)
        test_sets.append(testcase_list)
    summary = debug_suite(test_sets, project, suite, config_list, save=False)
    save_summary('', summary, project, type=3)
    strategy = kwargs['strategy']
    if strategy == '始终发送' or (strategy == '仅失败发送' and summary['stat']['failures'] > 0):
        webhook = kwargs.get('webhook', '')
        if webhook:
            summary['name'] = kwargs['task_name']
            message.send_message(summary=summary, webhook=webhook)
        receiver = kwargs.get('receiver', '')
        if receiver:
            receiver = receiver.split(';')
            cc_mail = kwargs.get('copy', '')
            if cc_mail:
                cc_mail = cc_mail.split(';')
            message.send_message_email(summary=summary, receivers=receiver, cc_mail=cc_mail)




