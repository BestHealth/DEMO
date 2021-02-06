<template>
    <el-container>
        <el-header style="padding: 0; height: 50px;">
            <div style=" padding-left: 10px;">
                <el-row :gutter="50">
                    <el-col :span="1">
                        <el-checkbox
                            v-if="apiData.count > 0"
                            v-model="checked"
                            style="padding-top: 14px; padding-left: 2px"
                        >
                        </el-checkbox>
                    </el-col>
                    <!-- v-if="reportData.count > 11"-->
                    <el-col :span="6">
                        <el-input placeholder="请输入接口名称" clearable v-model="search">
                            <el-button slot="append" icon="el-icon-search" @click="getAPIList"></el-button>
                        </el-input>
                    </el-col>

                    <el-col :span="7">
                        <el-pagination
                            style="margin-top: 5px"
                            :page-size="11"
                            v-show="apiData.count !== 0 "
                            background
                            @current-change="handleCurrentChange"
                            :current-page.sync="currentPage"
                            layout="total, prev, pager, next, jumper"
                            :total="apiData.count"
                        >
                        </el-pagination>
                    </el-col>

                </el-row>
            </div>
        </el-header>

        <el-container>
            <el-main style="padding: 0; margin-left: 10px;">
                <el-dialog
                    v-if="dialogTableVisible"
                    :visible.sync="dialogTableVisible"
                    width="70%"
                >
                    <report :summary="summary"></report>
                </el-dialog>

                <el-dialog
                    title="Run API"
                    :visible.sync="dialogTreeVisible"
                    width="45%"
                >
                    <div>
                        <div>
                            <el-row :gutter="2">
                                <el-col :span="8">
                                    <el-switch
                                        style="margin-top: 10px"
                                        v-model="asyncs"
                                        active-color="#13ce66"
                                        inactive-color="#ff4949"
                                        active-text="异步执行"
                                        inactive-text="同步执行">
                                    </el-switch>
                                </el-col>
                                <el-col :span="10">
                                    <el-input
                                        v-show="asyncs"
                                        clearable
                                        placeholder="请输入报告名称"
                                        v-model="reportName"
                                        :disabled="false">
                                    </el-input>

                                </el-col>
                            </el-row>
                        </div>
                        <div style="margin-top: 20px">
                            <el-input
                                placeholder="输入节点名称进行过滤"
                                v-model="filterText"
                                size="medium"
                                clearable
                                prefix-icon="el-icon-search"
                            >
                            </el-input>

                            <el-tree
                                :filter-node-method="filterNode"
                                :data="dataTree"
                                show-checkbox
                                node-key="id"
                                :expand-on-click-node="false"
                                check-on-click-node
                                :check-strictly="true"
                                :highlight-current="true"
                                ref="tree"
                            >
                            <span class="custom-tree-node"
                                  slot-scope="{ node, data }"
                            >
                                <span><i class="iconfont" v-html="expand"></i>&nbsp;&nbsp;{{ node.label }}</span>
                            </span>
                            </el-tree>
                        </div>

                    </div>
                    <span slot="footer" class="dialog-footer">
                    <el-button @click="dialogTreeVisible = false">取 消</el-button>
                    <el-button type="primary" @click="runTree">确 定</el-button>
                  </span>
                </el-dialog>

                <el-dialog
                    title="Move API"
                    :visible.sync="dialogTreeMoveAPIVisible"
                    width="45%"
                >
                    <div>
                        <div style="margin-top: 20px">
                            <el-input
                                placeholder="输入关键字进行过滤"
                                v-model="filterText"
                                size="medium"
                                clearable
                                prefix-icon="el-icon-search"
                            >
                            </el-input>

                            <el-tree
                                :filter-node-method="filterNode"
                                :data="dataTree"
                                show-checkbox
                                node-key="id"
                                :expand-on-click-node="false"
                                check-on-click-node
                                :check-strictly="true"
                                :highlight-current="true"
                                ref="tree"
                            >
                            <span class="custom-tree-node"
                                  slot-scope="{ node, data }"
                            >
                                <span><i class="iconfont" v-html="expand"></i>&nbsp;&nbsp;{{ node.label }}</span>
                            </span>
                            </el-tree>
                        </div>

                    </div>
                    <span slot="footer" class="dialog-footer">
                    <el-button @click="dialogTreeMoveAPIVisible = false">取 消</el-button>
                    <el-button type="primary" @click="moveAPI">确 定</el-button>
                  </span>
                </el-dialog>


                <div style="position: fixed; bottom: 0; right:0; left: 500px; top: 160px">
                    <el-table
                        highlight-current-row
                        height="calc(100%)"
                        ref="multipleTable"
                        :data="apiData.results"
                        :show-header="false"
                        :cell-style="{paddingTop: '4px', paddingBottom: '4px'}"
                        @cell-mouse-enter="cellMouseEnter"
                        @cell-mouse-leave="cellMouseLeave"
                        style="width: 100%;"
                        @selection-change="handleSelectionChange"
                        v-loading="loading"
                    >
                        <el-table-column
                            type="selection"
                            width="40"
                        >
                        </el-table-column>

                        <el-table-column
                            min-width="450"
                            align="center"
                        >
                            <template slot-scope="scope">
                                <div class="block block_post" v-if="scope.row.method.toUpperCase() === 'POST' ">
                                    <span class="block-method block_method_post block_method_color">POST</span>
                                    <span class="block-method block_url">{{ scope.row.url | ellipsis }}</span>
                                    <span class="block-summary-description">{{ scope.row.name | str_ellipsis }}</span>
                                </div>

                                <div class="block block_get" v-if="scope.row.method.toUpperCase() === 'GET' ">
                                    <span class="block-method block_method_get block_method_color">GET</span>
                                    <span class="block-method block_url">{{ scope.row.url | ellipsis }}</span>
                                    <span class="block-summary-description">{{ scope.row.name | str_ellipsis }}</span>
                                </div>

                                <div class="block block_put" v-if="scope.row.method.toUpperCase() === 'PUT' ">
                                    <span class="block-method block_method_put block_method_color">PUT</span>
                                    <span class="block-method block_url">{{ scope.row.url | ellipsis }}</span>
                                    <span class="block-summary-description">{{ scope.row.name | str_ellipsis }}</span>
                                </div>

                                <div class="block block_delete" v-if="scope.row.method.toUpperCase() === 'DELETE' ">
                                    <span class="block-method block_method_delete block_method_color">DELETE</span>
                                    <span class="block-method block_url">{{ scope.row.url | ellipsis }}</span>
                                    <span class="block-summary-description">{{ scope.row.name | str_ellipsis }}</span>
                                </div>

                                <div class="block block_patch" v-if="scope.row.method.toUpperCase() === 'PATCH' ">
                                    <span class="block-method block_method_patch block_method_color">PATCH</span>
                                    <span class="block-method block_url">{{ scope.row.url | ellipsis }}</span>
                                    <span class="block-summary-description">{{ scope.row.name | str_ellipsis }}</span>
                                </div>

                                <div class="block block_head" v-if="scope.row.method.toUpperCase() === 'HEAD' ">
                                    <span class="block-method block_method_head block_method_color">HEAD</span>
                                    <span class="block-method block_url">{{ scope.row.url | ellipsis }}</span>
                                    <span class="block-summary-description">{{ scope.row.name | str_ellipsis }}</span>
                                </div>

                                <div class="block block_options" v-if="scope.row.method.toUpperCase()=== 'OPTIONS' ">
                                    <span class="block-method block_method_options block_method_color">OPTIONS</span>
                                    <span class="block-method block_url">{{ scope.row.url | ellipsis }}</span>
                                    <span class="block-summary-description">{{ scope.row.name | str_ellipsis }}</span>
                                </div>

                            </template>
                        </el-table-column>

                        <el-table-column>
                            <template slot-scope="scope">
                                <el-row v-show="currentRow === scope.row">
                                    <el-button
                                        type="info"
                                        icon="el-icon-edit"
                                        title="修改 API"
                                        circle size="mini"
                                        @click="handleRowClick(scope.row)"
                                    ></el-button>

                                    <el-button
                                        type="success"
                                        icon="el-icon-document"
                                        title="复制 API"
                                        circle size="mini"
                                        @click="handleCopyAPI(scope.row.id)"
                                    >
                                    </el-button>

                                    <el-popover
                                        style="margin-left: 10px"
                                        trigger="hover"
                                    >
                                        <div style="text-align: center">

                                            <el-button
                                                type="primary"
                                                icon="el-icon-caret-right"
                                                title="运行 API"
                                                circle size="mini"
                                                @click="handleRunAPI(scope.row.id)"
                                            ></el-button>

                                            <el-button
                                                v-show="scope.row.cases.length>0"
                                                type="warning"
                                                icon="el-icon-refresh"
                                                title="同步 API 至用例"
                                                circle size="mini"
                                                @click="handleSyncCaseStep(scope.row.id)"
                                            >
                                            </el-button>

                                            <el-button
                                                type="danger"
                                                icon="el-icon-delete"
                                                title="删除 API"
                                                circle size="mini"
                                                @click="handleDelApi(scope.row.id)"
                                            >
                                            </el-button>
                                        </div>
                                        <el-button icon="el-icon-more" title="更多" circle size="mini"
                                                   slot="reference"></el-button>
                                    </el-popover>
                                </el-row>
                            </template>
                        </el-table-column>

                    </el-table>
                </div>

            </el-main>
        </el-container>
    </el-container>
</template>

<script>
import Report from '../../../reports/DebugReport'

export default {
    filters: {
        ellipsis(value) {
            if (!value) return ''
            if (value.length > 40) {
                return value.slice(0, 40) + '......'
            }
            return value
        },
        str_ellipsis(value) {
            if (!value) return ''
            if (value.length > 10) {
                return value.slice(0, 10) + '......'
            }
            return value
        }
    },
    components: {
        Report
    },
    name: "ApiList",
    props: {
        host: {
            require: true
        },
        config: {
            require: true
        },
        run: Boolean,
        back: Boolean,
        node: {
            require: true
        },
        project: {
            require: true
        },
        del: Boolean,
        move: Boolean,
        onlyMe: Boolean,
        isSelectCase: Boolean
    },
    data() {
        return {
            checked: false,
            search: '',
            reportName: '',
            asyncs: false,
            filterText: '',
            loading: false,
            expand: '&#xe65f;',
            dataTree: {},
            dialogTreeVisible: false,
            dialogTableVisible: false,
            dialogTreeMoveAPIVisible: false,
            summary: {},
            selectAPI: [],
            currentRow: '',
            currentPage: 1,
            apiData: {
                count: 0,
                results: []
            }
        }
    },
    watch: {
        filterText(val) {
            this.$refs.tree.filter(val);
        },

        run() {
            this.asyncs = false;
            this.reportName = "";
            this.getTree('run');
        },

        move() {
            this.asyncs = false;
            this.reportName = "";
            this.getTree('move');
        },
        back() {
            this.getAPIList();
        },
        node() {
            this.search = '';
            this.getAPIList();
        },
        checked() {
            if (this.checked) {
                this.toggleAll();
            } else {
                this.toggleClear();
            }
        },

        del() {
            if (this.selectAPI.length !== 0) {
                this.$confirm('此操作将永久删除API，是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning',
                }).then(() => {
                    this.$api.delAllAPI({data: this.selectAPI}).then(resp => {
                        this.getAPIList();
                    })
                })
            } else {
                this.$notify.warning({
                    title: '提示',
                    message: '请至少选择一个接口',
                    duration: 1000
                })
            }
        }
    },

    methods: {

        // api同步用例步骤
        handleSyncCaseStep(id) {
            this.$confirm('是否确定把当前 API 同步到用例步骤', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning',
            }).then(() => {
                this.$api.syncCaseStep(id).then(resp => {
                    if (resp.success) {
                        this.getAPIList();
                        this.$notify.success({
                            title: '提示',
                            message: '用例步骤同步成功',
                            duration: 1500
                        })
                    } else {
                        this.$message.error(resp.msg);
                    }
                })
            }).catch(e => e)
        },

        handleCopyAPI(id) {
            this.$prompt('请输入接口名称', '提示', {
                confirmButtonText: '确定',
                inputPattern: /^[\s\S]*.*[^\s][\s\S]*$/,
                inputErrorMessage: '接口名称不能为空'
            }).then(({value}) => {
                this.$api.copyAPI(id, {
                    'name': value
                }).then(resp => {
                    if (resp.success) {
                        this.getAPIList();
                    } else {
                        this.$message.error(resp.msg);
                    }
                })
            })
        },
        filterNode(value, data) {
            if (!value) return true;
            return data.label.indexOf(value) !== -1;
        },

        runTree() {
            this.dialogTreeVisible = false;
            const relation = this.$refs.tree.getCheckedKeys();
            if (relation.length === 0) {
                this.$notify.error({
                    title: '提示',
                    message: '请至少选择一个节点',
                    duration: 1500
                });
            } else {
                this.$api.runAPITree({
                    "host": this.host,
                    "project": this.project,
                    "relation": relation,
                    "async": this.asyncs,
                    "name": this.reportName,
                    "config": this.config
                }).then(resp => {
                    if (resp.hasOwnProperty("status")) {
                        this.$message.info({
                            message: resp.msg,
                            duration: 1500
                        });
                    } else {
                        this.summary = resp;
                        this.dialogTableVisible = true;
                    }

                })
            }
        },

        getTree(showType) {
            this.$api.getTree(this.$route.params.id, {params: {type: 1}}).then(resp => {
                this.dataTree = resp.tree;
                // run是批量运行api弹窗，其他是批量更新api relation弹窗
                if (showType === 'run'){
                    this.dialogTreeVisible = true;
                }else {
                    this.dialogTreeMoveAPIVisible = this;
                }
            })
        },

        moveAPI() {
            this.dialogTreeVisible = false;
            const relation = this.$refs.tree.getCheckedKeys();
            let length = relation.length;
            if (length === 0) {
                this.$notify.error({
                    title: '提示',
                    message: '请至少选择一个节点',
                    duration: 1500
                });
            } else if ( length !== 1){
                this.$notify.error({
                    title: '提示',
                    message: 'API只能移动到一个节点, 现在选了' + length + '个节点',
                    duration: 1500
                });
            } else {
                this.$api.moveAPI({
                    "project": this.project,
                    "relation": relation[0],
                    "api": this.selectAPI
                }).then(resp => {
                    if (resp.success) {
                        this.getAPIList();
                        this.$message.success({
                            message: '移动API成功',
                            duration: 1500
                        });
                        this.dialogTreeMoveAPIVisible = false
                        this.resetSearch()
                    } else {
                        this.$message.error({
                            message: resp.msg,
                            duration: 1500
                        })
                    }
                })
            }
        },

        handleSelectionChange(val) {
            this.selectAPI = val;
            // 更新是否已经选择API, 父组件依赖这个属性来判断是否显示Move API按钮
            if (this.selectAPI.length > 0){
                this.$emit('update:isSelectAPI', true);
            }else {
                this.$emit('update:isSelectAPI', false);
            }

        },

        toggleAll() {
            this.$refs.multipleTable.toggleAllSelection();
        },

        toggleClear() {
            this.$refs.multipleTable.clearSelection();
        },
        // 查询api列表
        getAPIList() {
            this.$api.apiList({
                params: {
                    node: this.node,
                    project: this.project,
                    search: this.search
                }
            }).then(res => {
                this.apiData = res;
            })
        },


        handleCurrentChange(val) {
            this.$api.getPaginationBypage({
                params: {
                    page: this.currentPage,
                    node: this.node,
                    project: this.project,
                    search: this.search
                }
            }).then(res => {
                this.apiData = res;
            })
        },

        //删除api
        handleDelApi(index) {
            this.$confirm('此操作将永久删除该API，是否继续?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning',
            }).then(() => {
                this.$api.delAPI(index).then(resp => {
                    if (resp.success) {
                        this.getAPIList();
                    } else {
                        this.$message.error(resp.msg);
                    }
                })
            })
        },

        // 编辑API
        handleRowClick(row) {
            this.$api.getAPISingle(row.id).then(resp => {
                if (resp.success) {
                    this.$emit('api', resp);
                } else {
                    this.$message.error(resp.msg)
                }
            })
        },
        // 运行API
        handleRunAPI(id) {
            this.loading = true;
            this.$api.runAPIByPk(id, {
                params: {
                    host: this.host,
                    config: this.config
                }
            }).then(resp => {
                this.summary = resp;
                this.dialogTableVisible = true;
                this.loading = false;
            }).catch(resp => {
                this.loading = false;
            })
        },

        cellMouseEnter(row) {
            this.currentRow = row;
        },

        cellMouseLeave(row) {
            this.currentRow = '';
        }
    },
    mounted() {
        this.getAPIList();
    }
}
</script>

<style scoped>


</style>
