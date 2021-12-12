<template>
  <div class="container">
    <div class="title" v-if="editCase">
      <span>修改用例</span> <span class="back" @click="back"> <i class="iconfont icon-fanhui"></i> 返回 </span>
    </div>
    <el-divider></el-divider>
    <div class="wrap">
      <el-row>
        <el-col :lg="16" :md="20" :sm="24" :xs="24">
          <el-form :model="form" status-icon ref="form" label-width="100px" v-loading="loading" @submit.native.prevent class="form" :rules="rules">
            <el-form-item label="用例名称" prop="name">
              <el-input size="medium" v-model="form.name" placeholder="请填写用例名称" :disabled="Boolean(editCase)"></el-input>
            </el-form-item>
            <el-form-item label="所属分组" prop="caseGroup">
              <el-select v-model="form.caseGroup" filterable placeholder="请选用例分组" size="medium" :disabled="Boolean(editCase)">
                <el-option
                  v-for="item in allGroup"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id">
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="URL" prop="url">
              <el-input size="medium" v-model="form.url" placeholder="请填写URL">
                <template slot="prepend">http://server</template>
              </el-input>
            </el-form-item>
            <el-form-item label="请求方法">
              <el-radio-group v-model="form.method">
                <label v-for="(val,key) in type.method" :key="key" class="el-radio">
                  <el-radio :label="key">{{val}}</el-radio>
                </label>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="data" prop="data">
              <el-input size="medium" type="textarea" :autosize="{ minRows: 3, maxRows: 9}" placeholder="请输入请求体" v-model="form.data">
              </el-input>
            </el-form-item>
            <el-form-item label="header" prop="header">
              <el-input size="medium" type="textarea" :autosize="{ minRows: 3, maxRows: 9}" placeholder="请输入请求头" v-model="form.header">
              </el-input>
            </el-form-item>
            <el-form-item label="请求方式">
              <el-radio-group v-model="form.submit">
                <label v-for="(val,key) in type.submit" :key="key" class="el-radio">
                  <el-radio :label="key">{{val}}</el-radio>
                </label>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="后置处理">
              <el-radio-group v-model="form.deal" @change="resetDeal">
                <label v-for="(val,key) in type.deal" :key="key" class="el-radio">
                  <el-radio :label="key">{{val}}</el-radio>
                </label>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="处理语句" prop="condition">
              <codemirror v-show="form.deal==5" ref="dealConditionCode" v-model="form.condition"  :options="cmOptions"></codemirror>
              <el-input v-if="form.deal!=5" size="medium" type="textarea" :autosize="{ minRows: 1, maxRows: 3}" placeholder="请输入处理语句"
              v-model="form.condition" maxlength="50" show-word-limit></el-input>
            </el-form-item>
            <el-form-item label="断言方式">
              <el-radio-group v-model="form.assertion">
                <label v-for="(val,key) in type.assert" :key="key" class="el-radio">
                  <el-radio :label="key">{{val}}</el-radio>
                </label>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="期望结果" prop="expect">
              <el-input size="medium" type="textarea" :autosize="{ minRows: 2, maxRows: 6}" placeholder="请输入期望结果" v-model="form.expect" maxlength="500" show-word-limit>
              </el-input>
            </el-form-item>
            <el-form-item label="用例描述" prop="info">
              <el-input size="medium" type="textarea" :autosize="{ minRows: 3, maxRows: 9}" placeholder="请输入用例描述" v-model="form.info" maxlength="50" show-word-limit>
              </el-input>
            </el-form-item>
            <el-form-item class="submit">
              <el-button type="primary" @click="submitForm('form')">保 存</el-button>
              <el-button @click="resetForm('form')">重 置</el-button>
            </el-form-item>
          </el-form>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import { codemirror } from 'vue-codemirror'
import { get, post, put } from '@/lin/plugins/axios'
/* eslint-disable*/
import 'codemirror/mode/python/python.js'
import 'codemirror/theme/material-palenight.css'
import 'codemirror/addon/scroll/simplescrollbars.css'
import 'codemirror/addon/scroll/simplescrollbars'
import 'codemirror/addon/hint/show-hint';
import 'codemirror/addon/hint/show-hint.css';
import 'codemirror/addon/edit/matchbrackets'
import 'codemirror/addon/edit/closebrackets'
import 'codemirror/addon/display/autorefresh'
import 'codemirror/addon/comment/comment'

export default {
  components: {
    codemirror
  },
  inject: ['eventBus'],
  props: {
    editCase: {
      type: Object,
    },
  },
  data() {
    return {
      loading: false,
      allGroup: [],
      oldCase: {},
      cmOptions: {
        theme: 'material-palenight',
        mode: 'python',
        indentUnit: 4,
        indentWithTabs: true,
        autofocus: true,
        autoCloseBrackets: true,
        matchBrackets: true,
        styleActiveLine: true,
        smartIndent: true,
        lineNumbers: true,
        line: true,
        lineWrapping: true,
        autoRefresh: true,
        scrollbarStyle: 'overlay',
        hintOptions: {
          completeSingle: false
        },
      },
      form: {
        name: null,
        info: null,
        data: null,
        header: null,
        url: null,
        method: '1',
        submit: '1',
        deal: '1',
        condition: null,
        assertion: '1',
        expect: null,
        caseGroup: '',
        type: 1
      },
      rules: {
        name: [
          { required: true, message: '请输入用例名称', trigger: 'blur' },
          { max: 20, message: '用例名称需小于20字', trigger: 'blur' },
        ],
        caseGroup: [
          { required: true, message: '请选择用例分组', trigger: 'blur' },
        ],
        url: [
          { required: true, message: '请输入请求地址', trigger: 'blur' },
          { max: 500, message: '用例名称需小于500字', trigger: 'blur' }
        ],
      },
      type: {
        method: {},
        submit: {},
        deal: {},
        assert: {}
      },
    }
  },
  async mounted() {
    this.loading = true
    await this.getType()
    await this.getAllGroups()
    if (this.editCase) {
      this.form = this.editCase
      this.form.deal = this.editCase.deal.toString()
      this.form.method = this.editCase.method.toString()
      this.form.submit = this.editCase.submit.toString()
      this.form.assertion = this.editCase.assertion.toString()
      this.form.caseGroup = this.editCase.case_group
    }
    this.loading = false
    this.$nextTick(()=>{
      this.$refs.dealConditionCode.codemirror.on('keypress', () => {
        //编译器内容更改事件
        this.$refs.dealConditionCode.codemirror.showHint();
      }) 
   }) 
  },
  methods: {
    async resetDeal(val) {
      if (this.editCase) {
        const reult = await get('/v1/case', {id: this.editCase.id}, { showBackend: true })
        const [form] = reult.data
        if (val==form.deal){
          this.form.condition = form.condition
        }else{
          if (val==5){
            this.form.condition = '# 规则：自定义python函数，入参为2个字典，param1->接口返回数据  param2->当前运行工程的全局变量, 需要返回一个变量字典'
          }else{
            this.form.condition = ''
          }
        }
      }else {
        if (val==5){
          this.form.condition = '# 规则：自定义python函数，入参为2个字典，param1->接口返回数据  param2->当前运行工程的全局变量, 需要返回一个变量字典'
        }else{
          this.form.condition = ''
        }
      }
      setTimeout(() => {
        this.$refs.dealConditionCode.codemirror.refresh()
      },5)
    },
    async getAllGroups() {
      try {
        this.allGroup = await get('/v1/caseGroup/auth', { showBackend: true })
      } catch (e) {
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
    async create() {
      const newForm = this.form
      newForm.method = parseInt(this.form.method, 10)
      newForm.submit = parseInt(this.form.submit, 10)
      newForm.deal = parseInt(this.form.deal, 10)
      newForm.assertion = parseInt(this.form.assertion, 10)
      let res
      try {
        this.loading = true
        res = await post('/v1/case', newForm, { showBackend: true })
      } catch (e) {
        this.loading = false
      }
      if (res.error_code === 0) {
        this.loading = false
        this.$message.success(`${res.msg}`)
        this.eventBus.$emit('case', true)
        this.$router.push('/case/case/list')
      } else {
        this.loading = false
        this.$message.error(`${res.msg}`)
      }
    },
    async edit() {
      const newForm = this.form
      newForm.method = parseInt(this.form.method, 10)
      newForm.submit = parseInt(this.form.submit, 10)
      newForm.deal = parseInt(this.form.deal, 10)
      newForm.assertion = parseInt(this.form.assertion, 10)
      let res
      try {
        this.loading = true
        res = await put(`/v1/case/${newForm.id}`, newForm, { showBackend: true })
      } catch (e) {
        this.loading = false
      }
      if (res.error_code === 0) {
        this.loading = false
        this.$message.success(`${res.msg}`)
        this.eventBus.$emit('case', true)
        this.$emit('editClose')
      } else {
        this.loading = false
        this.$message.error(`${res.msg}`)
      }
    },
    async submitForm(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          if (this.editCase) {
            this.edit()
          } else {
            this.create()
          }
        } else {
          return false
        }
      })
    },
    // 重置表单
    async resetForm(formName) {
      // 如果是编辑用例则重置为编辑初始值
      if (this.editCase) {
        this.loading = true
        const reult = await get('/v1/case', {
          id: this.editCase.id,
        }, { showBackend: true })
        const [form] = reult.data
        this.form = form
        this.form.deal = form.deal.toString()
        this.form.method = form.method.toString()
        this.form.submit = form.submit.toString()
        this.form.assertion = form.assertion.toString()
        this.loading = false
      } else {
        this.$refs[formName].resetFields()
        this.form.submit = '1'
        this.form.deal = '1'
        this.form.assertion = '1'
        this.form.method = '1'
      }
    },
    back() {
      this.$emit('editClose')
    },
  },
}
</script>

<style lang="scss" scoped>
.el-divider--horizontal {
  margin: 0;
}

.container {
  .vue-codemirror {
    line-height: 150%;
  }
  .title {
    height: 59px;
    line-height: 59px;
    color: $parent-title-color;
    font-size: 16px;
    font-weight: 500;
    text-indent: 40px;

    .back {
      float: right;
      margin-right: 40px;
      cursor: pointer;
    }
  }

  .form /deep/ .el-input-group__prepend {
    background: #f5f7fa;
    border: 1px solid #3963bc;
    color: #3963bc;
  }

  .wrap {
    padding: 20px;
  }

  .submit {
    float: left;
  }
}
</style>
