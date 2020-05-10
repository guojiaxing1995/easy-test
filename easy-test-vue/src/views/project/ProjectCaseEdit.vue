<template>
  <div class="caseEdit">
    <el-form :model="element" status-icon ref="form" label-width="80px" v-loading="loading" @submit.native.prevent class="form" :rules="rules">
      <el-form-item label="URL" prop="url">
        <el-input size="mini" v-model="element.url" placeholder="请填写url"></el-input>
      </el-form-item>
      <el-form-item label="请求方法"  prop="method">
        <el-radio-group v-model="element.method" size="mini">
          <label v-for="(val,key) in type.method" :key="key" class="el-radio">
            <el-radio size="mini" :label="key">{{val}}</el-radio>
          </label>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="data" prop="data">
        <el-input size="mini" type="textarea" :autosize="{ minRows: 3, maxRows: 9}" placeholder="请输入请求体" v-model="element.data">
        </el-input>
      </el-form-item>
      <el-form-item label="header" prop="header">
        <el-input size="mini" type="textarea" :autosize="{ minRows: 3, maxRows: 9}" placeholder="请输入请求头" v-model="element.header">
        </el-input>
      </el-form-item>
      <el-form-item label="请求方式" prop="submit">
        <el-radio-group v-model="element.submit" size="mini">
          <label v-for="(val,key) in type.submit" :key="key" class="el-radio">
            <el-radio :label="key">{{val}}</el-radio>
          </label>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="后置处理" prop="deal">
        <el-select size="mini" v-model="element.deal">
          <el-option
            v-for="(val,key) in type.deal"
            :key="key"
            :label="val"
            :value="key">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="处理语句" prop="condition">
        <el-input size="mini" type="textarea" :autosize="{ minRows: 1, maxRows: 3}" placeholder="请输入处理语句" v-model="element.condition" maxlength="50" show-word-limit>
        </el-input>
      </el-form-item>
      <el-form-item label="断言方式" prop="assertion">
        <el-select size="mini" v-model="element.assertion">
          <el-option
            v-for="(val,key) in type.assert"
            :key="key"
            :label="val"
            :value="key">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="期望结果" prop="expect">
        <el-input size="mini" type="textarea" :autosize="{ minRows: 1, maxRows: 3}" placeholder="请输入期望结果" v-model="element.expect" maxlength="500" show-word-limit>
        </el-input>
      </el-form-item>
      <el-form-item class="submit">
        <el-button type="primary" @click="submitForm('form')" size="mini">保 存</el-button>
        <el-button type="info" size="mini" @click="synchro">同 步</el-button>
        <el-button @click="resetForm()" size="mini">重 置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { get, put } from '@/lin/plugins/axios'

export default {
  props: {
    caseDate: {
      type: Object,
    },
    caseTypeCode: {
      type: Object,
    },
    projectId: {
      type: Number,
    },
  },
  data() {
    return {
      loading: false,
      element: {},
      type: [],
      rules: {
        url: [
          { required: true, message: '请输入请求地址', trigger: 'blur' },
          { max: 500, message: '用例名称需小于500字', trigger: 'blur' }
        ],
      },
    }
  },
  async mounted() {
    this.dataDeal()
    this.type = this.caseTypeCode
  },
  methods: {
    dataDeal() {
      this.element = JSON.parse(JSON.stringify(this.caseDate))
      this.element.submit = this.caseDate.submit.toString()
      this.element.method = this.caseDate.method.toString()
      this.element.deal = this.caseDate.deal.toString()
      this.element.assertion = this.caseDate.assertion.toString()
    },
    // 重置表单
    async resetForm() {
      this.dataDeal()
    },
    async submitForm(formName) {
      this.$refs[formName].validate(async valid => {
        if (valid) {
          try {
            this.loading = true
            const res = await put('/v1/project/copyConfig', {
              id: this.element.id,
              projectId: this.projectId,
              url: this.element.url,
              method: parseInt(this.element.method, 10),
              submit: parseInt(this.element.submit, 10),
              header: this.element.header,
              data: this.element.data,
              deal: parseInt(this.element.deal, 10),
              condition: this.element.condition,
              expect: this.element.expect,
              assertion: parseInt(this.element.assertion, 10)
            }, { showBackend: true })
            this.loading = false
            if (res.error_code === 0) {
              this.$message.success(`${res.msg}`)
            } else {
              this.$message.error(`${res.msg}`)
            }
          } catch (error) {
            this.loading = false
          }
        } else {
          return false
        }
      })
    },
    async synchro() {
      try {
        this.loading = true
        const data = await get('/v1/case', {
          id: this.element.case_id
        }, { showBackend: true })
        this.element.url = data.data[0].url
        this.element.method = data.data[0].method.toString()
        this.element.data = data.data[0].data
        this.element.header = data.data[0].header
        this.element.submit = data.data[0].submit.toString()
        this.element.deal = data.data[0].deal.toString()
        this.element.condition = data.data[0].condition
        this.element.assertion = data.data[0].assertion.toString()
        this.element.expect = data.data[0].expect
        this.loading = false
        this.$message.success('成功同步用例数据')
      } catch (error) {
        this.loading = false
        this.$message.error('同步失败目标用例已被删除')
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.caseEdit {
  background: rgba(236, 245, 255, 0.3);
  padding: 0 2px;
  .el-form-item {
    margin-bottom: 0px !important;
  }
}
</style>
