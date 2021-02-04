from django.db import models

# Create your models here.
from django.db import models

from testing_user.models import BaseTable


class Project(BaseTable):
    """
    项目信息表
    """

    class Meta:
        verbose_name = '项目信息'
        db_table = 'project'

    name = models.CharField('项目名称', unique=True, null=False, max_length=100, db_index=True)
    desc = models.CharField('简要介绍', max_length=100, null=False)
    responsible = models.CharField('创建人', max_length=20, null=False, db_index=True)


class Debugtalk(BaseTable):
    """
    驱动文件表
    """

    class Meta:
        verbose_name = '驱动库'
        db_table = 'debugtalk'

    code = models.TextField('python代码', default='# write you code', null=False)
    project = models.OneToOneField(to=Project, on_delete=models.CASCADE, db_index=True)


class Config(BaseTable):
    """
    环境信息表
    """

    class Meta:
        verbose_name = '环境信息'
        db_table = 'config'

    name = models.CharField('环境名称', null=False, max_length=100, db_index=True)
    body = models.TextField('主体信息', null=False)
    base_url = models.CharField('请求地址', null=False, max_length=1024, db_index=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, db_index=True)


class API(BaseTable):
    """
    API信息表
    """

    class Meta:
        verbose_name = '接口信息'
        db_table = 'api'

    name = models.CharField('接口名称', null=False, max_length=100, db_index=True)
    body = models.TextField('主体信息', null=False)
    url = models.CharField('请求地址', null=False, max_length=1024)
    method = models.CharField('请求方式', null=False, max_length=10)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, db_index=True)
    relation = models.IntegerField('节点id', null=False, db_index=True)


class Case(BaseTable):
    """
    用例信息表
    """

    class Meta:
        verbose_name = '用例信息'
        db_table = 'case'

    tag = (
        (1, '冒烟用例'),
        (2, '集成用例'),
        (3, '监控脚本')
    )
    name = models.CharField('用例名称', null=False, max_length=100, db_index=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, db_index=True)
    relation = models.IntegerField('节点id', null=False, db_index=True)
    length = models.IntegerField('API个数', null=False)
    tag = models.IntegerField('用例标签', choices=tag, default=2)


class CaseStep(BaseTable):
    """
    Test Case Step
    """

    class Meta:
        verbose_name = '用例信息 Step'
        db_table = 'case_step'

    name = models.CharField('用例名称', null=False, max_length=100, db_index=True)
    body = models.TextField('主体信息', null=False)
    url = models.CharField('请求地址', null=False, max_length=1024)
    method = models.CharField('请求方式', null=False, max_length=10)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, db_index=True)
    step = models.IntegerField('顺序', null=False)
    source_api_id = models.IntegerField("api来源", null=False)


class HostIP(BaseTable):
    """
    全局变量
    """

    class Meta:
        verbose_name = 'HOST配置'
        db_table = 'host_ip'

    name = models.CharField(null=False, max_length=100, db_index=True)
    value = models.TextField(null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, db_index=True)


class Variables(BaseTable):
    """
    全局变量
    """

    class Meta:
        verbose_name = '全局变量'
        db_table = 'variables'

    key = models.CharField(null=False, max_length=100, db_index=True)
    value = models.CharField(null=False, max_length=1024)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, db_index=True)
    description = models.CharField("全局变量描述", null=True, max_length=1024)


class Report(BaseTable):
    """
    报告存储
    """
    report_type = (
        (1, '调试'),
        (2, '异步'),
        (3, '定时')
    )

    class Meta:
        verbose_name = '测试报告'
        db_table = 'report'

    name = models.CharField('报告名称', null=False, max_length=100, db_index=True)
    type = models.IntegerField('报告类型', choices=report_type)
    summary = models.TextField('报告基本信息', null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, db_index=True)


class ReportDetail(BaseTable):
    class Meta:
        verbose_name = "测试报告详情"
        db_table = "report_detail"

    report = models.OneToOneField(Report, on_delete=models.CASCADE, null=True, db_constraint=False, db_index=True)
    summary_detail = models.TextField("报告详细信息")


class Relation(models.Model):
    """
    树形结构关系
    """

    class Meta:
        verbose_name = '树形结构关系'
        db_table = 'relation'

    project = models.ForeignKey(Project, on_delete=models.CASCADE, db_index=True)
    tree = models.TextField('结构主题', null=False, default=[])
    type = models.IntegerField('树类型', default=1)


class Mock(BaseTable):
    """
    Mock信息表
    """

    class Meta:
        verbose_name = 'Mock接口信息'
        db_table = 'mock'

    name = models.CharField('接口名称', null=False, max_length=100, db_index=True)
    request_body = models.TextField('主体信息', null=False)
    response_body = models.TextField('主体信息', null=False)
    url = models.CharField('请求地址', null=False, max_length=1024)
    method = models.CharField('请求方式', null=False, max_length=10)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, db_index=True)
    relation = models.IntegerField('节点id', null=False, db_index=True)
    description = models.CharField("Mock接口描述", null=True, max_length=1024)
    status = models.BooleanField('状态', default=False)
