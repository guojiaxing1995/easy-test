<template>
  <div>
    <div class="container">
      <el-row :gutter="30">
        <el-col :span="6">
          <el-button type="text" style="width:100%;margin-bottom:20px" icon="iconfont icon-fanhui" v-if="isAdd" @click="handleCancelAdd">取消</el-button>
          <el-button type="text" style="width:100%;margin-bottom:20px" icon="el-icon-circle-plus" @click="handleAdd" v-else >新增</el-button>
          <div style="padding: 0 5px"><el-input placeholder="输入请求地址进行过滤" v-model="filterText" size="small" clearable></el-input></div>
          <div class="tree">
            <transition-group type="transition" :name="'flip-list'" class="list-group" tag="ul" v-loading="treeLoading" element-loading-background="rgba(236, 245, 255, 0.5">
              <li class="list-group-item item-color-normal" v-for="element in mockDatas" :key="element.mid"
                v-bind:class="{
                  'item-color-get': !element.is_choose && type.method[element.method] === 'GET', 'item-color-get-choose': element.is_choose && type.method[element.method] === 'GET',
                  'item-color-post': !element.is_choose && type.method[element.method] === 'POST', 'item-color-post-choose': element.is_choose && type.method[element.method] === 'POST',
                  'item-color-put': !element.is_choose && type.method[element.method] === 'PUT', 'item-color-put-choose': element.is_choose && type.method[element.method] === 'PUT',
                  'item-color-delete': !element.is_choose && type.method[element.method] === 'DELETE', 'item-color-delete-choose': element.is_choose && type.method[element.method] === 'DELETE',
                  }"
                @click="handleChoose(element)">
                <span class="name">{{element.url}}</span>
                <!-- 调试 -->
                <i class="el-icon-close" @click.stop="handleDelete(element)"></i>
                <i class="el-icon-edit" @click.stop="handleEdit(element)"></i>
                <i class="el-icon-s-promotion" @click.stop="handleDebug(element)"></i>
              </li>
            </transition-group>
          </div>
        </el-col>
        <el-col :span="18">
          <div class="mock" v-if="isAdd">
            <el-input placeholder="请输入URL" v-model="mockNew.url">
              <el-select v-model="mockNew.method" slot="prepend" placeholder="请选择">
                <el-option
                  v-for="(val,key) in type.method"
                  :key="key"
                  :label="val"
                  :value="key">
                </el-option>
              </el-select>
              <div slot="append"><el-button :loading='loading' icon="el-icon-check" @click="addMock()">保存</el-button></div>
            </el-input>
            <el-tabs v-model="activeRequestModel" type="border-card" style="margin-top:15px">
              <el-tab-pane label="请求头" name="requestHeader">
                <codemirror  ref="addRequestHeader" v-model="mockNew.requestHeader"  :options="addOptions"></codemirror>
              </el-tab-pane>
              <el-tab-pane label="请求体" name="requestBody">
                <codemirror  ref="addRequestBody" v-model="mockNew.requestBody"  :options="addOptions"></codemirror>
              </el-tab-pane>
              <el-tab-pane label="描述" name="msg">
                <div style="height: 300px">
                  <el-input type="textarea" :rows="14" placeholder="请输入描述" v-model="mockNew.msg"></el-input>
                </div>
              </el-tab-pane>
            </el-tabs>
            <el-tabs v-model="activeResponseModel" type="border-card" style="margin-top:15px">
              <el-tab-pane label="响应头" name="reposnseHeader">
                <codemirror  ref="addReposnseHeader" v-model="mockNew.responseHeader"  :options="addOptions"></codemirror>
              </el-tab-pane>
              <el-tab-pane label="响应体" name="reposnseBody">
                <codemirror  ref="addReposnseBody" v-model="mockNew.responseBody"  :options="addOptions"></codemirror>
              </el-tab-pane>
              <el-tab-pane label="HTTP状态码" name="statusCode">
                <div style="height: 300px">
                  <el-input placeholder="请输入HTTP状态码" v-model="mockNew.statusCode" clearable style="width:10%"></el-input>
                </div>
              </el-tab-pane>
            </el-tabs>
          </div>
          <div class="mock" v-else>
            <el-input placeholder="URL" v-model="mockData.url" :readonly="cmOptions.readOnly">
              <el-select v-model="mockData.method" slot="prepend" placeholder="请选择">
                <el-option
                  v-for="(val,key) in type.method"
                  :key="key"
                  :label="val"
                  :value="key">
                </el-option>
              </el-select>
              <div slot="append" v-if="!cmOptions.readOnly">
                <el-button :loading='loading' icon="el-icon-check" @click="handleSaveEdit">保存</el-button>
                <el-divider direction="vertical"></el-divider>
                <el-button icon="el-icon-close" @click="handleCancleEdit">取消</el-button>
              </div>
            </el-input>
            <el-tabs v-model="activeRequestModel" type="border-card" style="margin-top:15px" @tab-click="updateReqCodemirror">
              <el-tab-pane label="请求头" name="requestHeader">
                <codemirror  ref="myCmRequestHeader" v-model="mockData.requestHeader"  :options="cmOptions"></codemirror>
              </el-tab-pane>
              <el-tab-pane label="请求体" name="requestBody">
                <codemirror  ref="myCmRequestBody" v-model="mockData.requestBody"  :options="cmOptions"></codemirror>
              </el-tab-pane>
              <el-tab-pane label="描述" name="msg">
                <div style="height: 300px">
                  <el-input type="textarea" :rows="14" placeholder="描述" v-model="mockData.msg" :readonly="cmOptions.readOnly"></el-input>
                </div>
              </el-tab-pane>
            </el-tabs>
            <el-tabs v-model="activeResponseModel" type="border-card" style="margin-top:15px" @tab-click="updateRepCodemirror">
              <el-tab-pane label="响应头" name="reposnseHeader">
                <codemirror  ref="myCmReposnseHeader" v-model="mockData.responseHeader"  :options="cmOptions"></codemirror>
              </el-tab-pane>
              <el-tab-pane label="响应体" name="reposnseBody">
                <codemirror  ref="myCmReposnseBody" v-model="mockData.responseBody"  :options="cmOptions"></codemirror>
              </el-tab-pane>
              <el-tab-pane label="HTTP状态码" name="statusCode">
                <div style="height: 300px">
                  <el-input placeholder="HTTP状态码" v-model="mockData.statusCode" clearable style="width:10%" :readonly="cmOptions.readOnly"></el-input>
                </div>
              </el-tab-pane>
            </el-tabs>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import Utils from 'lin/utils/util'
import { codemirror } from 'vue-codemirror'
import { get, post, put, _delete } from '@/lin/plugins/axios'
/* eslint-disable*/
import 'codemirror/mode/javascript/javascript.js'
import 'codemirror/theme/mdn-like.css'
import 'codemirror/theme/paraiso-light.css'
import 'codemirror/addon/scroll/simplescrollbars.css'
import 'codemirror/addon/scroll/simplescrollbars'


export default {
  components: {
    codemirror
  },
  data() {
    return {
      isAdd: false,
      activeRequestModel: 'requestBody',
      activeResponseModel: 'reposnseBody',
      filterText: '',
      treeLoading: false,
      loading: false,
      cid: null,
      mockData: {
        mid: 0,
        url: null,
        method: null,
        requestHeader: '',
        requestBody: '',
        responseHeader: '',
        responseBody: '',
        statusCode: 200,
        msg: ''
      },
      mockNew: {
        url: null,
        method: null,
        requestHeader: '',
        requestBody: '',
        responseHeader: '',
        responseBody: '',
        statusCode: 200,
        msg: ''        
      },
      type: {
        method: {},
        submit: {},
        deal: {},
        assert: {}
      },
      mockDatas: [],
      cmOptions: {
        tabSize: 2,
        mode: 'text/javascript',
        theme: 'mdn-like',
        lineNumbers: true,
        line: true,
        matchBrackets: true,
        autoRefresh: true,
        scrollbarStyle: 'overlay',
        readOnly: true
      },
      addOptions: {
        tabSize: 2,
        mode: 'text/javascript',
        theme: 'paraiso-light',
        lineNumbers: true,
        line: true,
        matchBrackets: true,
        autoRefresh: true,
        scrollbarStyle: 'overlay',
        readOnly: false
      },
      mockServer: '',
    }
  },
  activated() {
  },
  async created() {
    await this.getType()
    await this.searchMock()
    await this.getMockServer()
    // 节流搜素
    this.$watch(
      'filterText',
      Utils.debounce(() => {
        this.searchMock()
      }, 1000),
    )
  },
  methods: {
    async getMockServer() {
      let res
      try {
        res =  await get('/v1/mock/server', { showBackend: true })
        this.mockServer = res.server
        console.log(res.server)
      } catch (error) {
      } 
    },
    async getType() {
      const type = await get('/v1/case/type', { showBackend: true })
      this.type.method = type.METHOD
      this.type.submit = type.SUBMIT
      this.type.deal = type.DEAL
      this.type.assert = type.ASSERT
      this.mockData.method = '1'
      this.mockNew.method = '1'
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
    handleChoose(element) {
      this.handleCancelAdd()
      this.cmOptions.readOnly = true
      this.cmOptions.theme = 'mdn-like'
      for (let index = 0; index < this.mockDatas.length; index++) {
        this.$set(this.mockDatas[index], 'is_choose', false)
      }
      element.is_choose = true
      this.mockData.mid = element.mid
      this.mockData.method = element.method
      this.mockData.url = element.url
      this.mockData.msg = element.msg
      this.mockData.statusCode = element.status_code
      this.mockData.requestHeader = element.request_header
      this.mockData.requestBody = element.request_body
      this.mockData.responseHeader = element.response_header
      this.mockData.responseBody = element.response_body
      this.updateReqCodemirror()
      this.updateRepCodemirror()
    },
    handleAdd() {
      this.isAdd = true
      this.mockNew.method = '1'
    },
    handleCancelAdd() {
      this.isAdd = false
    },
    async addMock() {
      if (!this.mockNew.url) {
        this.$message.warning('请输入请求地址')
        return
      }
      let res
      try {
        this.loading = true
        res = await post('/v1/mock', this.mockNew, { showBackend: true })
        if (res.error_code === 0) {
          this.loading = false
          this.$message.success(`${res.msg}`)
          this.isAdd = false
          await this.searchMock()
          this.mockNew = {
            mid: 0,
            url: null,
            method: null,
            requestHeader: '',
            requestBody: '',
            responseHeader: '',
            responseBody: '',
            statusCode: 200,
            msg: ''        
          }
          this.cmOptions.theme = 'mdn-like'
          this.cmOptions.readOnly = true
        } else {
          this.loading = false
          this.$message.error(`${res.msg}`)
        }
      } catch (error) {
        this.loading = false
      }
    },
    async searchMock() {
      this.treeLoading = true
      try {
        this.mockDatas =  await get('/v1/mock', {'url': this.filterText}, { showBackend: true })
        this.treeLoading = false
        if (this.mockDatas.length>0) {
          this.handleChoose(this.mockDatas[0])
        }
      } catch (error) {
        this.mockDatas = []
        this.treeLoading = false
      }
    },
    handleEdit(element) {
      this.handleChoose(element)
      this.cmOptions.theme = 'paraiso-light'
      this.cmOptions.readOnly = false
    },
    handleCancleEdit() {
      this.cmOptions.theme = 'mdn-like'
      this.cmOptions.readOnly = true
    },
    async handleSaveEdit() {
      if (!this.mockData.url) {
        this.$message.warning('请输入请求地址')
        return
      }
      let res
      try {
        this.loading = true
        res = await put(`/v1/mock/${this.mockData.mid}`, this.mockData, { showBackend: true })
        if (res.error_code === 0) {
          this.loading = false
          this.$message.success(`${res.msg}`)
          this.isAdd = false
          await this.searchMock()
          this.cmOptions.theme = 'mdn-like'
          this.cmOptions.readOnly = true
        } else {
          this.loading = false
          this.$message.error(`${res.msg}`)
        }
      } catch (error) {
        this.loading = false
      }    
    },
    handleDelete(element) {
      this.$confirm('此操作将永久删除该mock数据, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }).then(async () => {
        const res = await _delete(`/v1/mock/${element.mid}`, { showBackend: true })
        if (res.error_code === 0) {
          this.searchMock()
          this.$message({
            type: 'success',
            message: `${res.msg}`,
          })
        }
      })
    },
    handleDebug(element) {
      this.$router.push({ path: '/postman', query: { mid: element.mid, mockServer: this.mockServer } })
    }
  },
}
</script>

<style lang="scss" scoped>
.container {
  padding: 30px;

  .mock {
    width: 95%;

    .el-select {
      width: 130px;
    }
  }

  .tree {
    height: 70vh;
    width: 100%;
    margin-top:30px;

    .list-group {
      background: rgba(236, 245, 255, 0.5);
      border-radius: 4px;
      overflow-y: auto;
      height: 100%;
      width: 100%;
      margin: auto;

      .item-color-normal {
        color: #409EFF;
        background: #ecf5ff;
        border:1px solid #b3d8ff;
      }

      .item-color-choose {
        color: #ecf5ff;
        background: #409EFF;
        border:1px solid #b3d8ff;
      }

      .item-color-get {
        color: #66DABE;
        background: #E6F9F4;
        border:1px solid #66DABE;
      }

      .item-color-get-choose {
        color: #E6F9F4;
        background: #00C292;
        border:1px solid #00C292;
      }

      .item-color-post {
        color: #f7aa25;
        background: #f5dcb1;
        border:1px solid #f7aa25;
      }

      .item-color-post-choose {
        color: #f5dcb1;
        background: #f7aa25;
        border:1px solid #f5dcb1;
      }

      .item-color-put {
        color: #88A1D7;
        background: #EBEFF8;
        border:1px solid #88A1D7;
      }

      .item-color-put-choose {
        color: #b1c6f5;
        background: #4b7ff0;
        border:1px solid #b1c6f5;
      }

      .item-color-delete {
        color: #F897A7;
        background: #FEEEF0;
        border:1px solid #F897A7;
      }

      .item-color-delete-choose {
        color: #FEEEF0;
        background: #F4516C;
        border:1px solid #FEEEF0;
      }

      .list-group-item {
        height: 35px;
        line-height: 35px;
        font-weight: 500;
        cursor: pointer;
        border-radius: 4px;
        padding: 0 5px;
        margin: 0 5px 5px 5px;
        display: flex;

        .name {
          flex: 1;
          white-space: nowrap;
          text-overflow: ellipsis;
          width: 100%;
          overflow: hidden;
        }

        i {
          margin: auto 2px;
          cursor: pointer
        }

      }
    }

    .flip-list-move {
      transition: transform 0.6s;
    }

    .list-group::-webkit-scrollbar{
      width:8px;
      height:8px;
      /**/
    }
    .list-group::-webkit-scrollbar-track{
      background: rgb(239, 239, 239);
      border-radius:2px;
    }
    .list-group::-webkit-scrollbar-thumb{
      background: #dad4d4;
      border-radius:10px;
    }
    .list-group::-webkit-scrollbar-thumb:hover{
      background: rgb(175, 173, 173);
    }
  }

}
</style>
