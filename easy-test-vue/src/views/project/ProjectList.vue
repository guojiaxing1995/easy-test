<template>
  <div class="container">
    <div class="title">
      工程信息
      <el-select size="small" v-model="selectProject" filterable placeholder="请输入工程名称查询" class="select" clearable>
        <el-option
          v-for="item in selectData"
          :key="item.id"
          :label="item.name"
          :value="item.name">
        </el-option>
      </el-select>
    </div>
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
        fixed
        prop="server"
        label="服务地址"
        :show-overflow-tooltip="true"
        min-width="200">
      </el-table-column>
      <el-table-column
        label="类型"
        align="center"
        width="70">
        <template slot-scope="scope">
          <div :key="key" v-for="(val,key) in projecType">
            <div v-show="scope.row.type === parseInt(key)" style="margin:auto">{{val}}</div>
          </div>
        </template>
      </el-table-column>
      <el-table-column
        fixed
        prop="info"
        label="描述"
        :show-overflow-tooltip="true"
        min-width="350">
      </el-table-column>
      <el-table-column
        width="180"
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
            v-auth="{ auth: '删除工程', type: 'disabled'}"
            size="mini"
            type="danger"
            plain
            style="margin:auto"
            @click="handleDelete(scope.$index, scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog
      :append-to-body="true"
      :visible.sync="dialogFormVisible"
      :before-close="handleClose"
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
        <el-button type="primary" @click="confirmEdit">确 定</el-button>
        <el-button @click="resetForm('form')">重 置</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { get, put, _delete } from '@/lin/plugins/axios'
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
      selectData: [], // 拉框数据
      selectProject: '',
      dialogFormVisible: false, // 是否弹窗
      labelPosition: 'right', // 设置label位置
      form: {
        // 表单信息
        name: null,
        server: null,
        header: null,
        info: null,
        users: [],
        type: '1',
      },
      projecType: {},
      groupUsers: [], // 拥有的分组权限
      loading: false,
      editLoading: false,
      activeTab: '修改信息', // tab 标题
      rules: {
        server: [
          { required: true, message: '请输入服务地址', trigger: 'blur' },
          { max: 60, message: '服务地址需小于60字', trigger: 'blur' },
        ],
        name: [
          { required: true, message: '请输入工程名称', trigger: 'blur' },
          { max: 20, message: '工程名称需小于20字', trigger: 'blur' },
        ],
        info: [],
      },
    }
  },
  watch: {
    selectProject() {
      if (this.selectProject === '') {
        this.tableData = this.selectData
      } else {
        for (const project of this.selectData) {
          if (project.name === this.selectProject) {
            this.tableData = []
            this.tableData.push(project)
          }
        }
      }
    },
  },
  methods: {
    async getType() {
      const type = await get('/v1/project/type', { type: 'TYPE' }, { showBackend: true })
      this.projecType = type
    },
    // 获取所有分组并传给table渲染
    async getAllProjects() {
      try {
        this.loading = true
        this.tableData = await get('/v1/project', { showBackend: true })
        this.selectData = this.tableData
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
    async confirmEdit() {
      // 修改分组信息
      if (this.form.name === '') {
        this.$message.warning('请将信息填写完整')
        return
      }
      if (this.groupUsers === []) {
        this.$message.warning('请等待数据加载完重试')
        return
      }
      this.editLoading = true
      this.getAuths()
      let res
      try {
        res = await put(`/v1/project/${this.id}`, this.form, { showBackend: true })
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
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
      this.$refs.groupAuths.getGroupAuths()
    },
    // 获取所拥有的权限并渲染  由子组件提供
    handleEdit(index, val) {
      this.id = val.id
      this.form.name = val.name
      this.form.info = val.info
      this.form.server = val.server
      this.form.header = val.header
      this.form.type = val.type.toString()
      this.dialogFormVisible = true
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
    // 监听分组是否成功
    this.eventBus.$on('addProject', this.addProject)
  },
  beforeDestroy() {
    this.eventBus.$off('addProject', this.addProject)
  },
}
</script>

<style lang="scss" scoped>
.container {
  padding: 0 30px;

  .title {
    height: 59px;
    line-height: 59px;
    color: $parent-title-color;
    font-size: 16px;
    font-weight: 500;
    position: relative;
    width: 100%;
    .select {
      position: absolute;
      right: 0;
    }
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
