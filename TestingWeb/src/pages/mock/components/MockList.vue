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
                        :show-header="apiData.results.length !== 0 "
                        stripe
                        @cell-mouse-enter="cellMouseEnter"
                        @cell-mouse-leave="cellMouseLeave"
                        style="width: 100%;"
                        @selection-change="handleSelectionChange"
                        v-loading="loading"
                    >
                        <el-table-column
                            type="selection"
                            width="50"
                        >
                        </el-table-column>

                        <el-table-column
                            prop="name"
                            label="接口名称"
                            width="130"
                            :show-overflow-tooltip="true"
                        >
                        </el-table-column>

                        <el-table-column
                            prop="tag"
                            label="请求类型"
                            width="100"
                            filter-placement="bottom-end">
                            <template slot-scope="scope">
                                <el-tag
                                    type="success"
                                    disable-transitions>{{ scope.row.method.toUpperCase() }}
                                </el-tag>
                            </template>
                        </el-table-column>

                        <el-table-column
                            width="80"
                            label="接口状态"
                        >
                            <template slot-scope="scope">
                                <el-switch
                                    v-model="scope.row.status"
                                    active-color="#13ce66"
                                    inactive-color="#ff4949"
                                    @change="handleSwitchChange(scope.row.id, scope.row.status, scope.row.url)">
                                </el-switch>
                            </template>
                        </el-table-column>

                        <el-table-column
                            prop="url"
                            label="接口路径"
                            width="300"
                            :show-overflow-tooltip="true"
                        >
                        </el-table-column>


                        <el-table-column
                            prop="description"
                            label="接口描述"
                            width="250"
                            :show-overflow-tooltip="true"
                        >
                        </el-table-column>
                        <el-table-column
                            prop="create_time"
                            label="创建时间"
                            width="180"
                            :show-overflow-tooltip="true"
                        >
                        </el-table-column>


                        <el-table-column
                            label="操作"
                        >
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
                                        type="primary"
                                        icon="el-icon-caret-right"
                                        title="测试 API"
                                        circle size="mini"
                                        @click="handleRunAPI(scope.row.id)"
                                    ></el-button>
                                    <el-popover
                                        style="margin-left: 10px"
                                        trigger="hover"
                                    >
                                        <div style="text-align: center">

                                            <el-button
                                                type="success"
                                                icon="el-icon-document"
                                                title="复制 API"
                                                circle size="mini"
                                                @click="handleCopyAPI(scope.row.id)"
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
import Report from '../../reports/DebugReport'
import {baseUrl} from "../../../restful/api";

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
            },
            base_url: baseUrl
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
                    this.$api.delAllMockAPI({data: this.selectAPI}).then(resp => {
                        this.$message.success(resp.msg);
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

        handleCopyAPI(id) {
            this.$prompt('请输入接口名称', '提示', {
                confirmButtonText: '确定',
                inputPattern: /^[\s\S]*.*[^\s][\s\S]*$/,
                inputErrorMessage: '接口名称不能为空'
            }).then(({value}) => {
                this.$api.copyMockAPI(id, {
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

        // 测试API
        handleRunAPI(id) {
            this.loading = true;
            this.$api.runMockAPIByPk(id, {
                params: {
                    base_url: this.base_url,
                }
            }).then(resp => {
                this.summary = resp;
                this.dialogTableVisible = true;
                this.loading = false;
            }).catch(resp => {
                this.loading = false;
            })
        },

        filterNode(value, data) {
            if (!value) return true;
            return data.label.indexOf(value) !== -1;
        },

        getTree(showType) {
            this.$api.getTree(this.$route.params.id, {params: {type: 3}}).then(resp => {
                this.dataTree = resp.tree;
                // run是批量运行api弹窗，其他是批量更新api relation弹窗
                if (showType === 'run') {
                    this.dialogTreeVisible = true;
                } else {
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
            } else if (length !== 1) {
                this.$notify.error({
                    title: '提示',
                    message: 'API只能移动到一个节点, 现在选了' + length + '个节点',
                    duration: 1500
                });
            } else {
                this.$api.moveMockAPI({
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
            if (this.selectAPI.length > 0) {
                this.$emit('update:isSelectAPI', true);
            } else {
                this.$emit('update:isSelectAPI', false);
            }

        },

        handleSwitchChange(id, val, url) {
            this.$api.patchMockApi(id, {'status': val, 'url': url}).then(resp => {
                if (resp.success) {
                    this.$notify.success('更新接口状态成功！');
                } else {
                    this.$notify.error(resp.msg);
                }
                this.getAPIList()
            })
        },

        toggleAll() {
            this.$refs.multipleTable.toggleAllSelection();
        },

        toggleClear() {
            this.$refs.multipleTable.clearSelection();
        },
        // 查询api列表
        getAPIList() {
            this.$api.mockApiList({
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
            this.$api.getMockPaginationBypage({
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
                this.$api.delMockAPI(index).then(resp => {
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
            this.$api.getMockAPISingle(row.id).then(resp => {
                if (resp.success) {
                    this.$emit('api', resp);
                } else {
                    this.$message.error(resp.msg)
                }
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
