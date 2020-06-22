<template>
  <div>
    <div class="container">
      <el-row :gutter="30">
        <el-col :span="6">
          <div><el-input placeholder="输入用例名称、分组名称进行过滤" v-model="filterText" size="small" style="width:90%"></el-input></div>
          <div class="tree">
            <el-tree v-loading="treeLoading" :data="treeData" ref="tree" :props="treeProps" accordion highlight-current @node-click="handleNodeClick" :filter-node-method="filterNode"></el-tree>
          </div>
        </el-col>
        <el-col :span="18">
          <div class="postman">
            <el-input placeholder="请输入URL" v-model="testCase.url">
              <el-select v-model="testCase.method" slot="prepend" placeholder="请选择">
                <el-option
                  v-for="(val,key) in type.method"
                  :key="key"
                  :label="val"
                  :value="key">
                </el-option>
              </el-select>
              <el-button slot="append" icon="el-icon-s-promotion" @click="debug" :loading='loading'>{{ loading ? 'sending...' : 'send  ' }}</el-button>
            </el-input>
            <el-tabs v-model="activeRequestModel" type="border-card" style="margin-top:15px" @tab-click="updateReqCodemirror">
              <el-tab-pane label="请求头" name="requestHeader">
                <codemirror  ref="myCmRequestHeader" v-model="testCase.header"  :options="cmOptions"></codemirror>
              </el-tab-pane>
              <el-tab-pane label="请求体" name="requestBody">
                <codemirror  ref="myCmRequestBody" v-model="testCase.data"  :options="cmOptions"></codemirror>
              </el-tab-pane>
              <el-tab-pane label="提交方式" name="submit">
                <div style="height: 300px">
                  <el-radio-group v-model="testCase.submit">
                    <label v-for="(val,key) in type.submit" :key="key" class="el-radio">
                      <el-radio :label="key">{{val}}</el-radio>
                    </label>
                  </el-radio-group>
                </div>
              </el-tab-pane>
            </el-tabs>
            <el-tabs v-model="activeResponseModel" type="border-card" style="margin-top:15px" @tab-click="updateRepCodemirror">
              <div style="position:absolute;top:28px;right:33px;z-index:99999999 " v-show="reponse.statusCode">
                <el-tag v-if="this.reponse.statusCode>=400"  type="danger">{{reponse.statusCode}}</el-tag>
                <el-tag v-else type="success">{{reponse.statusCode}}</el-tag>
              </div>
              <el-tab-pane label="响应头" name="reposnseHeader">
                <codemirror  ref="myCmReposnseHeader" v-model="reponse.headers"  :options="cmOptions"></codemirror>
              </el-tab-pane>
              <el-tab-pane label="响应体" name="reposnseBody">
                <codemirror  ref="myCmReposnseBody" v-model="reponse.body"  :options="cmOptions"></codemirror>
              </el-tab-pane>
            </el-tabs>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import { codemirror } from 'vue-codemirror'
import { get, post } from '@/lin/plugins/axios'
/* eslint-disable*/
import 'codemirror/mode/javascript/javascript.js'
import 'codemirror/theme/erlang-dark.css'


export default {
  components: {
    codemirror
  },
  data() {
    return {
      activeRequestModel: 'requestBody',
      activeResponseModel: 'reposnseBody',
      filterText: '',
      treeLoading: false,
      loading: false,
      cid: null,
      testCase: {
        url: null,
        submit: '1',
        method: null,
        header: null,
        data: '',
      },
      reponse: {
        headers: null,
        body: null,
        statusCode: 0,
        totalSeconds: 0,
      },
      type: {
        method: {},
        submit: {},
        deal: {},
        assert: {}
      },
      treeData: [],
      treeProps: {
        children: 'cases',
        label: 'name',
      },
      cmOptions: {
        tabSize: 2,
        mode: 'text/javascript',
        theme: 'erlang-dark',
        lineNumbers: true,
        line: true,
        matchBrackets: true,
        autoRefresh: true
      }
    }
  },
  activated() {
  },
  async created() {
    await this.getType()
    await this.groupByCaseGroup()
  },
  methods: {
    filterNode(value, data) {
      if (!value) return true
      return data.name.indexOf(value) !== -1
    },
    async getType() {
      const type = await get('/v1/case/type', { showBackend: true })
      this.type.method = type.METHOD
      this.type.submit = type.SUBMIT
      this.type.deal = type.DEAL
      this.type.assert = type.ASSERT
      this.testCase.method = '1'
    },
    async debug() {
      try {
        this.loading = true
        const result = await post('/v1/case/debug', {
          url: this.testCase.url,
          method: parseInt(this.testCase.method, 10),
          submit: parseInt(this.testCase.submit, 10),
          data: this.testCase.data,
          header: this.testCase.header,
        }, { showBackend: true })
        this.reponse.statusCode = result.statusCode
        if (result.body.constructor === String) {
          this.reponse.body = result.body
        } else {
          this.reponse.body = JSON.stringify(result.body, null, '\t')
        }
        if (result.body.headers === String) {
          this.reponse.headers = result.headers
        } else {
          this.reponse.headers = JSON.stringify(result.headers, null, '\t')
        }
        this.reponse.totalSeconds = result.totalSeconds
        this.loading = false
      } catch (error) {
        this.loading = false
      }
    },
    updateReqCodemirror() {
      setTimeout(() => {
        this.$refs.myCmRequestHeader.codemirror.refresh()
        this.$refs.myCmRequestBody.codemirror.refresh()
      },5)
    },
    updateRepCodemirror() {
      setTimeout(() => {
        this.$refs.myCmReposnseHeader.codemirror.refresh()
        this.$refs.myCmReposnseBody.codemirror.refresh()
      },5)
    },
    async getCase() {
      const data = await get('/v1/case', { id: this.cid }, { showBackend: true })
      this.testCase.method = data.data[0].method.toString()
      this.testCase.submit = data.data[0].submit.toString()
      if (data.data[0].data !== null) {
        this.testCase.data = data.data[0].data
      } else {
        this.testCase.data = ''
      }
      if (data.data[0].header !== null) {
        this.testCase.header = data.data[0].header
      } else {
        this.testCase.header = ''
      }   
      this.testCase.url = data.data[0].url
    },
    async groupByCaseGroup() {
      this.treeLoading = true
      try {
        this.treeData = await get('/v1/case/groupByCaseGroup', { showBackend: true })
        this.treeLoading = false
      } catch (e) {
        this.loading = false
        this.treeLoading = false
      }
    },
    handleNodeClick(obj) {
      if (obj.cases === undefined) {
        this.reponse.body = ''
        this.reponse.headers = ''
        this.reponse.statusCode = 0
        this.reponse.totalSeconds = 0
        this.cid = obj.id
        this.getCase()
      }
    },
  },
  watch: {
    filterText(val) {
      this.$refs.tree.filter(val)
    },
  },
}
</script>

<style lang="scss" scoped>
.container {
  padding: 30px;

  .postman {
    width: 95%;

    .el-select {
      width: 130px;
    }
  }

  .tree {
    height: 75vh;
    width: 100%;
    margin-top:30px;
    overflow-y: auto;
  }

  .tree::-webkit-scrollbar{
    width:8px;
    height:8px;
    /**/
  }
  .tree::-webkit-scrollbar-track{
    background: rgb(239, 239, 239);
    border-radius:2px;
  }
  .tree::-webkit-scrollbar-thumb{
    background: #dad4d4;
    border-radius:10px;
  }
  .tree::-webkit-scrollbar-thumb:hover{
    background: rgb(175, 173, 173);
  }

}
</style>
