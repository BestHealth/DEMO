<template>

    <el-menu
        class="common-side-bar"
        :default-active="$store.state.routerName"
        background-color="#304056"
        text-color="#BFCBD9"
        active-text-color="#318DF1"
        @select="select"
    >
        <el-menu-item index="Dashboard">
            <i class="el-icon-s-home"></i>
            <span slot="title">系统概述</span>
        </el-menu-item>

        <el-submenu index="ProjectTest">
            <template slot="title">
                <i class="el-icon-menu"></i>
                <span slot="title">项目管理</span>
            </template>
            <el-menu-item index="ProjectList">
                <i class="el-icon-s-operation"></i>
                <span slot="title">项目概述</span>
            </el-menu-item>
            <el-menu-item index="ProjectDetail" :disabled="$store.state.routerName === 'ProjectList' || $store.state.routerName === 'Dashboard'">
                <i class="el-icon-s-order"></i>
                <span slot="title">项目详情</span>
            </el-menu-item>
        </el-submenu>

        <el-submenu index="ApiTest" :disabled="$store.state.routerName === 'ProjectList' || $store.state.routerName === 'Dashboard'">
            <template slot="title">
                <i class="el-icon-s-ticket"></i>
                <span slot="title">接口测试</span>
            </template>

            <el-menu-item-group>
                <el-menu-item v-for="item of side_ApiTest" :index="item.url" :key="item.url">
                    <span :class="item.code"></span>&nbsp;&nbsp;{{ item.name }}
                </el-menu-item>
            </el-menu-item-group>
        </el-submenu>
        <el-menu-item index="Pressure" disabled>
            <i class="el-icon-s-platform"></i>
            <span slot="title">UI 测试</span>
        </el-menu-item>
        <el-submenu index="MOCK" :disabled="$store.state.routerName === 'ProjectList' || $store.state.routerName === 'Dashboard'">
            <template slot="title">
                <i class="el-icon-s-opportunity"></i>
                <span slot="title">MOCK接口</span>
            </template>
            <el-menu-item-group>
                <el-menu-item v-for="item of MOCK" :index="item.url" :key="item.url">
                    <span :class="item.code"></span>&nbsp;&nbsp;{{ item.name }}
                </el-menu-item>
            </el-menu-item-group>
        </el-submenu>

        <el-menu-item index="Register" disabled>
            <i class="el-icon-user-solid"></i>
            <span slot="title">权限管理</span>
        </el-menu-item>


    </el-menu>
</template>

<script>
export default {
    name: "Side",
    data() {
        return {
            side_ApiTest: [
                {name: "API 接口", url: "RecordApi", code: "el-icon-s-ticket"},
                {name: "API 用例", url: "AutoTest", code: "el-icon-s-finance"},
                {name: "配置管理", url: "RecordConfig", code: "el-icon-s-tools"},
                {name: "全局变量", url: "GlobalEnv", code: "el-icon-share"},
                {name: "域名管理", url: "HostIP", code: "el-icon-s-opportunity"},
                {name: "驱动代码", url: "DebugTalk", code: "el-icon-s-help"},
                {name: "定时任务", url: "Task", code: "el-icon-s-promotion"},
                {name: "历史报告", url: "Reports", code: "el-icon-s-data"}
            ],
            MOCK: [
                {name: "模拟接口", url: "MOCK", code: "el-icon-coordinate"}
            ],
        }
    },
    methods: {
        select(url) {
            this.$store.commit('setRouterName', url);
            this.$router.push({name: url});
            this.setLocalValue("routerName", url);
        }
    }
}
</script>

<style scoped>

.common-side-bar {
    position: fixed;
    top: 48px;
    border-right: 1px solid #ddd;
    height: 100%;
    width: 202px;
    background-color: #fff;
    display: inline-block;
}
</style>
