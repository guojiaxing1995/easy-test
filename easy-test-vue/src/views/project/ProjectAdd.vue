<template>
  <div class="container">
    <div class="title">新建分组信息</div>
    <el-row>
      <el-col :lg="16" :md="20" :sm="24" :xs="24">
        <div class="content">
          <el-form
            status-icon
            :rules="rules"
            :model="form"
            ref="form"
            label-position="right"
            label-width="100px"
            v-loading="loading"
            @submit.native.prevent
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
            <el-form-item label="工程类型">
              <el-radio-group v-model="form.type">
                <label v-for="(val,key) in type" :key="key" class="el-radio">
                  <el-radio :label="key">{{val}}</el-radio>
                </label>
              </el-radio-group>
              <el-tooltip effect="dark" placement="top-start">
                <div slot="content">关联类型是关联用例，修改原用例则工程中的用例同步修改。副本类型是将原用例复制一份，原用例与工程中用例修改互不影响</div>
                <div class="info"><l-icon name="Info2" color="#3963bc"></l-icon></div>
              </el-tooltip>
            </el-form-item>
            <el-form-item>
              <group-users
                @updateAuths="updateAuths"
                ref="groupUsers"
                title="分配人员"
              >
              </group-users>
            </el-form-item>
            <el-form-item class="submit">
              <el-button type="primary" @click="submitForm('form')">保 存</el-button>
              <el-button @click="resetForm('form')">重 置</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { post, get } from '@/lin/plugins/axios'
import GroupUsers from '../../components/GroupUsers'

export default {
  components: {
    GroupUsers,
  },
  inject: ['eventBus'],
  data() {
    return {
      groupUsers: [], // 子组件传递的用户组人员被选情况 需处理
      form: {
        name: null,
        info: null,
        server: null,
        header: null,
        type: '1',
        users: [],
      },
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
      loading: false,
      type: {},
    }
  },
  async created() {
    await this.getType()
  },
  methods: {
    async getType() {
      const type = await get('/v1/project/type', { type: 'TYPE' }, { showBackend: true })
      this.type = type
    },
    updateAuths(groupUsers) {
      this.groupUsers = groupUsers
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
    async submitForm(formName) {
      this.$refs[formName].validate(async valid => {
        // eslint-disable-line
        if (valid) {
          this.getAuths()
          let res
          try {
            this.loading = true
            const newForm = this.form
            newForm.type = parseInt(this.form.type, 10)
            res = await post('/v1/project', newForm, { showBackend: true })
          } catch (e) {
            this.loading = false
            console.log(e)
          }
          if (res.error_code === 0) {
            this.loading = false
            this.$message.success(`${res.msg}`)
            this.eventBus.$emit('addProject', true)
            this.$router.push('/project/list')
            this.resetForm('form')
          } else {
            this.loading = false
            this.$message.error(`${res.msg}`)
          }
        } else {
          this.$message.error('请将信息填写完整')
          return false
        }
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
      this.$refs.groupUsers.getGroupAuths()
    },
  },
}
</script>

<style lang="scss" scoped>
.container {
  .title {
    height: 59px;
    line-height: 59px;
    color: $parent-title-color;
    font-size: 16px;
    font-weight: 500;
    text-indent: 40px;
    border-bottom: 1px solid #dae1ec;
  }

  .content {
    margin-top: 10px;
    padding-left: 25px;
    padding-right: 40px;

  }
  .el-radio-group {
    position: relative;
  }
  .info {
    position: absolute;
    top: 5px;
    left: 180px;
  }

  .submit {
    float: left;
  }
}
</style>
