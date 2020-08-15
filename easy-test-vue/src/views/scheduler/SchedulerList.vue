<template>
  <div>
    <div class="container">
      <div class="header">
        <div>
          <label class="label ">工程名称</label>
          <el-select size="small" v-model="project" filterable clearable >
            <el-option
              v-for="item in projectData"
              :key="item.id"
              :label="item.name"
              :value="item.id">
            </el-option>
          </el-select>
        </div>
        <div class="search">
          <label class="label">维护人员</label>
          <el-cascader
            clearable
            filterable
            size="small"
            :show-all-levels="false"
            v-model="user_id"
            :options="users"
            :props="{ expandTrigger: 'hover' }"
          ></el-cascader>
        </div>
        <div class="search"><i class="el-icon-refresh" @click="handleRefresh" style="font-size:1.6em"></i></div>
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
          <el-table-column
            width="350"
            align="center"
            fixed="right"
            label="操作">
            <template slot-scope="scope">
              <el-button
                size="mini"
                style="margin:auto"
                type="success"
                plain
                :disabled="scope.row.state"
                v-auth="{ auth: '启动定时任务', type: 'disabled'}"
                @click="handleStart(scope.$index, scope.row)">启动</el-button>
              <el-button
                size="mini"
                type="danger"
                style="margin:auto"
                plain
                :disabled="!scope.row.state"
                v-auth="{ auth: '停止定时任务', type: 'disabled'}"
                @click="handleStop(scope.$index, scope.row)">停止</el-button>
              <el-button
                size="mini"
                type="warning"
                style="margin:auto"
                plain
                v-auth="{ auth: '编辑定时任务', type: 'disabled'}"
                @click="handleEdit(scope.$index, scope.row)">设置</el-button>
              <el-button
                size="mini"
                type="primary"
                style="margin:auto"
                plain
                v-auth="{ auth: '编辑定时任务', type: 'disabled'}"
                @click="handleCron(scope.$index, scope.row)">cron</el-button>
              <el-button
                size="mini"
                type="danger"
                style="margin:auto"
                v-auth="{ auth: '删除定时任务', type: 'disabled'}"
                @click="handleDelete(scope.$index, scope.row)">删除</el-button>
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
          :page-size=this.count
          :total="total">
        </el-pagination>
      </div>
    </div>
    <el-dialog
      :append-to-body="true"
      :visible.sync="dialogFormVisible"
      :before-close="handleClose"
      class="groupListInfoDialog"
    >
      <div style="margin-top:-25px;">
        <el-tabs v-model="activeTab" @tab-click="handleClick" v-loading="editLoading">
          <el-tab-pane label="基础信息" name="基础信息" style="margin-top:10px;">
            <el-form
              status-icon
              ref="formOne"
              label-width="120px"
              :model="form"
              label-position="labelPosition"
              :rules="rules"
              style="margin-left:-35px;margin-bottom:-35px;margin-top:15px;"
            >
              <el-form-item label="维护人员" prop="user">
                <el-cascader
                  style="width:60%"
                  clearable
                  filterable
                  :show-all-levels="false"
                  v-model="form.user"
                  :options="users"
                  :props="{ expandTrigger: 'hover' }"
                  ></el-cascader>
              </el-form-item>
              <el-form-item label="发送邮件" prop="sendEmail">
                <el-switch v-model="form.sendEmail"></el-switch>
              </el-form-item>
              <el-form-item label="邮件策略" v-if="form.sendEmail">
                <el-radio-group v-model="form.emailStrategy">
                  <label v-for="(val,key) in strategy" :key="key" class="el-radio">
                    <el-radio :label="key">{{val}}</el-radio>
                  </label>
                </el-radio-group>
              </el-form-item>
              <el-form-item label="抄送人员" prop="copyPerson">
                <el-cascader
                  style="width:60%"
                  clearable
                  filterable
                  :show-all-levels="false"
                  v-model="form.copyPerson"
                  :options="users"
                  :props="{ expandTrigger: 'hover', multiple: true }"
                  ></el-cascader>
              </el-form-item>
            </el-form>
          </el-tab-pane>
          <el-tab-pane label="cron表达式" name="cron表达式" style="margin-top:10px;">
            <el-form
              status-icon
              ref="formTwo"
              label-width="120px"
              :model="form"
              label-position="labelPosition"
              :rules="rules"
              style="margin-left:-35px;margin-bottom:-35px;margin-top:15px;"
            >
              <el-form-item label="cron" prop="cron" style="width:95%">
                <el-input v-model="form.cron" auto-complete="off">
                  <el-button slot="append" v-if="!showCronBox" icon="el-icon-arrow-down" @click="showCronBox = true" title="打开图形配置"></el-button>
                  <el-button slot="append" v-else icon="el-icon-arrow-up" @click="showCronBox = false" title="关闭图形配置"></el-button>
                </el-input>
                <div style="color: #E6A23C; font-size: 12px;">corn从左到右（用空格隔开）：秒 分 小时 月份中的日期 月份 星期中的日期 年份</div>
                <cron v-if="showCronBox" v-model="form.cron"></cron>
              </el-form-item>
            </el-form>
          </el-tab-pane>
        </el-tabs>
      </div>
      <div slot="footer" class="dialog-footer" style="padding-left:5px;">
        <el-button type="primary" @click="confirmEdit('formOne', 'formTwo')">确 定</el-button>
        <el-button @click="resetForm()">重 置</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import cron from '../../components/cron/cron'
import { get, put, _delete } from '@/lin/plugins/axios'

export default {
  components: {
    cron
  },
  inject: ['eventBus'],
  data() {
    return {
      loading: false,
      tableData: [],
      dialogFormVisible: false,
      page: 1,
      count: 10,
      pages: 1,
      total: 0,
      user_id: [null, null],
      users: [],
      projectData: [],
      project: null,
      // edit
      currentEditId: null,
      editLoading: false,
      showCronBox: false,
      activeTab: '基础信息',
      projects: [],
      form: {
        sendEmail: true,
        emailStrategy: '3',
        user: null,
        copyPerson: [],
        cron: null,
      },
      strategy: {
        1: '总是发送',
        2: '成功发送',
        3: '失败发送',
      },
      rules: {
        user: [{ required: true, message: '请选择维护人员', trigger: 'blur, change' }],
        cron: [{ required: true, message: '请填写cron表达式', trigger: 'blur, change' }],
      },
    }
  },
  activated() {
  },
  async created() {
    this.loading = true
    await this.getJobs()
    this.loading = false
    await this.geUsers()
    await this.getAllProjects()
    this.eventBus.$on('addScheduler', this.job)
  },
  beforeDestroy() {
    this.eventBus.$off('addScheduler', this.job)
  },
  methods: {
    handleClick(tab) {
      this.activeTab = tab.name
    },
    copyPersonDeal() {
      const copyPersonArray = []
      for (let index = 0; index < this.form.copyPerson.length; index++) {
        copyPersonArray.push(this.form.copyPerson[index][1])
      }
      return copyPersonArray.join(',')
    },
    async getAllProjects() {
      try {
        this.projectData = await get('/v1/project/auth', { showBackend: true })
      } catch (error) {
        console.log(error)
      }
    },
    async geUsers() {
      const allUsers = await get('/cms/user/userByInitials',
        {},
        { showBackend: true })
      this.groupDataDeal(allUsers)
    },
    groupDataDeal(allUsers) {
      for (const group of allUsers) {
        if (group.users.length > 0) {
          group.value = group.name
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
    // 监听新增更新用例是否成功
    async job(flag) {
      if (flag === true) {
        this.page = 1
        await this.getJobs()
      }
    },
    async handleRefresh() {
      this.page = 1
      await this.getJobs()
    },
    async getJobs() {
      this.loading = true
      try {
        const data = await get('/v1/scheduler/search', {
          project: this.project,
          user: this.user_id[1],
          count: this.count,
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
    async handleStart(index, row) {
      try {
        const res = await get('/v1/scheduler/start', {
          schedulerId: row.scheduler_id
        }, { showBackend: true })
        this.getJobs()
        this.$message({
          type: 'success',
          message: `${res.msg}`,
        })
      } catch (error) {
        if (error.error_code !== 0) {
          this.$message({
            type: 'error',
            message: `${error.msg}`,
          })
        }
        this.loading = false
      }
    },
    async handleStop(index, row) {
      try {
        const res = await get('/v1/scheduler/stop', {
          schedulerId: row.scheduler_id
        }, { showBackend: true })
        this.getJobs()
        this.$message({
          type: 'success',
          message: `${res.msg}`,
        })
      } catch (error) {
        if (error.error_code !== 0) {
          this.$message({
            type: 'error',
            message: `${error.msg}`,
          })
        }
        this.loading = false
      }
    },
    // 维护人数据处理
    getUserData(userId) {
      for (let i = 0; i < this.users.length; i++) {
        for (let c = 0; c < this.users[i].children.length; c++) {
          if (this.users[i].children[c].value === userId) {
            return [this.users[i].label, userId]
          }
        }
      }
    },
    // 抄送人数据处理
    getCopyPersonData(copyPerson) {
      const copy_person = []
      let copyPersonArray = []
      if (copyPerson !== null) {
        copyPersonArray = copyPerson.split(',')
      }
      for (let p = 0; p < copyPersonArray.length; p++) {
        for (let i = 0; i < this.users.length; i++) {
          for (let c = 0; c < this.users[i].children.length; c++) {
            if (this.users[i].children[c].value.toString() === copyPersonArray[p]) {
              copy_person.push([this.users[i].label, copyPersonArray[p]])
            }
          }
        }
      }
      return copy_person
    },
    handleEdit(index, row) {
      this.dialogFormVisible = true
      this.activeTab = '基础信息'
      this.currentEditId = row.id
      this.form.sendEmail = row.send_email
      this.form.user = this.getUserData(row.user)
      this.form.copyPerson = this.getCopyPersonData(row.copy_person)
      this.form.emailStrategy = row.email_strategy.toString()
      this.form.cron = row.cron
    },
    handleCron(index, row) {
      this.dialogFormVisible = true
      this.activeTab = 'cron表达式'
      this.currentEditId = row.id
      this.form.sendEmail = row.send_email
      this.form.user = this.getUserData(row.user)
      this.form.copyPerson = this.getCopyPersonData(row.copy_person)
      this.form.cron = row.cron
    },
    handleDelete(index, row) {
      this.$confirm('此操作将永久删除该定时任务, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }).then(async () => {
        const res = await _delete(`/v1/scheduler/remove/${row.id}`, { showBackend: true })
        if (res.error_code === 0) {
          this.page = 1
          this.getJobs()
          this.$message({
            type: 'success',
            message: `${res.msg}`,
          })
        }
      })
    },
    async confirmEdit(formOne, formTwo) {
      this.$refs[formOne].validate(async validOne => {
        this.$refs[formTwo].validate(async validTwo => {
          // eslint-disable-line
          if (validOne && validTwo) {
            let res
            try {
              this.editLoading = true
              res = await put(`/v1/scheduler/edit/${this.currentEditId}`, {
                sendEmail: this.form.sendEmail,
                emailStrategy: parseInt(this.form.emailStrategy, 10),
                user: this.form.user[1],
                copyPerson: this.copyPersonDeal(),
                cron: this.form.cron,
              }, { showBackend: true })
            } catch (e) {
              this.editLoading = false
              console.log(e)
            }
            if (res.error_code === 0) {
              this.editLoading = false
              this.dialogFormVisible = false
              this.$message.success(`${res.msg}`)
              this.getJobs()
            } else {
              this.loading = false
              this.$message.error(`${res.msg}`)
            }
          } else {
            this.$message.error('请将信息填写完整')
            return false
          }
        })
      })
    },
    resetForm() {
      for (let index = 0; index < this.tableData.length; index++) {
        if (this.tableData[index].id === this.currentEditId) {
          this.form.cron = this.tableData[index].cron
          this.form.sendEmail = this.tableData[index].send_email
          this.form.user = this.getUserData(this.tableData[index].user)
          this.form.copyPerson = this.getCopyPersonData(this.tableData[index].copy_person)
        }
      }
    },
    handleCurrentChange(val) {
      this.page = val
      this.getJobs()
    },
    // 弹框 右上角 X
    handleClose(done) {
      done()
    },
  },
  watch: {
    project() {
      this.page = 1
      this.getJobs()
    },
    user_id() {
      this.page = 1
      this.getJobs()
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
    display: flex;

    .search {
      margin-left: 30px;
    }

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
.groupListInfoDialog /deep/ .el-dialog__footer {
  text-align: left;
  padding-left: 30px;
}
.groupListInfoDialog /deep/ .el-dialog__header {
  padding-left: 30px;
}

.groupListInfoDialog /deep/ .el-dialog__body {
  padding: 30px;
}
</style>
