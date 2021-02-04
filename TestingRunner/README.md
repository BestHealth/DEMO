# TestingRunner

>
> TestingRunner后端部署
>

```
环境描述：
    TestingRunner           ---------  项目
        TestingRunner       ---------  项目全局文件
        testing_user        ---------  用户模块（目前用户及对应的权限未完善）
        testing_runner      ---------  自动化模块
```

```
部署修改字段描述：
    1、TestingRunner/settings中数据库相关配置：DATABASES
    2、TestingRunner/settings中MQ相关配置：BROKER_URL
    3、TestingRunner/settings中邮件相关配置：EMAIL_SERVER、EMAIL_USERNAME、EMAIL_PASSWORD、EMAIL_SENDER
    4、TestingRunner/settings中报告URL相关配置：REPORT_URL
```

```
测试环境部署：
    1、pip install -r requirements.txt
    2、python3 manage.py makemigrations testing_user testing_runner
    3、python3 manage.py migrate testing_user testing_runner djcelery
    4、运行
```

```
生产环境部署：
1. 运行部署Mysql数据库，建议拉取mysql5.7镜像
2. 新建数据库
4. 修改settings.py DATABASES 字典相关配置，NAME, USER, PASSWORD, HOST
5. 运行部署rabbitmq
6. 修改settings.py BROKER_URL(配置rabbittmq的IP，username,password)
7. 安装dos2unix：yum install -y dos2unix
8. 切换到TestingRunner目录，Linux环境执行下：dos2unix ./start.sh
9. docker build -t testingrunner:latest .    # 构建docker镜像
9. 运行容器：docker run -d --name testingrunner -p:8081:5000 --restart always testingrunner:latest  # 后台运行docker容器,默认后台端口5000
10. docker exec -it testingrunner /bin/sh  #进入容器内部
11. 部署Django环境
        python3 manage.py makemigrations  (testing_user testing_runner)
        python3 manage.py migrate         (testing_user testing_runner djcelery) 

```

