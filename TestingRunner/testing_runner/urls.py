from django.urls import path, re_path

from testing_runner.views import project, api, suite, config, schedule, run, report, mock_client, mock_server, dashboard

urlpatterns = [
    # 首页详细信息
    path('dashboard/', dashboard.possess),

    # 项目相关接口地址
    path('project/', project.ProjectView.as_view({
        'get': 'list',
        'post': 'add',
        'patch': 'update',
        'delete': 'delete'
    })),
    path('project/<int:pk>/', project.ProjectView.as_view({'get': 'single'})),

    # 文件上传 修改 删除接口地址
    # path('file/', project.FileView.as_view()),

    # 二叉树接口地址
    path('tree/<int:pk>/', project.TreeView.as_view()),

    # api接口模板地址
    path('api/', api.APITemplateView.as_view({
        'post': 'add',
        'get': 'list'
    })),

    path('api/move_api/', api.APITemplateView.as_view({
        "patch": "move",
    })),

    path('api/<int:pk>/', api.APITemplateView.as_view({
        'delete': 'delete',
        'get': 'single',
        'patch': 'update',
        'post': 'copy'
    })),

    path('api/sync/<int:pk>/', api.APITemplateView.as_view({
        "patch": "sync_case",  # api同步用例步骤
    })),

    # test接口地址
    path('test/', suite.TestCaseView.as_view({
        'get': 'get',
        'post': 'post',
        'delete': 'delete'
    })),

    path('test/<int:pk>/', suite.TestCaseView.as_view({
        'delete': 'delete',
        'post': 'copy',
        "put": "put"  # 请求方法和处理方法同名时可以省略
    })),

    path('teststep/<int:pk>/', suite.CaseStepView.as_view()),

    path('test/move_case/', suite.TestCaseView.as_view({
        "patch": "move",
    })),

    # config接口地址
    path('config/', config.ConfigView.as_view({
        'post': 'add',
        'get': 'list',
        'delete': 'delete'
    })),

    path('config/<int:pk>/', config.ConfigView.as_view({
        'post': 'copy',
        'delete': 'delete',
        'patch': 'update',
        'get': 'all'
    })),

    # Variables接口地址
    path('variables/', config.VariablesView.as_view({
        'post': 'add',
        'get': 'list',
        'delete': 'delete'
    })),

    path('variables/<int:pk>/', config.VariablesView.as_view({
        'delete': 'delete',
        'patch': 'update'
    })),

    # HostIP接口地址
    path('host_ip/', config.HostIPView.as_view({
        'post': 'add',
        'get': 'list',
        'delete': 'delete'
    })),

    path('host_ip/<int:pk>/', config.HostIPView.as_view({
        'delete': 'delete',
        'patch': 'update',
        'get': 'all'
    })),

    # debugtalk.py相关接口地址
    path('debugtalk/<int:pk>/', project.DebugTalkView.as_view({'get': 'debugtalk'})),
    path('debugtalk/', project.DebugTalkView.as_view({
        'patch': 'update',
        'post': 'run'
    })),

    # 定时任务相关接口
    path('schedule/', schedule.ScheduleView.as_view({
        'get': 'list',
        'post': 'add',
        'delete': 'delete'
    })),

    path('schedule/<int:pk>/', schedule.ScheduleView.as_view({
        "get": "run",
        'delete': 'delete',
        'put': 'update',
        'patch': 'up_switch'
    })),

    # run api
    path('run_api_pk/<int:pk>/', run.run_api_pk),
    path('run_api_tree/', run.run_api_tree),
    path('run_api/', run.run_api),

    # run testsuite
    path('run_testsuite/', run.run_testsuite),
    path('run_test/', run.run_test),
    path('run_testsuite_pk/<int:pk>/', run.run_testsuite_pk),
    path('run_suite_tree/', run.run_suite_tree),
    path('automation_test/', run.automation_test),

    # 报告地址
    path('reports/', report.ReportView.as_view({
        'get': 'list'
    })),

    path('reports/<int:pk>/', report.ReportView.as_view({
        'delete': 'delete',
        'get': 'look'
    })),

    # mockApi接口模板地址
    path('mock_client/', mock_client.MOCKClientTemplateView.as_view({
        'post': 'add',
        'get': 'list'
    })),

    path('mock_client/<int:pk>/', mock_client.MOCKClientTemplateView.as_view({
        'delete': 'delete',
        'get': 'single',
        'put': 'update',
        'post': 'copy',
        'patch': 'up_switch'
    })),

    path('mock_client/move_api/', mock_client.MOCKClientTemplateView.as_view({
        "patch": "move",
    })),

    re_path(r'mock/(?P<pk>\d+)/.', mock_server.MOCKServerTemplateView.as_view({
        "get": "mockServer",
        "post": "mockServer",
    })),

    path('run_mock/<int:pk>/', mock_client.MOCKClientTemplateView.as_view({
        'get': 'run_mock'
    })),
]
