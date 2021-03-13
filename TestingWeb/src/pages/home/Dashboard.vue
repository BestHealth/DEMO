<template>
    <div>
        <el-row :gutter="20">
            <el-col :span="6">
                <el-card>
                    <span>系统总用户：{{possessData.user_count}}</span>
                </el-card>
            </el-col>
            <el-col :span="6">
                <el-card>
                    <span>当天在线用户数：{{possessData.token_count}}</span>
                </el-card>
            </el-col>
            <el-col :span="6">
                <el-card>
                    <span>当前项目数：{{possessData.project_count}}</span>
                </el-card>
            </el-col>
            <el-col :span="6">
                <el-card>
                    <span>测试报告数：{{possessData.report_count}}</span>
                </el-card>
            </el-col>
        </el-row>
        <el-row :gutter="20">
            <el-col :span="6">
                <el-card>
                    <span>接口用例数：{{possessData.case_count}}</span>
                </el-card>
            </el-col>
            <el-col :span="6">
                <el-card>
                    <span>MOCK接口数：{{possessData.mock_count}}</span>
                </el-card>
            </el-col>
            <el-col :span="6">
                <el-card>
                    <span>UI 用例数：1000</span>
                </el-card>
            </el-col>
            <el-col :span="6">
                <el-card>
                    <span>定时任务数：{{possessData.task_count}}</span>
                </el-card>
            </el-col>
        </el-row>
        <el-row :gutter="20">
            <el-col :span="6">
                <el-card>
                    <div slot="header">
                        <span>近7天新增用户趋势图：{{possessData.user_recently_count}}</span>
                    </div>
                    <div>
                        <div id="userChart" style="font-size: 20px"></div>
                    </div>

                </el-card>
            </el-col>
            <el-col :span="6">
                <el-card>
                    <div slot="header">
                        <span>近7天项目趋势图：{{possessData.project_recently_count}}</span>
                    </div>
                    <div>
                        <div id="projectChart" style="font-size: 20px"></div>
                    </div>
                </el-card>
            </el-col>
            <el-col :span="6">
                <el-card>
                    <div slot="header">
                        <span>近7天接口用例趋势图：{{possessData.case_recently_count}}</span>
                    </div>
                    <div>
                        <div id="caseChart" style="font-size: 20px"></div>
                    </div>
                </el-card>
            </el-col>
            <el-col :span="6">
                <el-card>
                    <div slot="header">
                        <span>近7天MOCK趋势图：{{possessData.mock_recently_count}}</span>
                    </div>
                    <div>
                        <div id="mockChart" style="font-size: 20px"></div>
                    </div>
                </el-card>
            </el-col>
        </el-row>
        <el-row :gutter="20">
            <el-col :span="6">
                <el-card>
                    <div slot="header">
                        <span>近7天UI用例趋势图：11111</span>
                    </div>
                    <div>
                        <div id="uiChart" style="font-size: 20px"></div>
                    </div>
                </el-card>
            </el-col>
            <el-col :span="6">
                <el-card>
                    <div slot="header">
                        <span>近7天测试报告趋势图：{{possessData.report_recently_count}}</span>
                    </div>
                    <div>
                        <div id="reportChart" style="font-size: 20px"></div>
                    </div>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>
<style lang="scss">
.el-row {
    margin-bottom: 20px;

    &:last-child {
        margin-bottom: 0;
    }
}
</style>
<script>
import G2 from "@antv/g2";

export default {
    name: "Dashboard",
    data() {
        return {
            possessData: {},
            data: [{
                "date": "2021-03-06",
                "value": 10
            }, {
                "date": "2021-03-07",
                "value": 20
            }, {
                "date": "2021-03-08",
                "value": 30
            }, {
                "date": "2021-03-09",
                "value": 40
            }, {
                "date": "2021-03-10",
                "value": 50
            }, {
                "date": "2021-03-11",
                "value": 60
            }, {
                "date": "2021-03-12",
                "value": 80
            }],
            userChart: null,
            projectChart: null,
            caseChart: null,
            orderChart: null,
            reportChart: null,
        };
    },
    methods: {
        getDashboardList() {
            this.$api.getDashboard().then(resp => {
                this.possessData = resp;
                this.drawUserChart(resp.user_recently)
                this.drawProjectChart(resp.project_recently)
                this.drawCaseChart(resp.case_recently)
                this.drawMockChart(resp.mock_recently)
                this.drawUIChart()
                this.drawReportChart(resp.report_recently)
            })
        },
        drawUserChart: function (user_recently) {
            this.userChart = new G2.Chart({
                container: "userChart",
                forceFit: true,
                height: 200,
                padding: [40, 0, 0, 0]
            });
            this.userChart.source(user_recently);
            this.userChart.scale({
                date: {
                    type: "time",
                    alias: "日期"
                }
            });
            this.userChart.area().position("date*value");
            this.userChart
                .line()
                .position("date*value")
                .size(2);
            this.userChart.render();
        },
        drawProjectChart: function (project_recently) {
            this.projectChart = new G2.Chart({
                container: "projectChart",
                forceFit: true,
                height: 200,
                padding: [40, 0, 0, 0]
            });
            this.projectChart.source(project_recently);
            this.projectChart.scale({
                date: {
                    type: "time",
                    alias: "日期"
                }
            });
            this.projectChart.area().position("date*value");
            this.projectChart
                .line()
                .position("date*value")
                .size(2);
            this.projectChart.render();
        },
        drawCaseChart: function (case_recently) {
            this.caseChart = new G2.Chart({
                container: "caseChart",
                forceFit: true,
                height: 200,
                padding: [40, 0, 0, 0]
            });
            this.caseChart.source(case_recently);
            this.caseChart.scale({
                date: {
                    type: "time",
                    alias: "日期"
                }
            });
            this.caseChart.area().position("date*value");
            this.caseChart
                .line()
                .position("date*value")
                .size(2);
            this.caseChart.render();
        },
        drawMockChart: function (mock_recently) {
            this.orderChart = new G2.Chart({
                container: "mockChart",
                forceFit: true,
                height: 200,
                padding: [40, 0, 0, 0]
            });
            this.orderChart.source(mock_recently);
            this.orderChart.scale({
                date: {
                    type: "time",
                    alias: "日期"
                }
            });
            this.orderChart.area().position("date*value");
            this.orderChart
                .line()
                .position("date*value")
                .size(2);
            this.orderChart.render();
        },
        drawUIChart: function () {
            this.orderChart = new G2.Chart({
                container: "uiChart",
                forceFit: true,
                height: 200,
                padding: [40, 0, 0, 0]
            });
            this.orderChart.source(this.data);
            this.orderChart.scale({
                date: {
                    type: "time",
                    alias: "日期"
                }
            });
            this.orderChart.area().position("date*value");
            this.orderChart
                .line()
                .position("date*value")
                .size(2);
            this.orderChart.render();
        },
        drawReportChart: function (report_recently) {
            this.reportChart = new G2.Chart({
                container: "reportChart",
                forceFit: true,
                height: 200,
                padding: [40, 0, 0, 0]
            });
            this.reportChart.source(report_recently);
            this.reportChart.scale({
                date: {
                    type: "time",
                    alias: "日期"
                }
            });
            this.reportChart.area().position("date*value");
            this.reportChart
                .line()
                .position("date*value")
                .size(2);
            this.reportChart.render();
        }
    },
    mounted() {
        this.getDashboardList();

    }
};
</script>
