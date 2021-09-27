<template>
  <div class="container">
    <div class="header">
      <div class="title">工程信息</div>
      <div class="search">
        <el-input placeholder="请输入工程名称查询" v-model="name" clearable size="small"></el-input>
      </div>
    </div>
    <div class="table">
      <el-table
        :data="tableData"
        stripe
        v-loading="loading"
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
          min-width="290">
        </el-table-column>
        <el-table-column
          label="类型"
          fixed="right"
          align="center"
          width="70">
          <template slot-scope="scope">
            <div :key="key" v-for="(val,key) in projecType">
              <div v-if="scope.row.type === parseInt(key)">{{val}}</div>
            </div>
          </template>
        </el-table-column>
        <el-table-column
          width="240"
          align="center"
          fixed="right"
          label="操作">
          <template slot-scope="scope">
            <el-button
              size="mini"
              type="primary"
              plain
              style="margin:auto"
              @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
            <el-button
              size="mini"
              type="primary"
              plain
              style="margin:auto"
              @click="handleParam(scope.$index, scope.row)">运行参数</el-button>
            <el-button
              v-auth="{ auth: '删除工程', type: 'disabled'}"
              size="mini"
              type="danger"
              plain
              style="margin:auto"
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
          :page-size=10
          :total="total">
        </el-pagination>
      </div>
    <el-dialog
      :append-to-body="true"
      :visible.sync="dialogFormVisible"
      :before-close="handleClose"
      top="5vh"
      class="groupListInfoDialog"
    >
      <div style="margin-top:-25px;">
        <el-tabs v-model="activeTab" @tab-click="handleClick" v-loading="editLoading">
          <el-tab-pane label="修改信息" name="修改信息" style="margin-top:10px;">
            <el-form
              status-icon
              v-if="dialogFormVisible"
              ref="form"
              label-width="120px"
              :model="form"
              label-position="labelPosition"
              :rules="rules"
              style="margin-left:-35px;margin-bottom:-35px;margin-top:15px;"
            >
              <el-form-item label="工程名称" prop="name">
                <el-input size="medium" clearable v-model="form.name"></el-input>
              </el-form-item>
              <el-form-item label="服务地址" prop="server">
                <el-input size="medium" clearable v-model="form.server"></el-input>
              </el-form-item>
              <el-form-item label="header" prop="header">
                <el-input size="medium" type="textarea" :autosize="{ minRows: 3, maxRows: 9}" placeholder="请输入公共请求头" v-model="form.header">
                </el-input>
              </el-form-item>
              <el-form-item label="工程描述" prop="info">
                <el-input size="medium" clearable v-model="form.info"></el-input>
              </el-form-item>
              <el-form-item label="工程类型" prop="type">
                <el-radio-group v-model="form.type" aria-disabled="">
                  <label v-for="(val,key) in projecType" :key="key" class="el-radio">
                    <el-radio disabled :label="key">{{val}}</el-radio>
                  </label>
                </el-radio-group>
              </el-form-item>
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
          <el-tab-pane label="配置权限" name="配置权限" style="margin-top:10px;">
            <group-users
              v-if="dialogFormVisible"
              :groupId="id"
              :authType="type"
              ref="groupAuths"
              @updateAuths="updateAuths"
              style="margin-right:-30px;margin-left:-25px;margin-bottom:-10px;"
            >
            </group-users>
          </el-tab-pane>
        </el-tabs>
      </div>
      <div slot="footer" class="dialog-footer" style="padding-left:5px;">
        <el-button type="primary" @click="confirmEdit('form')">确 定</el-button>
        <el-button @click="resetForm('form')">重 置</el-button>
      </div>
    </el-dialog>
    <el-dialog
      :visible.sync="userParam.dialogVisible"
      :close-on-click-modal="false"
      top="15vh"
      width="35%"
      title="工程变量"
      v-loading="userParam.loading"
      center
    >
      <div style="margin-top:-25px;">
        <el-form
          status-icon
          v-if="userParam.dialogVisible"
          ref="userParam"
          label-width="80px"
          :model="userParam"
          style="margin-bottom:-15px;margin-top:15px;"
        >
          <el-input size="medium" type="textarea"  clearable v-model="userParam.param" :autosize="{ minRows: 12, maxRows: 16}" placeholder="请输入json格式"></el-input>
        </el-form>
      </div>
      <div slot="footer" class="dialog-footer" style="text-align: center;">
        <el-button type="primary" @click="confirmSetParam()" style="margin-right:20px">确 定</el-button>
        <el-button @click="resetParam('userParam')" style="margin-left:20px">重 置</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import Utils from 'lin/utils/util'
import { get, put, post, _delete } from '@/lin/plugins/axios'
import GroupUsers from '../../components/GroupUsers'

export default {
  components: {
    GroupUsers,
  },
  inject: ['eventBus'],
  data() {
    return {
      id: 0, // 分组id
      type: 2, // 类型为工程
      tableData: [], // 表格数据
      name: '',
      dialogFormVisible: false, // 是否弹窗
      labelPosition: 'right', // 设置label位置
      form: {
        // 表单信息
        name: null,
        server: null,
        header: null,
        info: null,
        // 授权人与
        users: [],
        type: '1',
        sendEmail: true,
        emailStrategy: '3',
        // 维护人
        user: null,
        copyPerson: [],
      },
      // 人员树
      users: [],
      projecType: {},
      groupUsers: [], // 拥有的分组权限
      loading: false,
      editLoading: false,
      strategy: {
        1: '总是发送',
        2: '成功发送',
        3: '失败发送',
      },
      total: 0,
      page: 1,
      activeTab: '修改信息', // tab 标题
      rules: {
        server: [
          { required: true, message: '请输入服务地址', trigger: 'blur' },
          { max: 60, message: '服务地址需小于60字', trigger: 'blur' },
        ],
        user: [{ required: true, message: '请选择维护人员', trigger: 'blur, change' }],
        name: [
          { required: true, message: '请输入工程名称', trigger: 'blur' },
          { max: 20, message: '工程名称需小于20字', trigger: 'blur' },
        ],
        info: [],
      },
      userParam: {
        loading: false,
        param: null,
        dialogVisible: false,
        id: null
      }
    }
  },
  methods: {
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
    copyPersonDeal() {
      const copyPersonArray = []
      for (let index = 0; index < this.form.copyPerson.length; index++) {
        copyPersonArray.push(this.form.copyPerson[index][1])
      }
      return copyPersonArray.join(',')
    },
    async getType() {
      const type = await get('/v1/project/type', { type: 'TYPE' }, { showBackend: true })
      this.projecType = type
    },
    // 获取所有工程并传给table渲染
    async getAllProjects() {
      let res
      try {
        this.loading = true
        res = await get('/v1/project/list', { page: this.page, name: this.name }, { showBackend: true })
        this.tableData = res.data
        this.total = res.total
        this.page = res.page
        this.pages = res.pages
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    // 获取所有授权用户的id放入数组
    getAuths() {
      const allAuthsUsers = []
      for (const group of this.groupUsers) {
        if (typeof group.choose !== 'undefined') {
          allAuthsUsers.push(...group.choose)
        }
      }
      this.form.users = allAuthsUsers
    },
    async confirmEdit(form) {
      this.$refs[form].validate(async valid => {
        if (valid) {
          if (this.groupUsers === []) {
            this.$message.warning('请等待数据加载完重试')
            return
          }
          this.editLoading = true
          this.getAuths()
          let res
          try {
            res = await put(`/v1/project/${this.id}`, {
              name: this.form.name,
              server: this.form.server,
              header: this.form.header,
              info: this.form.info,
              users: this.form.users,
              type: this.form.type,
              sendEmail: this.form.sendEmail,
              emailStrategy: parseInt(this.form.emailStrategy, 10),
              user: this.form.user[1],
              copyPerson: this.copyPersonDeal(),
            }, { showBackend: true })
            if (res.error_code === 0) {
              this.$message.success(`${res.msg}`)
              this.dialogFormVisible = false
              await this.getAllProjects()
            } else {
              this.$message.error(`${res.msg}`)
            }
            this.editLoading = false
          } catch (error) {
            this.editLoading = false
          }
        } else {
          this.$message.error('请将信息填写完整')
          return false
        }
      })
    },
    async confirmSetParam() {
      let res
      this.userParam.loading = true
      try {
        res = await post('/v1/project/userParam', {
          userParam: this.userParam.param,
          id: this.userParam.id,
        }, { showBackend: true })
        if (res.error_code === 0) {
          this.$message.success(`${res.msg}`)
          this.userParam.dialogVisible = false
        } else {
          this.$message.error(`${res.msg}`)
        }
        this.userParam.loading = false
      } catch (error) {
        this.userParam.loading = false
      }
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
      this.$refs.userParam.getGroupAuths()
    },
    resetParam(formName) {
      this.$refs[formName].resetFields()
      this.handleParam(0, this.userParam)
    },
    // 获取所拥有的权限并渲染  由子组件提供
    handleEdit(index, val) {
      this.id = val.id
      this.form.name = val.name
      this.form.info = val.info
      this.form.server = val.server
      this.form.header = val.header
      this.form.type = val.type.toString()
      this.form.emailStrategy = val.email_strategy.toString()
      this.form.sendEmail = val.send_email
      this.form.user = this.getUserData(val.user)
      this.form.copyPerson = this.getCopyPersonData(val.copy_person)
      this.dialogFormVisible = true
    },
    async handleParam(index, val) {
      let res
      this.userParam.dialogVisible = true
      this.userParam.id = val.id
      try {
        this.userParam.loading = true
        res = await get('/v1/project/userParam', { id: val.id }, { showBackend: true })
        if (res.param) {
          if (res.param.constructor === String) {
            this.userParam.param = res.param
          } else {
            this.userParam.param = JSON.stringify(res.param, null, '\t')
          }
        } else {
          this.userParam.param = null
        }
        this.userParam.loading = false
      } catch (e) {
        this.userParam.loading = false
        console.log(e)
      }
    },
    handleDelete(index, val) {
      let res
      this.$confirm('此操作将永久删除该工程, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }).then(async () => {
        try {
          this.loading = true
          res = await _delete(`/v1/project/${val.id}`, { showBackend: true })
        } catch (e) {
          this.loading = false
          console.log(e)
        }
        if (res.error_code === 0) {
          await this.getAllProjects()
          this.$message({
            type: 'success',
            message: `${res.msg}`,
          })
        } else {
          this.loading = false
          this.$message({
            type: 'error',
            message: `${res.msg}`,
          })
        }
      })
    },
    handleCurrentChange(val) {
      this.page = val
      this.getAllProjects()
    },
    // 获取拥有的权限
    updateAuths(groupUsers) {
      this.groupUsers = groupUsers
    },
    // 弹框 右上角 X
    handleClose(done) {
      done()
    },
    // 切换tab栏
    handleClick(tab) {
      this.activeTab = tab.name
    },
    // 监听分组是否成功
    async addProject(flag) {
      if (flag === true) {
        await this.getAllProjects()
      }
    },
  },
  async created() {
    await this.getType()
    await this.getAllProjects()
    await this.geUsers()
    // 监听分组是否成功
    this.eventBus.$on('addProject', this.addProject)
    if (this.$route.query.pname) {
      this.name = this.$route.query.pname
    }
    // 节流搜素
    this.$watch(
      'name',
      Utils.debounce(() => {
        this.page = 1
        this.getAllProjects()
      }, 1000),
    )
  },
  beforeDestroy() {
    this.eventBus.$off('addProject', this.addProject)
  },
}
</script>

<style lang="scss" scoped>
.container {
  padding: 15px 30px;

  .header{
    display: flex;
    height: 65px;
    line-height: 65px;
    justify-content: space-between;

    .title {
      color: $parent-title-color;
      font-size: 18px;
      font-weight: 500;
    }
    .search {
      width: 15%;
    }

  }

  .table {
    margin-top: 15px;
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
