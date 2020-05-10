<template>
  <div>
    <div class="container" v-if="!showEdit">
      <div class="header">
        <el-row>
        <el-col :span="5">
          <label class="label">用例分组</label>
          <el-select v-model="caseGroup" filterable placeholder="请选用例分组" clearable size="small" style="width:60%">
            <el-option
              v-for="item in allGroup"
              :key="item.id"
              :label="item.name"
              :value="item.id">
            </el-option>
          </el-select>
        </el-col>
        <el-col :span="5">
          <label class="label" >用例名称</label>
          <el-input placeholder="请输入用例名称" v-model="name" clearable style="width:60%" size="small"></el-input>
        </el-col>
        <el-col :span="6">
          <label class="label" >URL</label>
          <el-input placeholder="请输入URL" v-model="url" clearable style="width:75%" size="small"></el-input>
        </el-col>
          <el-col :span="7">
          <label class="label" >更新时间</label>
          <el-date-picker
            v-model="datetime"
            clearable
            :default-time="['00:00:00', '23:59:59']"
            value-format="yyyy-MM-dd HH:mm:ss"
            size="small"
            style="width:70%"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期">
          </el-date-picker>
        </el-col>
        <el-col :span="1"><i class="el-icon-refresh" @click="handleRefresh" style="font-size:1.6em"></i></el-col>
      </el-row>
      <el-row style="margin-top:30px">
        <el-col :span="5">
          <label class="label">请求方法</label>
          <el-select v-model="method" filterable placeholder="请选择请求方法" clearable size="small" style="width:60%">
            <el-option
              :key="key" v-for="(val,key) in type.method"
              :label="val"
              :value="key">
            </el-option>
          </el-select>
        </el-col>
        <el-col :span="5">
          <label class="label">后置处理</label>
          <el-select v-model="deal" filterable placeholder="请选择处理方法" clearable size="small" style="width:60%">
            <el-option
              :key="key" v-for="(val,key) in type.deal"
              :label="val"
              :value="key">
            </el-option>
          </el-select>
        </el-col>
      </el-row>
      </div>
      <!-- 列表页面 -->
      <div class="table">
        <el-table
          :data="tableData"
          stripe
          v-loading="loading"
          style="width: 100%">
          <el-table-column type="expand" fixed>
            <template slot-scope="props">
              <el-form label-position="left" inline class="demo-table-expand">
                <el-form-item label="处理方法">
                  <div v-for="(val,key) in type.deal" :key="key">
                    <span v-if="props.row.deal === parseInt(key)">{{ val }}</span>
                  </div>
                </el-form-item>
                <el-form-item label="处理语句">
                  <span>{{ props.row.condition }}</span>
                </el-form-item>
                <el-form-item label="断言方式">
                  <div v-for="(val,key) in type.assert" :key="key">
                    <span v-if="props.row.assertion === parseInt(key)">{{ val }}</span>
                  </div>
                </el-form-item>
                <el-form-item label="预期结果">
                  <span>{{ props.row.expect }}</span>
                </el-form-item>
                <el-form-item label="data">
                  <pre>{{ props.row.data }}</pre>
                </el-form-item>
                <el-form-item label="header">
                  <pre>{{ props.row.header }}</pre>
                </el-form-item>
              </el-form>
            </template>
          </el-table-column>
          <el-table-column
            fixed
            prop="name"
            label="用例名称"
            :show-overflow-tooltip="true"
            min-width="200">
          </el-table-column>
          <el-table-column
            label="请求方法"
            :show-overflow-tooltip="true"
            width="125">
            <template slot-scope="scope">
              <div :key="key" v-for="(val,key) in type.method" class="method">
                <div v-if="scope.row.method === 1 && scope.row.method === parseInt(key)" class="get">{{val}}</div>
                <div v-else-if="scope.row.method === 2 && scope.row.method === parseInt(key)" class="post">{{val}}</div>
                <div v-else-if="scope.row.method === 3 && scope.row.method === parseInt(key)" class="put">{{val}}</div>
                <div v-else-if="scope.row.method === 4 && scope.row.method === parseInt(key)" class="delete">{{val}}</div>
              </div>
            </template>
          </el-table-column>
          <el-table-column
            prop="url"
            label="URL"
            :show-overflow-tooltip="true"
            min-width="280">
          </el-table-column>
          <el-table-column
            label="提交方式"
            :show-overflow-tooltip="true"
            width="125">
            <template slot-scope="scope">
              <div :key="key" v-for="(val,key) in type.submit" class="submit">
                <div v-if="scope.row.submit === 1 && scope.row.submit === parseInt(key)" class="json">{{val}}</div>
                <div v-else-if="scope.row.submit === 2 && scope.row.submit === parseInt(key)" class="form">{{val}}</div>
              </div>
            </template>
          </el-table-column>
          <el-table-column
            prop="group_name"
            label="用例组"
            :show-overflow-tooltip="true"
            min-width="160">
          </el-table-column>
          <el-table-column
            label="描述"
            align="center"
            width="70">
            <template slot-scope="scope">
              <el-tooltip effect="dark" placement="top-start" v-if="scope.row.info">
                <div slot="content">{{scope.row.info}}</div>
                <l-icon name="info" color="#3963bc" height="1.6em" width="1.6em" style="margin:auto"></l-icon>
              </el-tooltip>
              <l-icon name="info" color="#ccc" height="1.6em" width="1.6em" v-else style="margin:auto"></l-icon>
            </template>
          </el-table-column>
          <el-table-column
            width="250"
            align="center"
            fixed="right"
            label="操作">
            <template slot-scope="scope">
              <el-button
                size="mini"
                style="margin:auto"
                type="primary"
                plain
                v-auth="{ auth: '编辑用例', type: 'disabled'}"
                @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
              <el-button
                size="mini"
                type="danger"
                style="margin:auto"
                plain
                v-auth="{ auth: '删除用例', type: 'disabled'}"
                @click="handleDelete(scope.$index, scope.row)">删除</el-button>
              <el-button
                size="mini"
                type="info"
                style="margin:auto"
                plain=""
                @click="handleDebug(scope.$index, scope.row)">调试</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div class="pagination">
        <el-pagination
          background
          :hide-on-single-page=true
          @current-change="handleCurrentChange"
          layout="prev, pager, next"
          :current-page="page"
          :page-size=10
          :total="total">
        </el-pagination>
      </div>
    </div>
    <!-- 编辑页面 -->
    <case-add-or-edit v-else @editClose="editClose" :editCase="editCase"></case-add-or-edit>
    <!-- 調試框 -->
    <el-drawer
      title="用例调试"
      :with-header="false"
      :visible.sync="drawer"
      direction="ltr"
      ustom-class="drawer"
      ref="drawer"
      size='31%'
      >
      <div class="debug">
        <div class="title">{{debugForm.name}}</div>
        <div class="debugForm">
          <el-form :model="debugForm" :rules="rules" ref="debugForm">
            <el-form-item label="SERVER" label-width="80px" prop="server">
              <el-input v-model="debugForm.server" autocomplete="off" placeholder="请输入服务地址"></el-input>
            </el-form-item>
            <el-form-item label="URL" label-width="80px" prop="url">
              <el-input v-model="debugForm.url" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="请求方法" label-width="80px" prop="method">
              <el-radio-group v-model="debugForm.method">
                <label v-for="(val,key) in type.method" :key="key" class="el-radio">
                  <el-radio :label="key">{{val}}</el-radio>
                </label>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="header" prop="header" label-width="80px">
              <el-input size="medium" type="textarea" :autosize="{ minRows: 3, maxRows: 5}" v-model="debugForm.header">
              </el-input>
            </el-form-item>
            <el-form-item label="data" prop="data" label-width="80px">
              <el-input size="medium" type="textarea" :autosize="{ minRows: 3, maxRows: 5}" v-model="debugForm.data">
              </el-input>
            </el-form-item>
            <el-form-item label="请求方式" label-width="80px" prop="submit">
              <el-radio-group v-model="debugForm.submit">
                <label v-for="(val,key) in type.submit" :key="key" class="el-radio">
                  <el-radio :label="key">{{val}}</el-radio>
                </label>
              </el-radio-group>
            </el-form-item>
          </el-form>
        </div>
        <div class="result" ref="result" v-loading='debugLoding'>
          <el-scrollbar style="height:100%" v-if="debugResult">
            <el-tag v-if="this.statusCode>=400"  effect="plain" type="danger" class="code">{{statusCode}}</el-tag>
            <el-tag v-else  effect="plain" type="success" class="code">{{statusCode}}</el-tag>
            <i class="el-icon-copy-document" @click="copyText"></i>
            <pre>{{debugResult}}</pre>
          </el-scrollbar>
        </div>
        <div class="debugButton">
          <el-button type="primary" @click="send" icon="el-icon-s-promotion" :loading='debugLoding'>{{ debugLoding ? 'sending...' : 'send' }}</el-button>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script>
import Utils from 'lin/utils/util'

import { get, _delete, post } from '@/lin/plugins/axios'
import CaseAddOrEdit from './CaseAddOrEdit'

export default {
  components: {
    CaseAddOrEdit
  },
  inject: ['eventBus'],
  data() {
    return {
      statusCode: 200,
      debugLoding: false,
      debugResultDiv: false,
      debugResult: '',
      drawer: false,
      debugForm: {
        url: '',
        method: '',
        data: '',
        header: '',
        submit: '',
        server: '',
        name: '',
      },
      rules: {
        server: [
          { required: true, message: '请输入服务地址', trigger: 'blur' },
        ],
      },
      editBookID: {},
      loading: false,
      caseGroup: null,
      method: null,
      deal: null,
      allGroup: null,
      name: '',
      url: '',
      datetime: null,
      startTime: null,
      endTime: null,
      tableData: [],
      showEdit: false,
      editBook: {},
      page: 1,
      pages: 1,
      total: 0,
      type: {
        method: {},
        submit: {},
        deal: {},
        assert: {}
      }
    }
  },
  async created() {
    this.loading = true
    await this.getType()
    await this.getCases()
    this.loading = false
    await this.getAllGroups()
    // 节流搜素
    this.$watch(
      'name',
      Utils.debounce(() => {
        this.getCases()
      }, 1000),
    )
    this.$watch(
      'url',
      Utils.debounce(() => {
        this.getCases()
      }, 1000),
    )

    this.eventBus.$on('case', this.case)
  },
  beforeDestroy() {
    this.eventBus.$off('case', this.case)
  },
  methods: {
    // 监听新增更新用例是否成功
    async case(flag) {
      if (flag === true) {
        await this.getCases()
      }
    },
    async handleRefresh() {
      await this.getCases()
    },
    async getType() {
      const type = await get('/v1/case/type', { showBackend: true })
      this.type.method = type.METHOD
      this.type.submit = type.SUBMIT
      this.type.deal = type.DEAL
      this.type.assert = type.ASSERT
    },
    async getAllGroups() {
      try {
        this.allGroup = await get('/v1/caseGroup/auth', { showBackend: true })
      } catch (e) {
        this.loading = false
      }
    },
    async getCases() {
      this.loading = true
      if (this.datetime) {
        [this.startTime, this.endTime] = this.datetime
      } else {
        this.startTime = null
        this.endTime = null
      }
      let methodPara = null
      let dealPara = null
      if (this.method) {
        methodPara = parseInt(this.method, 10)
      }
      if (this.deal) {
        dealPara = parseInt(this.deal, 10)
      }
      try {
        const data = await get('/v1/case', {
          caseGroup: this.caseGroup,
          name: this.name,
          method: methodPara,
          deal: dealPara,
          url: this.url,
          start: this.startTime,
          end: this.endTime,
          page: this.page
        }, { showBackend: true })
        this.tableData = data.data
        this.total = data.total
        this.page = data.page
        this.pages = data.pages
        this.loading = false
      } catch (error) {
        if (error.error_code !== 0) {
          this.tableData = []
        }
        this.loading = false
      }
    },
    handleEdit(index, row) {
      this.showEdit = true
      this.editCase = row
    },
    handleDelete(index, row) {
      this.$confirm('此操作将永久删除该用例, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }).then(async () => {
        const res = await _delete(`/v1/case/${row.id}`, { showBackend: true })
        if (res.error_code === 0) {
          this.getCases()
          this.$message({
            type: 'success',
            message: `${res.msg}`,
          })
        }
      })
    },
    handleDebug(index, row) {
      this.drawer = true
      this.debugForm.url = row.url
      this.debugForm.method = row.method.toString()
      this.debugForm.header = row.header
      this.debugForm.data = row.data
      this.debugForm.submit = row.submit.toString()
      this.debugForm.name = row.name
    },
    editClose() {
      this.showEdit = false
      this.getCases()
    },
    handleCurrentChange(val) {
      this.page = val
      this.getCases()
    },
    copyText() {
      const text = this.$refs.result.innerText
      if (text) {
        const input = document.createElement('input')
        input.value = text
        document.body.appendChild(input)
        input.select()
        document.execCommand('Copy')
        document.body.removeChild(input)
        this.$message({
          type: 'success',
          message: '复制文本成功',
        })
      }
    },
    send() {
      this.$refs.debugForm.validate(async valid => {
        if (valid) {
          this.debugResultDiv = false
          this.debugResult = ''
          this.debugLoding = true
          try {
            const result = await post('/v1/case/debug', {
              url: this.debugForm.server + this.debugForm.url,
              method: parseInt(this.debugForm.method, 10),
              submit: parseInt(this.debugForm.submit, 10),
              data: this.debugForm.data,
              header: this.debugForm.header,
            }, { showBackend: true })
            this.statusCode = result.statusCode
            if (result.body.constructor === String) {
              this.debugResult = result.body
            } else {
              this.debugResult = JSON.stringify(result.body, null, '\t')
            }
            this.debugResultDiv = true
            this.debugLoding = false
          } catch (error) {
            this.debugLoding = false
          }
        } else {
          return false
        }
      })
    },
  },
  watch: {
    caseGroup() {
      this.getCases()
    },
    datetime() {
      this.getCases()
    },
    method() {
      this.getCases()
    },
    deal() {
      this.getCases()
    }
  },
}
</script>

<style lang="scss" scoped>
.container {
  padding: 30px;

  .header {
    color: $parent-title-color;
    font-size: 16px;
    font-weight: 500;

    .el-icon-refresh{
      font-size: 20px;
      cursor: pointer;
    }

    .label {
      margin-right: 10px;
    }
  }

  .table{
    margin-top: 30px;
    .method {
      .get {
        color: #67C23A;
        font-weight: 500;
      }
      .post {
        color: #E6A23C;
        font-weight: 500;
      }
      .put {
        color: #409EFF;
        font-weight: 500;
      }
      .delete {
        color: #F56C6C;
        font-weight: 500;
      }
    }

    .submit {
      .json {
        color: #4f383e;
        font-weight: 500;
      }
      .form {
        color: #5c2223;
        font-weight: 500;
      }
    }

  }

  .table /deep/ .demo-table-expand {
    font-size: 0;
  }
  .table /deep/ .demo-table-expand label {
    width: 80px;
    color: #3963bc;
  }
  .table /deep/ .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 50%;
  }
  .table /deep/ .el-form-item__content {
    margin-bottom: 0;
  }
  .table /deep/ .el-table .cell {
    padding-left: 20px;
  }
  // 滚动条优化
  .table /deep/ .el-table__body-wrapper::-webkit-scrollbar {
    width: 6px;
    height: 10px;
  }
  .table /deep/ .el-table__body-wrapper::-webkit-scrollbar-thumb {
    background-color: #ddd;
    border-radius: 5px;
  }

  .pagination {
    display: flex;
    justify-content: flex-end;
    margin-top: 30px;
    margin-bottom: 20px;
  }

  .debug {
    padding: 25px;
    height: 100vh;
    display: flex;
    flex-direction: column;

    .title {
      color: $parent-title-color;
      font-size: 18px;
      font-weight: 600;
    }

    .debugForm {
      margin-top: 20px;
    }

    .result {
      flex: 1;
      overflow: auto;

      .el-scrollbar__view {
        position: relative;
        i {
          position: absolute;
          right: 0;
          top: 5px;
        }
        .code {
          position: absolute;
          right: 30px;
          top: 0;
        }
      }

    }

    .debugButton {
      display: flex;
      button {
        flex: 1;
      }
    }

  }
  .el-drawer .ltr {
    left: 0;
    overflow: scroll;
  }
}
</style>
