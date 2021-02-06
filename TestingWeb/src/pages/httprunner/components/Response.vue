<template>
    <div>
        <div style="margin-left: 200px;">
            <el-radio-group v-model="dataType">
                <el-radio
                    v-for="item of dataOptions"
                    :label="item.label"
                    :key="item.value"
                >{{item.value}}
                </el-radio>
            </el-radio-group>
        </div>
        <div style="margin-top: 5px">
            <editor v-model="jsonData"
                    @init="editorInit"
                    lang="json"
                    theme="github"
                    width="100%"
                    :height="height"
                    v-show="dataType === 'json' "
            >
            </editor>
            <editor v-model="textData"
                    @init="editorInit"
                    lang="text"
                    theme="github"
                    width="100%"
                    :height="height"
            >
            </editor>
        </div>

    </div>


</template>

<script>
    export default {
        props: {
            save: Boolean,
            request: {
                require: false
            }
        },
        computed:{
            height() {
                return window.screen.height - 464
            }
        },

        name: "Request",
        components: {
            editor: require('vue2-ace-editor'),
        },


        watch: {
            save: function () {
                this.$emit('request', {
                    json: this.parseJson(),
                    text: this.textData,
                }, {
                    json_data: this.jsonData,
                    text_data: this.textData,
                });
            },

            request: function () {
                if (this.request.length !== 0) {
                    this.jsonData = this.request.json_data;
                    this.textData = this.request.text_data;
                }
            }
        },

        methods: {
            editorInit() {
                require('brace/ext/language_tools');
                require('brace/mode/json');
                require('brace/theme/github');
                require('brace/snippets/json');
            },

            parseJson() {
                let json = {};
                if (this.jsonData !== '') {
                    try {
                        json = JSON.parse(this.jsonData);
                    }
                    catch (err) {
                        this.$notify.error({
                            title: 'json错误',
                            message: '不是标准的json数据格式',
                            duration: 2000
                        });
                    }
                }
                return json;
            },
        },

        data() {
            return {
                fileList: [],
                currentIndex: 0,
                currentRow: '',
                jsonData: '',
                textData: '',
                dataOptions: [{
                    label: 'json',
                    value: 'json',
                },{
                    label: 'text',
                    value: 'text',
                }],
                dataType: 'json'
            }
        }
    }
</script>
<style scoped>
.ace_editor {
    position: relative;
    overflow: hidden;
    font: 18px/normal 'Monaco', 'Menlo', 'Ubuntu Mono', 'Consolas', 'source-code-pro', monospace !important;
    direction: ltr;
    text-align: left;
    -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
}

</style>

