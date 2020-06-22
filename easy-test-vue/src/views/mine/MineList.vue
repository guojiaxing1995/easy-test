<template>
  <div>
    <div class="container">
      <div class="header">
        <el-row>
          <el-col :span="7">
            <label class="label" >用例名称</label>
            <el-input placeholder="请输入用例名称" v-model="caseName" clearable style="width:70%" size="small"></el-input>
          </el-col>
          <el-col :span="7">
            <label class="label" >工程名称</label>
            <el-input placeholder="请输入工程名称" v-model="projectName" clearable style="width:70%" size="small"></el-input>
          </el-col>
          <el-col :span="7">
            <label class="label" >测试时间</label>
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
      <el-tabs tab-position="left" style="margin-top: 30px;" >
        <el-tab-pane label="我创建的用例" class="caseList">
          <!-- 列表页面 -->
          <div class="table">
            <el-table
              :data="caseTableData"
              stripe
              v-loading="caseLoading"
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
            </el-table>
          </div>
          <div class="pagination">
            <el-pagination
              background
              :hide-on-single-page=true
              layout="prev, pager, next"
              :current-page="caseList.page"
               @current-change="handleCaseCurrentChange"
              :page-size=10
              :total="caseList.total">
            </el-pagination>
          </div>
        </el-tab-pane>
        <el-tab-pane label="我维护的工程" class="projectList">
          <div class="table">
            <el-table
              :data="projectTableDate"
              stripe
              v-loading="projectLoading"
              style="width: 100%">
              <el-table-column
                fixed
                prop="name"
                label="名称"
                :show-overflow-tooltip="true"
                min-width="200">
              </el-table-column>
              <el-table-column
                prop="server"
                label="服务地址"
                :show-overflow-tooltip="true"
                min-width="200">
              </el-table-column>
              <el-table-column
                prop="user_name"
                label="维护人员"
                :show-overflow-tooltip="true"
                min-width="100">
              </el-table-column>
              <el-table-column
                prop="send_email"
                label="发送邮件"
                align="center"
                :show-overflow-tooltip="true"
                min-width="80">
                <template slot-scope="scope">
                  <div slot="content" v-if="scope.row.send_email" style="margin:auto">是</div>
                  <div slot="content" v-else style="margin:auto">否</div>
                </template>
              </el-table-column>
              <el-table-column
                prop="copy_person_name"
                label="邮件抄送人员"
                :show-overflow-tooltip="true"
                min-width="200">
                <template slot-scope="scope">
                  <div slot="content">{{scope.row.copy_person_name.join(',')}}</div>
                </template>
              </el-table-column>
              <el-table-column
                prop="info"
                label="描述"
                :show-overflow-tooltip="true"
                min-width="350">
              </el-table-column>
              <el-table-column
                label="类型"
                fixed="right"
                width="100">
                <template slot-scope="scope">
                  <div :key="key" v-for="(val,key) in projecType">
                    <div v-if="scope.row.type === parseInt(key)">{{val}}</div>
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </div>
          <div class="pagination">
            <el-pagination
              background
              :hide-on-single-page=true
              @current-change="handleProjectCurrentChange"
              layout="prev, pager, next"
              :current-page="projectList.page"
              :page-size=10
              :total="projectList.total">
            </el-pagination>
          </div>
        </el-tab-pane>
        <el-tab-pane label="我维护的定时任务" class="schedulerList">
          <div class="table">
            <el-table
              :data="schedulerTableData"
              stripe
              v-loading="schedulerLoading"
              style="width: 100%">
              <el-table-column
                fixed
                prop="state"
                align="center"
                label="状态"
                :show-overflow-tooltip="true"
                min-width="60">
                <template slot-scope="scope">
                  <div slot="content" v-if="scope.row.state" class="state running"></div>
                  <div slot="content" v-else class="state stoped"></div>
                </template>
              </el-table-column>
              <el-table-column
                fixed
                prop="scheduler_id"
                label="任务编号"
                :show-overflow-tooltip="true"
                min-width="200">
              </el-table-column>
              <el-table-column
                prop="project_name"
                label="工程名称"
                :show-overflow-tooltip="true"
                min-width="200">
              </el-table-column>
              <el-table-column
                prop="cron"
                label="cron表达式"
                :show-overflow-tooltip="true"
                min-width="150">
              </el-table-column>
              <el-table-column
                prop="next_run_time"
                label="下次执行时间"
                :show-overflow-tooltip="true"
                min-width="160">
                <template slot-scope="scope">
                  <i v-show="scope.row.next_run_time" class="el-icon-time" style="margin-top:auto;margin-bottom:auto"></i>
                  <span style="margin-left: 10px">{{ scope.row.next_run_time }}</span>
                </template>
              </el-table-column>
              <el-table-column
                prop="user_name"
                label="维护人员"
                :show-overflow-tooltip="true"
                min-width="100">
              </el-table-column>
              <el-table-column
                prop="send_email"
                label="发送邮件"
                align="center"
                :show-overflow-tooltip="true"
                min-width="80">
                <template slot-scope="scope">
                  <div slot="content" v-if="scope.row.send_email" style="margin:auto">是</div>
                  <div slot="content" v-else style="margin:auto">否</div>
                </template>
              </el-table-column>
              <el-table-column
                prop="copy_person_name"
                label="邮件抄送人员"
                :show-overflow-tooltip="true"
                min-width="200">
                <template slot-scope="scope">
                  <div slot="content">{{scope.row.copy_person_name.join(',')}}</div>
                </template>
              </el-table-column>
            </el-table>
          </div>
          <div class="pagination">
            <el-pagination
              background
              :hide-on-single-page=true
              @current-change="handleSchedulerCurrentChange"
              layout="prev, pager, next"
              :current-page="schedulerList.page"
              :page-size=10
              :total="schedulerList.total">
            </el-pagination>
          </div>
        </el-tab-pane>
        <el-tab-pane label="我执行的测试" class="taskList">
          <div class="table">
            <el-table
              :data="taskTableData"
              stripe
              v-loading="taskLoading"
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
                  <span style="margin: auto;color: #00C292">{{ scope.row.success }}</span>
                </template>
              </el-table-column>
              <el-table-column
                prop="fail"
                label="失败"
                align="center"
                :show-overflow-tooltip="true"
                min-width="130">
                <template slot-scope="scope">
                  <span style="margin: auto;color: #E46A76">{{ scope.row.fail }}</span>
                </template>
              </el-table-column>
              <el-table-column
                prop="total"
                label="总计"
                align="center"
                :show-overflow-tooltip="true"
                min-width="130">
                <template slot-scope="scope">
                  <span style="margin: auto;color: #3963BC">{{ scope.row.total }}</span>
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
            </el-table>
          </div>
          <div class="pagination">
            <el-pagination
              background
              :hide-on-single-page=true
              @current-change="handleTaskCurrentChange"
              layout="prev, pager, next"
              :current-page="taskList.page"
              :page-size=10
              :total="taskList.total">
            </el-pagination>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
import Utils from 'lin/utils/util'

import { get } from '@/lin/plugins/axios'

export default {
  data() {
    return {
      caseLoading: false,
      projectLoading: false,
      schedulerLoading: false,
      taskLoading: false,
      type: {
        method: {},
        submit: {},
        deal: {},
        assert: {}
      },
      projecType: {},
      caseName: null,
      projectName: null,
      datetime: null,
      startTime: null,
      endTime: null,
      caseList: {
        page: 1,
        total: 0,
      },
      projectList: {
        page: 1,
        total: 0,
      },
      schedulerList: {
        page: 1,
        total: 0,
      },
      taskList: {
        page: 1,
        total: 0,
      },
      caseTableData: [],
      projectTableDate: [],
      schedulerTableData: [],
      taskTableData: [],
    }
  },
  activated() {

  },
  async created() {
    await this.getCases()
    await this.getType()
    await this.getAllProjects()
    await this.getJobs()
    await this.getTasks()
    // 节流搜素
    this.$watch(
      'caseName',
      Utils.debounce(() => {
        this.caseList.page = 1
        this.getCases()
      }, 1000),
    )
    this.$watch(
      'projectName',
      Utils.debounce(() => {
        this.projectList.page = 1
        this.schedulerList.page = 1
        this.taskList.page = 1
        this.getAllProjects()
        this.getJobs()
        this.getTasks()
      }, 1000),
    )
  },
  watch: {
    datetime() {
      this.taskList.page = 1
      this.getTasks()
    },
  },
  methods: {
    handleRefresh() {
      this.getCases()
      this.getAllProjects()
      this.getJobs()
      this.getTasks()
    },
    async getType() {
      const type = await get('/v1/case/type', { showBackend: true })
      this.type.method = type.METHOD
      this.type.submit = type.SUBMIT
      this.type.deal = type.DEAL
      this.type.assert = type.ASSERT
      const projecType = await get('/v1/project/type', { type: 'TYPE' }, { showBackend: true })
      this.projecType = projecType
    },
    async getCases() {
      this.caseLoading = true
      try {
        const data = await get('/v1/user/case', {
          name: this.caseName,
          page: this.caseList.page
        }, { showBackend: true })
        this.caseTableData = data.data
        this.caseList.total = data.total
        this.caseList.page = data.page
        this.caseLoading = false
      } catch (error) {
        if (error.error_code !== 0) {
          this.caseTableData = []
        }
        this.caseLoading = false
      }
    },
    // 获取所有工程并传给table渲染
    async getAllProjects() {
      let res
      try {
        this.projectLoading = true
        res = await get('/v1/user/project', { name: this.projectName, page: this.projectList.page }, { showBackend: true })
        this.projectTableDate = res.data
        this.projectList.total = res.total
        this.projectList.page = res.page
        this.projectLoading = false
      } catch (e) {
        this.projectLoading = false
      }
    },
    async getJobs() {
      this.schedulerLoading = true
      try {
        const data = await get('/v1/user/scheduler', {
          name: this.projectName,
          page: this.schedulerList.page
        }, { showBackend: true })
        this.schedulerTableData = data.data
        this.schedulerList.total = data.total
        this.schedulerList.page = data.page
        this.schedulerLoading = false
      } catch (error) {
        if (error.error_code !== 0) {
          this.schedulerTableData = []
        }
        this.schedulerLoading = false
      }
    },
    async getTasks() {
      this.taskLoading = true
      if (this.datetime) {
        [this.startTime, this.endTime] = this.datetime
      } else {
        this.startTime = null
        this.endTime = null
      }
      try {
        const data = await get('/v1/user/task', {
          name: this.projectName,
          start: this.startTime,
          end: this.endTime,
          page: this.taskList.page,
          count: 10
        }, { showBackend: true })
        this.taskTableData = data.data
        this.taskList.total = data.total
        this.taskList.page = data.page
        this.taskLoading = false
      } catch (error) {
        if (error.error_code !== 0) {
          this.taskTableData = []
        }
        this.taskLoading = false
      }
    },
    handleCaseCurrentChange(val) {
      this.caseList.page = val
      this.getCases()
    },
    handleProjectCurrentChange(val) {
      this.projectList.page = val
      this.getAllProjects()
    },
    handleSchedulerCurrentChange(val) {
      this.schedulerList.page = val
      this.getJobs()
    },
    handleTaskCurrentChange(val) {
      this.taskList.page = val
      this.getTasks()
    }
  },
}
</script>

<style lang="scss" scoped>
.container {
  padding: 45px 30px 30px 30px;

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
  .caseList {
    .table{
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
  }

  .schedulerList {
    .table{

      .state {
        border-radius: 60px;
        margin: auto;
        width: 1.3em;
        height: 1.3em;
      }

      .running {
        background: #00C292;
      }

      .stoped {
        background: #E46A76;
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
</style>
