import re
import requests
import json
from TestingRunner import settings
from testing_runner import models
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL


def render_email(content, data):

    for key, val in data.items():
        content = re.sub('\{.*' + key + '.*\}', str(val), content)
    return content


def parse_message(summary, messageType):
    task_name = summary['name']
    rows_count = summary['stat']['testsRun']
    pass_count = summary['stat']['successes']
    fail_count = summary['stat']['failures']
    error_count = summary['stat']['errors']
    duration = '%.2fs' % summary['time']['duration']
    report_id = models.Report.objects.last().id
    report_url = '{}/api/runner/reports/{}/'.format(settings.REPORT_URL, report_id)
    executed = rows_count
    fail_rate = '{:.2%}'.format(fail_count / executed)
    if 'send_message' == messageType:
        text = '任务名称: {}\n 总共耗时: {}\n 成功接口: {}个\n 异常接口: {}个\n 失败接口: {}个\n ' \
               '失败比例: {}\n 查看详情: {}'.\
            format(task_name, duration, pass_count, error_count, fail_count, fail_rate, report_url)
        return text
    elif 'send_message_email' == messageType:
        mail_content = {
            'task_name': task_name,
            'duration': duration,
            'pass_count': pass_count,
            'error_count': error_count,
            'fail_count': fail_count,
            'fail_rate': fail_rate,
            'report_url': report_url
        }
        return mail_content


def send_message(summary: dict, webhook: str):
    msg = parse_message(summary=summary, messageType='send_message')
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'msgtype': 'markdown',
        'markdown': {
            'title': 'TestingRunner管理平台测试报告',
            'text': msg
        },
        'at': {
            'atMobiles': [
                '15367262993'
            ],
            'isAtAll': False
        }
    }
    requests.post(url=webhook, data=json.dumps(data).encode('utf-8'), headers=headers)


def send_message_email(summary, receivers, cc_mail):
    email_server = settings.EMAIL_SERVER
    email_username = settings.EMAIL_USERNAME
    email_password = settings.EMAIL_PASSWORD
    data = parse_message(summary=summary, messageType='send_message_email')
    email_sender = settings.EMAIL_SENDER
    mail_title = 'TestingRunner管理平台报告'
    email_template = settings.BASE_DIR.joinpath('templates/message_email.html')
    with open(email_template, encoding='utf8') as f:
        mail_msg = f.read()
    mail_msg = render_email(mail_msg, data)
    smtp = SMTP_SSL(email_server)
    smtp.ehlo(email_server)
    smtp.login(email_username, email_password)
    msg = MIMEText(mail_msg, 'html', 'utf-8')
    msg['Cc'] = ','.join(cc_mail)
    msg['Subject'] = Header(mail_title, 'utf-8')
    msg['From'] = email_username
    msg['To'] = Header('TestingRunner平台默认别名', 'utf-8')
    smtp.sendmail(email_sender, receivers + cc_mail, msg.as_string())
    smtp.quit()


