<template>
  <div>
    <div class="container" v-if="!showDetail">
      <div class="header">
        <el-row>
          <el-col :span="6">
            <label class="label" >用例名称</label>
            <el-input placeholder="请输入用例名称" v-model="name" clearable style="width:60%" size="small"></el-input>
          </el-col>
          <el-col :span="6">
            <label class="label" >工程名称</label>
            <el-input placeholder="请输入工程名称" v-model="project" clearable style="width:60%" size="small"></el-input>
          </el-col>
          <el-col :span="6">
            <label class="label" >任务编号</label>
            <el-input placeholder="请输入任务编号" v-model="task" clearable style="width:60%" size="small"></el-input>
          </el-col>
            <el-col :span="6">
            <label class="label" >测试时间</label>
            <el-date-picker
              v-model="datetime"
              clearable
              :default-time="['00:00:00', '23:59:59']"
              value-format="yyyy-MM-dd HH:mm:ss"
              size="small"
              style="width:80%"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期">
            </el-date-picker>
          </el-col>
        </el-row>
        <el-row style="margin-top:30px">
          <el-col :span="6">
            <label class="label">接口地址</label>
            <el-input placeholder="请输入URL" v-model="url" clearable style="width:60%" size="small"></el-input>
          </el-col>
          <el-col :span="6">
            <label class="label">测试结果</label>
            <el-select v-model="result" filterable placeholder="请选择测试结果" clearable size="small" style="width:60%">
              <el-option
                v-for="item in resultType"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </el-col>
        </el-row>
        <div class="btn">
          <el-button
            type="danger"
            @click="handleDelete"
            v-auth="{ auth: '删除用例日志', type: 'disabled'}"
            plain>删除日志</el-button>
          <div class="btn-search">
            <el-button plain @click="reset">重置</el-button>
            <el-button type="primary" plain @click="search">查询</el-button>
          </div>
        </div>
      <!-- 列表页面 -->
      <div class="table">
        <el-table
          :data="tableData"
          stripe
          v-loading="loading"
          style="width: 100%">
          <el-table-column
            fixed
            prop="name"
            label="用例名称"
            :show-overflow-tooltip="true"
            min-width="180">
          </el-table-column>
          <el-table-column
            fixed
            prop="project_name"
            label="工程名称"
            :show-overflow-tooltip="true"
            min-width="180">
          </el-table-column>
          <el-table-column
            fixed
            prop="task_no"
            label="任务编号"
            :show-overflow-tooltip="true"
            min-width="150">
          </el-table-column>
          <el-table-column
            align="center"
            prop="actual_result"
            label="测试结果"
            :show-overflow-tooltip="true"
            min-width="115">
            <template slot-scope="scope">
              <div v-if="scope.row.actual_result" class="success" style="margin:auto">成功</div>
              <div v-else class="fail" style="margin:auto">失败</div>
            </template>
          </el-table-column>
          <el-table-column
            prop="url"
            label="接口地址"
            :show-overflow-tooltip="true"
            min-width="230">
          </el-table-column>
          <el-table-column
            label="测试时间"
            min-width="180">
            <template slot-scope="scope">
              <i class="el-icon-time" style="margin-top:auto;margin-bottom:auto"></i>
              <span style="margin-left: 10px">{{ scope.row.create_time/1000 | filterTimeYmdHms }}</span>
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
                @click="toRecordList(scope.$index, scope.row)">运行记录</el-button>
              <el-button
                size="mini"
                style="margin:auto"
                type="primary"
                plain
                @click="handleDetail(scope.$index, scope.row)">日志详情</el-button>
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
    </div>
    <log-detail v-else @detailClose="detailClose" :detail="detail" :type="type"></log-detail>
  </div>
</template>

<script>
import { _delete, post, get } from '@/lin/plugins/axios'
import LogDetail from './LogDetail'

export default {
  components: {
    LogDetail
  },
  inject: ['eventBus'],
  data() {
    return {
      detail: {},
      showDetail: false,
      type: {
        method: {},
        submit: {},
        deal: {},
        assert: {}
      },
      loading: false,
      name: null,
      project: null,
      task: null,
      url: '',
      datetime: null,
      startTime: null,
      endTime: null,
      result: null,
      resultType: [
        {
          value: true,
          label: '成功'
        },
        {
          value: false,
          label: '失败'
        }
      ],
      tableData: [],
      page: 1,
      pages: 1,
      total: 0,
    }
  },
  async created() {
    await this.getCaseLogs()
    await this.getType()
  },
  activated() {
    if (this.$route.query.pname) {
      this.showDetail = false
      this.project = this.$route.query.pname
      this.name = null
      this.task = null
      this.page = 1
      this.result = null
      this.url = null
      this.datetime = null
      this.getCaseLogs()
    }
    if (this.$route.query.no) {
      this.showDetail = false
      this.task = this.$route.query.no
      this.name = null
      this.project = null
      this.page = 1
      this.result = null
      this.url = null
      this.datetime = null
      this.getCaseLogs()
    }
  },
  methods: {
    async getCaseLogs() {
      this.loading = true
      if (this.datetime) {
        [this.startTime, this.endTime] = this.datetime
      } else {
        this.startTime = null
        this.endTime = null
      }
      try {
        const data = await post('/v1/case/logs', {
          name: this.name,
          project: this.project,
          task: this.task,
          result: this.result,
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
    async getType() {
      const type = await get('/v1/case/type', { showBackend: true })
      this.type.method = type.METHOD
      this.type.submit = type.SUBMIT
      this.type.deal = type.DEAL
      this.type.assert = type.ASSERT
    },
    handleDetail(index, row) {
      this.showDetail = true
      this.detail = row
    },
    reset() {
      this.name = null
      this.project = null
      this.task = null
      this.page = 1
      this.result = null
      this.url = null
      this.datetime = null
      this.getCaseLogs()
    },
    search() {
      this.page = 1
      this.getCaseLogs()
    },
    handleCurrentChange(val) {
      this.page = val
      this.getCaseLogs()
    },
    detailClose() {
      this.showDetail = false
      this.getCaseLogs()
    },
    handleDelete() {
      this.$confirm('此操作将按当前查询条件永久删除日志, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }).then(async () => {
        const res = await _delete('/v1/case/logs/delete', {
          name: this.name,
          project: this.project,
          task: this.task,
          result: this.result,
          url: this.url,
          start: this.startTime,
          end: this.endTime
        }, { showBackend: true })
        if (res.error_code === 0) {
          this.getCaseLogs()
          this.$message({
            type: 'success',
            message: `${res.msg}`,
          })
        }
      })
    },
    toRecordList(index, val) {
      this.$router.push({ path: '/test/record', query: { no: val.task_no } })
    },
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

    .btn {
      display: flex;
      justify-content: space-between;
      margin-top: 15px;
      .btn-search {
        button {
          margin-left: 30px;
        }
      }
    }
  }

  .table{
    margin-top: 30px;

    .success {
      color: #00C292;
      font-weight: 500;
    }

    .fail {
      color: #E46A76;
      font-weight: 500;
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
</style>
