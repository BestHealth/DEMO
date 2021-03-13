import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/pages/home/Home'
import Dashboard from '@/pages/home/Dashboard'
import Register from '@/pages/auth/Register'
import Login from '@/pages/auth/Login'
import ProjectList from '@/pages/project/ProjectList'
import ProjectDetail from '@/pages/project/ProjectDetail'
import DebugTalk from '@/pages/httprunner/DebugTalk'
import RecordApi from '@/pages/runner/api/RecordApi'
import AutoTest from '@/pages/runner/case/AutoTest'
import GlobalEnv from '@/pages/variables/GlobalEnv'
import ReportList from '@/pages/reports/ReportList'
import RecordConfig from '@/pages/runner/config/RecordConfig'
import Tasks from '@/pages/task/Tasks'
import HostAddress from '@/pages/variables/HostAddress'
import RecordMock from '@/pages/mock/RecordMock'
import VueRouter from "vue-router";


//push
const VueRouterPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(to) {
    return VueRouterPush.call(this, to).catch(err => err)
}

//replace
const VueRouterReplace = VueRouter.prototype.replace
VueRouter.prototype.replace = function replace(to) {
    return VueRouterReplace.call(this, to).catch(err => err)
}

Vue.use(Router);

export default new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            redirect: '/runner/login'
        },
        {
            path: '/runner/register',
            name: 'Register',
            component: Register,
            meta: {
                title: '注册'
            }
        }, {
            path: '/runner/login',
            name: 'Login',
            component: Login,
            meta: {
                title: '登录'
            }
        }, {

            path: '/runner',
            name: 'Index',
            component: Home,
            meta: {
                title: '项目管理',
                requireAuth: true
            },
            children: [
                {
                    name: 'Dashboard',
                    path: 'dashboard',
                    component: Dashboard,
                    meta: {
                        title: '系统概述',
                        requireAuth: true,
                    }
                },
                {
                    name: 'ProjectList',
                    path: 'project_list',
                    component: ProjectList,
                    meta: {
                        title: '项目概述',
                        requireAuth: true,
                    }
                },
                {
                    name: 'ProjectDetail',
                    path: 'project/:id/dashbord',
                    component: ProjectDetail,
                    meta: {
                        title: '项目详情',
                        requireAuth: true,
                    }

                },
                {
                    name: 'DebugTalk',
                    path: 'debugtalk/:id',
                    component: DebugTalk,
                    meta: {
                        title: '驱动代码',
                        requireAuth: true,
                    }

                },
                {
                    name: 'RecordApi',
                    path: 'api_record/:id',
                    component: RecordApi,
                    meta: {
                        title: 'API 接口',
                        requireAuth: true
                    }

                },
                {
                    name: 'AutoTest',
                    path: 'auto_test/:id',
                    component: AutoTest,
                    meta: {
                        title: 'API 用例',
                        requireAuth: true
                    }

                },
                {
                    name: 'RecordConfig',
                    path: 'record_config/:id',
                    component: RecordConfig,
                    meta: {
                        title: '配置管理',
                        requireAuth: true
                    }

                },
                {
                    name: 'GlobalEnv',
                    path: 'global_env/:id',
                    component: GlobalEnv,
                    meta: {
                        title: '全局变量',
                        requireAuth: true
                    }

                },
                {
                    name: 'Reports',
                    path: 'reports/:id',
                    component: ReportList,
                    meta: {
                        title: '历史报告',
                        requireAuth: true
                    }

                },
                {
                    name: 'Task',
                    path: 'tasks/:id',
                    component: Tasks,
                    meta: {
                        title: '定时任务',
                        requireAuth: true
                    }

                },
                {
                    name: 'HostIP',
                    path: 'host_ip/:id',
                    component: HostAddress,
                    meta: {
                        title: 'HOST配置',
                        requireAuth: true
                    }

                },
                {
                    name: 'MOCK',
                    path: 'mock/:id',
                    component: RecordMock,
                    meta: {
                        title: 'MOCK接口',
                        requireAuth: true
                    }

                }
            ]
        },

    ]
})

