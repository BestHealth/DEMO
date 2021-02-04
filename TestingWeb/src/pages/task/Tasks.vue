<template>

    <el-container>
        <el-header style="background: #fff; padding: 0; height: 50px">
            <div class="nav-api-header">
                <div style="padding-top: 10px; margin-left: 30px">
                    <el-button
                        type="primary"
                        size="small"
                        icon="el-icon-circle-plus-outline"
                        @click="handleAddTask"
                    >添加任务
                    </el-button>

                    <el-button
                        v-show="tasksData.count !== 0 "
                        style="margin-left: 20px"
                        type="danger"
                        icon="el-icon-delete"
                        size="mini"
                        @click="delSelectionTask"
                    >批量删除
                    </el-button>

                    <el-button
                        :disabled="!addTasks"
                        type="text"
                        style="position: absolute; right: 30px;"
                        @click="addTasks=false"
                    >返回列表
                    </el-button>

                </div>
            </div>
        </el-header>

        <el-container>
            <el-header v-if="!addTasks" style="padding: 0; height: 50px">
                <div style="padding-top: 20px; padding-left: 30px; overflow: hidden">
                    <el-row :gutter="20">
                        <el-col :span="6">
                            <!-- v-if="reportData.count > 11"-->
                            <el-input placeholder="请输入任务名称" clearable v-model="search"
                                      size="small">
                                <el-button slot="append" icon="el-icon-search" @click="getTaskList"></el-button>
                            </el-input>

                        </el-col>
                        <el-col :span="7">
                            <el-pagination
                                :page-size="11"
                                v-show="tasksData.count !== 0 "
                                background
                                @current-change="handleCurrentChange"
                                :current-page.sync="currentPage"
                                layout="total, prev, pager, next, jumper"
                                :total="tasksData.count"
                            >
                            </el-pagination>
                        </el-col>
                    </el-row>
                </div>
            </el-header>
            <el-main style="padding: 0; margin-left: 10px; margin-top: 10px;">
                <div style="position: fixed; bottom: 0; right:0; left: 220px; top: 170px">
                    <el-table
                        v-if="!addTasks"
                        :data="tasksData.results"
                        :show-header="tasksData.results.length !== 0 "
                        stripe
                        highlight-current-row
                        height="calc(100%)"
                        @cell-mouse-enter="cellMouseEnter"
                        @cell-mouse-leave="cellMouseLeave"
                        @selection-change="selectionTask"
                    >
                        <el-table-column
                            type="selection"
                            width="55"
                        >
                        </el-table-column>


                        <el-table-column
                            label="任务名称"
                            width="200"
                        >
                            <template slot-scope="scope">
                                <div>{{ scope.row.name }}</div>
                            </template>
                        </el-table-column>


                        <el-table-column
                            width="120"
                            label="时间配置"
                        >
                            <template slot-scope="scope">
                                <div>{{ scope.row.kwargs.corntab }}</div>
                            </template>
                        </el-table-column>

                        <el-table-column
                            width="100"
                            label="信息策略"
                        >
                            <template slot-scope="scope">
                                <div>{{ scope.row.kwargs.strategy }}</div>

                            </template>
                        </el-table-column>


                        <el-table-column
                            width="80"
                            label="状态"
                        >
                            <template slot-scope="scope">
                                <el-switch
                                    v-model="scope.row.enabled"
                                    active-color="#13ce66"
                                    inactive-color="#ff4949"
                                    @change="handleSwitchChange(scope.row.id, scope.row.enabled)">
                                </el-switch>
                            </template>
                        </el-table-column>
                        <el-table-column
                            width="250"
                            label="接收人"
                        >
                            <template slot-scope="scope">
                                <div>{{ scope.row.kwargs.receiver }}</div>
                            </template>
                        </el-table-column>
                        <el-table-column
                            width="250"
                            label="抄送人"
                        >
                            <template slot-scope="scope">
                                <div>{{ scope.row.kwargs.copy }}</div>
                            </template>
                        </el-table-column>

                        <el-table-column
                            width="400"
                            label="WEBHOOK"
                        >
                            <template slot-scope="scope">
                                <div>{{ scope.row.kwargs.webhook }}</div>
                            </template>
                        </el-table-column>

                        <el-table-column
                            width="200"
                        >
                            <template slot-scope="scope">
                                <el-row v-show="currentRow === scope.row">
                                    <el-button
                                        type="info"
                                        icon="el-icon-edit"
                                        title="编辑定时任务"
                                        circle size="mini"
                                        @click="handleEditSchedule(scope.row.id, scope.row)"
                                    ></el-button>
                                    <el-button
                                        type="primary"
                                        icon="el-icon-s-opportunity"
                                        title="手动触发定时任务"
                                        circle size="mini"
                                        @click="runTask(scope.row.id)"
                                    >
                                    </el-button>
                                    <el-button
                                        type="danger"
                                        title="删除定时任务"
                                        icon="el-icon-delete"
                                        circle size="mini"
                                        @click="delTasks(scope.row.id)"
                                    >
                                    </el-button>
                                </el-row>
                            </template>

                        </el-table-column>

                    </el-table>
                </div>
            </el-main>
            <add-tasks
                v-if="addTasks"
                v-on:changeStatus="changeStatus"
                :ruleForm="ruleForm"
                :args = "args"
                :scheduleId="scheduleId"
            >
            </add-tasks>
        </el-container>
    </el-container>

</template>

<script>
import AddTasks from './AddTasks'

export default {
    components: {
        AddTasks
    },
    data() {
        return {
            search:'',
            addTasks: false,
            currentPage: 1,
            currentRow: '',
            tasksData: {
                count: 0,
                results: []
            },
            ruleForm: {
                name: '',
                switch: true,
                corntab: '',
                strategy: '始终发送',
                receiver: '',
                copy: '',
                webhook:''
            },
        }
    },

    methods: {
        handleAddTask(){
            this.addTasks = true;
            this.scheduleId = '';
            this.ruleForm = {
                name: '',
                switch: true,
                corntab: '',
                strategy: '始终发送',
                receiver: '',
                copy: '',
                webhook:''
            };
            this.args = [];
        },
        delTasks(id) {
            this.$confirm('此操作将永久删除该定时任务，是否继续?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning',
            }).then(() => {
                this.$api.deleteTasks(id).then(resp => {
                    if (resp.success) {
                        this.getTaskList();
                    }
                })
            })
        },
        handleCurrentChange(val) {
            this.$api.getTaskPaginationBypage({
                params: {
                    page: this.currentPage,
                    project: this.$route.params.id,
                    search: this.search
                }
            }).then(resp => {
                this.tasksData = resp;
            })
        },

        runTask(id) {
            this.$api.runTask(id).then(resp => {
                if (resp.success) {
                    this.$message.info({
                        title: '提示',
                        message: resp.msg,
                        duration: 2000,
                        center: true
                    })
                } else {
                    this.$message.error({
                        message: resp.msg,
                        duration: 2000,
                        center: true
                    })
                }
            })
        },
        handleEditSchedule(id, index_data){
            // debugger;
            // 激活addTasks组件
            this.addTasks = true;
            this.scheduleId = id;
            this.ruleForm["corntab"] = index_data.kwargs.corntab;
            this.ruleForm["strategy"] = index_data.kwargs.strategy;
            this.ruleForm["receiver"] = index_data.kwargs.receiver;
            this.ruleForm["copy"] = index_data.kwargs.copy;
            this.ruleForm["name"] = index_data.name;
            this.ruleForm["switch"] = index_data.enabled;
            this.ruleForm["webhook"] = index_data.kwargs.webhook;
            this.args = index_data.args;
        },

        changeStatus(value) {
            this.getTaskList();
            this.addTasks = value;
            this.args = [];
            this.ruleForm = {
                name: '',
                switch: true,
                corntab: '',
                strategy: '始终发送',
                receiver: '',
                copy: '',
                webhook:''
            }
        },
        getTaskList() {
            this.$api.taskList({params: {
                project: this.$route.params.id,
                search: this.search
            }}).then(resp => {
                this.tasksData = resp
            })
        },
        cellMouseEnter(row) {
            this.currentRow = row;
        },

        cellMouseLeave(row) {
            this.currentRow = '';
        },

        selectionTask(val) {
            this.tasksData = val;
        },

        delSelectionTask() {
            if (this.tasksData.length !== 0) {
                this.$confirm('此操作将永久删除勾选的定时任务，是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning',
                }).then(() => {
                    this.$api.delAllTasks({data: this.tasksData}).then(resp => {
                        this.getTaskList();
                    })

                })
            } else {
                this.$notify.warning({
                    title: '提示',
                    message: '请至少勾选一个全局变量',
                    duration: 1000
                })
            }
        },
        handleSwitchChange(id, val) {
            this.$api.patchTask(id,{'switch': val}).then( resp => {
                if(resp.success) {
                    this.$notify.success('更新定时任务成功！');
                }else{
                    this.$notify.success('更新定时任务失败！');
                }
                this.getTaskList()
            })
        },
    },
    name: "Tasks",
    mounted() {
        this.getTaskList();
    }
}
</script>

<style>


</style>
