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
        <el-col :span="6" >
          <el-button type="primary" @click="caseDownload">用例下载<i class="el-icon-download el-icon--right"></i></el-button>
        </el-col>
        <el-col :span="7" >
          <el-button type="primary" @click="dialogVisible = true">用例上传<i class="el-icon-upload el-icon--right"></i></el-button>
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
                  <pre>{{ props.row.condition }}</pre>
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
            prop="create_user"
            label="创建人员"
            :show-overflow-tooltip="true"
            min-width="90">
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

      <el-dialog title="用例批量上传" :visible.sync="dialogVisible" width="30%" height="35%">
        <div style="width:100%;text-align:center">
          <div>
            <el-upload
              :action="UploadUrl()"
              :multiple="false"
              with-credentials
              :on-success="handleUploadSuccess"
              :limit="1"
              :on-exceed="handleExceed"
              :http-request="myUpload"
              name="file"
              :file-list="fileList">
              <el-button  type="primary" plain style="margin:0 30px 20px 0" @click="download()">模板下载</el-button>
              <el-button type="primary" style="margin:0 0 20px 30px">选择上传</el-button>
              <div slot="tip" class="el-upload__tip">只能上传xls/xlsx文件，且不超过2M</div>
            </el-upload>
          </div>
        </div>
      </el-dialog>

    </div>
    <!-- 编辑页面 -->
    <case-add-or-edit v-else @editClose="editClose" :editCase="editCase"></case-add-or-edit>
    <!-- 調試框 -->
    <debug-case :case="debugCase" :drawerShow="drawer" :type="type" @closed="drawerClose" :ruleShow="ruleShow"></debug-case>

  </div>
</template>

<script>
import Utils from 'lin/utils/util'

import { get, post, _delete } from '@/lin/plugins/axios'
import CaseAddOrEdit from './CaseAddOrEdit'
import DebugCase from '../../../components/DebugCase'

export default {
  components: {
    CaseAddOrEdit,
    DebugCase
  },
  inject: ['eventBus'],
  data() {
    return {
      fileList: [],
      dialogVisible: false,
      ruleShow: true,
      debugCase: {
        url: '',
        method: '',
        data: '',
        header: '',
        submit: '',
        server: '',
        name: '',
      },
      drawer: false,
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
      page: 1,
      pages: 1,
      total: 0,
      type: {
        method: {},
        submit: {},
        deal: {},
        assert: {}
      },
    }
  },
  activated() {
    if (this.$route.query.group) {
      for (let index = 0; index < this.allGroup.length; index++) {
        if (this.$route.query.group === this.allGroup[index].id) {
          this.caseGroup = this.$route.query.group
        }
      }
      this.method = null
      this.deal = null
      this.name = this.$route.query.case
      this.page = 1
      this.datetime = null
      this.url = null
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
        this.page = 1
        this.getCases()
      }, 1000),
    )
    this.$watch(
      'url',
      Utils.debounce(() => {
        this.page = 1
        this.getCases()
      }, 1000),
    )

    this.eventBus.$on('case', this.case)
    if (this.$route.query.group) {
      for (let index = 0; index < this.allGroup.length; index++) {
        if (this.$route.query.group === this.allGroup[index].id) {
          this.caseGroup = this.$route.query.group
        }
      }
      this.method = null
      this.deal = null
      this.name = this.$route.query.case
      this.page = 1
      this.datetime = null
      this.url = null
    }
  },
  beforeDestroy() {
    this.eventBus.$off('case', this.case)
  },
  methods: {
    // 监听新增更新用例是否成功
    async case(flag) {
      if (flag === true) {
        this.page = 1
        await this.getCases()
      }
    },
    async handleRefresh() {
      this.page = 1
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
          this.page = 1
          this.getCases()
          this.$message({
            type: 'success',
            message: `${res.msg}`,
          })
        }
      })
    },
    caseDownload() {
      this.$confirm('将按当前查询条件导出用例, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'info',
      }).then(async () => {
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
        this.$axios({
          baseURL: `${process.env.VUE_APP_BASE_URL}`,
          url: '/v1/case/caseDownload',
          method: 'get',
          responseType: 'blob',
          params: {
            caseGroup: this.caseGroup,
            name: this.name,
            method: methodPara,
            deal: dealPara,
            url: this.url,
            start: this.startTime,
            end: this.endTime,
            handleError: true
          }
        }).then(res => {
          const fileName = 'cases.xls'
          const blob = new Blob([res])
          const link = document.createElement('a')
          link.download = fileName
          link.style.display = 'none'
          link.href = URL.createObjectURL(blob)
          document.body.appendChild(link)
          link.click()
          URL.revokeObjectURL(link.href)
          document.body.removeChild(link)
        }).catch(error => {
          const reader = new FileReader()
          reader.readAsText(error.data, 'utf-8')
          reader.onload = e => {
            this.$message.warning(JSON.parse(reader.result).msg)
            console.log(e.target.result)
          }
        })
      })
    },
    handleDebug(index, row) {
      this.drawer = true
      this.debugCase = row
    },
    drawerClose() {
      this.drawer = false
    },
    editClose() {
      this.showEdit = false
      this.getCases()
    },
    handleCurrentChange(val) {
      this.page = val
      this.getCases()
    },
    download() {
      window.location.href = `${process.env.VUE_APP_BASE_URL}v1/case/downloadTemplate`
    },
    UploadUrl() {
      return `${process.env.VUE_APP_BASE_URL}v1/case/upload`
    },
    handleExceed(files, fileList) {
      this.$message.warning(`当前限制选择 1 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`)
    },
    handleUploadSuccess() {
      this.$message.success('上传用例成功')
      this.dialogVisible = false
      this.page = 1
      this.getCases()
    },
    async myUpload(content) {
      const formData = new FormData()
      formData.append('file', content.file)
      await post(content.action, formData, { showBackend: true })
    },
  },
  watch: {
    caseGroup() {
      this.page = 1
      this.getCases()
    },
    datetime() {
      this.page = 1
      this.getCases()
    },
    method() {
      this.page = 1
      this.getCases()
    },
    deal() {
      this.page = 1
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

  .table /deep/ .el-table__fixed-right {
    height: 100% !important;
  }
  .table /deep/ .el-table__fixed {
    height: 100% !important;
  }

  .table{
    width: 100%;
    margin-top: 30px;
    .method {
      .get {
        color: #00C292;
        font-weight: 500;
      }
      .post {
        color: #E6A23C;
        font-weight: 500;
      }
      .put {
        color: #3963BC;
        font-weight: 500;
      }
      .delete {
        color: #E46A76;
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

}
.container /deep/ .el-dialog__body {
  height: 12vh;
  overflow: auto;
  }
</style>
