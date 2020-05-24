<template>
  <div>
    <div class="container">
      <div class="header">
        <el-row>
        <el-col :span="5">
          <label class="label">执行编号</label>
          <el-input placeholder="请输入执行编号" v-model="no" clearable style="width:60%" size="small"></el-input>
        </el-col>
        <el-col :span="5">
          <label class="label" >执行人</label>
            <el-cascader
              clearable
              filterable
              :show-all-levels="false"
              size="small"
              v-model="tester"
              :options="users"
              :props="{ expandTrigger: 'hover' }"
              ></el-cascader>
        </el-col>
        <el-col :span="6">
          <label class="label" >工程</label>
          <el-select v-model="project" filterable placeholder="请选择分组" clearable size="small" style="width:60%">
            <el-option
              v-for="item in projectList"
              :key="item.id"
              :label="item.name"
              :value="item.id">
            </el-option>
          </el-select>
        </el-col>
          <el-col :span="7">
          <label class="label" >执行时间</label>
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
      </div>
      <div><el-button style="margin-top:30px" type="danger" @click="handleDelete" v-auth="{ auth: '删除运行记录', type: 'disabled'}" plain>删除记录</el-button></div>
      <!-- 列表页面 -->
      <div class="table">
        <el-table
          :data="tableData"
          stripe
          v-loading="loading"
          style="width: 100%">
          <el-table-column
            fixed
            prop="task_no"
            label="执行编号"
            :show-overflow-tooltip="true"
            min-width="200">
          </el-table-column>
          <el-table-column
            prop="project_name"
            label="工程"
            :show-overflow-tooltip="true"
            min-width="280">
          </el-table-column>
          <el-table-column
            prop="username"
            label="执行人"
            :show-overflow-tooltip="true"
            min-width="160">
            <template slot-scope="scope">
              <i class="el-icon-user-solid" style="margin-top:auto;margin-bottom:auto"></i>
              <span style="margin-left: 10px">{{ scope.row.username }}</span>
            </template>
          </el-table-column>
          <el-table-column
            prop="success"
            label="成功"
            align="center"
            :show-overflow-tooltip="true"
            min-width="130">
            <template slot-scope="scope">
              <span style="margin: auto;color: #67C23A">{{ scope.row.success }}</span>
            </template>
          </el-table-column>
          <el-table-column
            prop="fail"
            label="失败"
            align="center"
            :show-overflow-tooltip="true"
            min-width="130">
            <template slot-scope="scope">
              <span style="margin: auto;color: #F56C6C">{{ scope.row.fail }}</span>
            </template>
          </el-table-column>
          <el-table-column
            prop="total"
            label="总计"
            align="center"
            :show-overflow-tooltip="true"
            min-width="130">
            <template slot-scope="scope">
              <span style="margin: auto;color: #409EFF">{{ scope.row.total }}</span>
            </template>
          </el-table-column>
          <el-table-column
            label="测试时间"
            :show-overflow-tooltip="true"
            min-width="180">
            <template slot-scope="scope">
              <i class="el-icon-time" style="margin-top:auto;margin-bottom:auto"></i>
              <span style="margin-left: 10px">{{ scope.row.create_time/1000 | filterTimeYmdHms }}</span>
            </template>
          </el-table-column>
          <el-table-column
            width="260"
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
                @click="toTestDetail(scope.$index, scope.row)">运行详情</el-button>
              <el-button
                size="mini"
                style="margin:auto"
                type="primary"
                plain
                v-auth="{ auth: '编辑用例', type: 'disabled'}"
            @click="toCaseLogList(scope.$index, scope.row)">用例日志</el-button>
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
</template>

<script>
import Utils from 'lin/utils/util'

import { get, _delete } from '@/lin/plugins/axios'

export default {
  data() {
    return {
      users: [],
      projectList: [],
      loading: true,
      project: null,
      tester: [null, null],
      no: null,
      datetime: null,
      startTime: null,
      endTime: null,
      tableData: [],
      page: 1,
      pages: 1,
      total: 0,
    }
  },
  activated() {
    // 跳转进入
    if (this.$route.query.pid) {
      for (let index = 0; index < this.projectList.length; index++) {
        if (this.$route.query.pid === this.projectList[index].id) {
          this.project = this.$route.query.pid
          this.no = null
          this.datetime = null
          this.tester = [null, null]
        }
      }
    }
    if (this.$route.query.no) {
      this.no = this.$route.query.no
      this.project = null
      this.datetime = null
      this.tester = [null, null]
    }
  },
  mounted() {
    // 跳转进入
    if (this.$route.query.pid) {
      this.project = this.$route.query.pid
      this.no = null
      this.datetime = null
      this.tester = [null, null]
    }
    if (this.$route.query.no) {
      this.no = this.$route.query.no
      this.project = null
      this.datetime = null
      this.tester = [null, null]
    }
  },
  async created() {
    await this.getTasks()
    await this.getAllProjects()
    await this.geUsers()
    // 节流搜素
    this.$watch(
      'no',
      Utils.debounce(() => {
        this.getTasks()
      }, 1000),
    )
  },
  methods: {
    async geUsers() {
      const allUsers = await get('/cms/user/userByInitials',
        {},
        { showBackend: true })
      this.GroupDataDeal(allUsers)
    },
    GroupDataDeal(allUsers) {
      for (const group of allUsers) {
        if (group.users.length > 0) {
          group.label = group.name
          group.children = group.users
          for (const user of group.children) {
            user.label = user.username
            user.value = user.id
          }
          this.users.push(group)
        }
      }
    },
    async getAllProjects() {
      try {
        this.projectList = await get('/v1/project', { showBackend: true })
      } catch (e) {
        this.projectList = []
      }
    },
    async handleRefresh() {
      await this.getTasks()
    },
    async getTasks() {
      this.loading = true
      if (this.datetime) {
        [this.startTime, this.endTime] = this.datetime
      } else {
        this.startTime = null
        this.endTime = null
      }
      try {
        const data = await get('/v1/task', {
          project: this.project,
          no: this.no,
          user: this.tester[1],
          start: this.startTime,
          end: this.endTime,
          page: this.page,
          count: 10
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
    handleCurrentChange(val) {
      this.page = val
      this.getTasks()
    },
    toCaseLogList(index, val) {
      this.$router.push({ path: '/test/log', query: { no: val.task_no } })
    },
    toTestDetail(index, val) {
      this.$router.push({ path: '/test/detail', query: { pid: val.project_id, taskNo: val.task_no } })
    },
    handleDelete() {
      this.$confirm('此操作将按当前查询条件永久删除记录及用例日志, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }).then(async () => {
        const res = await _delete('/v1/task/delete', {
          project: this.project,
          no: this.no,
          user: this.tester[1],
          start: this.startTime,
          end: this.endTime,
        }, { showBackend: true })
        if (res.error_code === 0) {
          this.getTasks()
          this.$message({
            type: 'success',
            message: `${res.msg}`,
          })
        }
      })
    },
  },
  watch: {
    project() {
      this.getTasks()
    },
    tester() {
      this.getTasks()
    },
    datetime() {
      this.getTasks()
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
  }

  .table{
    margin-top: 30px;
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
    margin-top: 40px;
    margin-bottom: 20px;
  }

}
</style>
