# TestingRunner

>
> TestingRunner前端部署
>

```
部署修改字段描述：
    1、修改/src/restful/api.js baseUrl地址, TestingRunner容器运行的宿主机地址
```

```
测试环境部署：
    1、npm install   下载依赖
    2、npm run dev   运行

```

```
生产环境Docker部署：
    1. 修改default.conf配置文件 server_name的ip(宿主机IP)     # 端口默认8080
    2. 执行npm install, npm run build                     # 生成生产环境包
    3. docker build -t testingweb:latest .               # 构建docker镜像
    4. docker run -d --name testingweb -p 8082:8080 --restart always testingweb:latest  # 后台运行docker容器
    5. url: http://宿主机ip:8082
    6. 配置差的Linux Docker部署可能会部署不了，下面是Linux部署后重启Docker的重启或者关闭命令
                启动          systemctl start docker
                守护进程重启    sudo systemctl daemon-reload
                重启docker服务   systemctl restart  docker
                重启docker服务  sudo service docker restart
                关闭docker        service docker stop
                关闭docker        systemctl stop docker
```

```
feat：  新增 feature
fix:    修复 bug
docs:   仅仅修改了文档，比如 README, CHANGELOG, CONTRIBUTE等等
style:  仅仅修改了空格、格式缩进、逗号等等，不改变代码逻辑
refactor: 代码重构，没有加新功能或者修复 bug
perf:   优化相关，比如提升性能、体验
test:   测试用例，包括单元测试、集成测试等
chore:  改变构建流程、或者增加依赖库、工具等
revert: 回滚到上一个版本
```
