<template>
  <div class="container">
    <div class="title">新建任务信息</div>
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
            <el-form-item label="工程名称" prop="project">
              <el-select v-model="form.project" filterable clearable style="width:50%">
                <el-option
                  v-for="item in projectData"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id">
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="维护人员" prop="user">
              <el-cascader
                style="width:50%"
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
                style="width:50%"
                clearable
                filterable
                :show-all-levels="false"
                v-model="form.copyPerson"
                :options="users"
                :props="{ expandTrigger: 'hover', multiple: true }"
                ></el-cascader>
            </el-form-item>
            <el-form-item label="cron" prop="cron" style="width:90%">
              <el-input v-model="form.cron" auto-complete="off">
                <el-button slot="append" v-if="!showCronBox" icon="el-icon-arrow-down" @click="showCronBox = true" title="打开图形配置"></el-button>
                <el-button slot="append" v-else icon="el-icon-arrow-up" @click="showCronBox = false" title="关闭图形配置"></el-button>
              </el-input>
              <div style="color: #E6A23C; font-size: 12px;">corn从左到右（用空格隔开）：秒 分 小时 月份中的日期 月份 星期中的日期 年份</div>
              <cron v-if="showCronBox" v-model="form.cron"></cron>
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
import cron from '../../components/cron/cron'
import { get, post } from '@/lin/plugins/axios'

export default {
  components: {
    cron
  },
  inject: ['eventBus'],
  data() {
    return {
      projects: [],
      showCronBox: false,
      form: {
        project: null,
        sendEmail: true,
        emailStrategy: '3',
        user: null,
        copyPerson: [],
        cron: null,
      },
      users: [],
      projectData: [],
      strategy: {
        1: '总是发送',
        2: '成功发送',
        3: '失败发送',
      },
      rules: {
        project: [{ required: true, message: '请选择工程', trigger: 'blur, change' }],
        user: [{ required: true, message: '请选择维护人员', trigger: 'blur, change' }],
        cron: [{ required: true, message: '请填写cron表达式', trigger: 'blur, change' }],
      },
      loading: false,
    }
  },
  methods: {
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
    async getAllProjects() {
      try {
        this.projectData = await get('/v1/project/auth', { showBackend: true })
      } catch (error) {
        console.log(error)
      }
    },
    async submitForm(formName) {
      this.$refs[formName].validate(async valid => {
        // eslint-disable-line
        if (valid) {
          let res
          try {
            this.loading = true
            res = await post('/v1/scheduler/add', {
              project: this.form.project,
              sendEmail: this.form.sendEmail,
              emailStrategy: parseInt(this.form.emailStrategy, 10),
              user: this.form.user[1],
              copyPerson: this.copyPersonDeal(),
              cron: this.form.cron,
            }, { showBackend: true })
          } catch (e) {
            this.loading = false
            console.log(e)
          }
          if (res.error_code === 0) {
            this.loading = false
            this.$message.success(`${res.msg}`)
            this.eventBus.$emit('addScheduler', true)
            this.$router.push('/scheduler/list')
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
    },
  },
  async created() {
    await this.getAllProjects()
    await this.geUsers()
  }
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

  .submit {
    float: left;
  }
}
</style>
