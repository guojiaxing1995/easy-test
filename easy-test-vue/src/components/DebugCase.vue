<template>
  <el-drawer
    title="用例调试"
    :with-header="false"
    :visible.sync="drawerVisible"
    direction="ltr"
    ustom-class="drawer"
    ref="drawer"
    size='31%'
    @close="close"
    >
    <div class="debug">
      <div class="title">{{debugForm.name}}</div>
      <div class="debugForm">
        <el-form :model="debugForm" :rules="rules" ref="debugForm">
          <el-form-item label="SERVER" label-width="80px" prop="server" v-if="ruleShow">
            <el-input v-model="debugForm.server" autocomplete="off" placeholder="请输入服务地址"></el-input>
          </el-form-item>
          <el-form-item label="SERVER" label-width="80px" v-else>
            <el-input v-model="debugForm.server" autocomplete="off" placeholder="请输入服务地址"></el-input>
          </el-form-item>
          <el-form-item label="URL" label-width="80px" prop="url">
            <el-input v-model="debugForm.url" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="请求方法" label-width="80px" prop="method">
            <el-radio-group v-model="debugForm.method">
              <label v-for="(val,key) in type.method" :key="key" class="el-radio">
                <el-radio :label="key">{{val}}</el-radio>
              </label>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="header" prop="header" label-width="80px">
            <el-input size="medium" type="textarea" :autosize="{ minRows: 3, maxRows: 5}" v-model="debugForm.header">
            </el-input>
          </el-form-item>
          <el-form-item label="data" prop="data" label-width="80px">
            <el-input size="medium" type="textarea" :autosize="{ minRows: 3, maxRows: 5}" v-model="debugForm.data">
            </el-input>
          </el-form-item>
          <el-form-item label="请求方式" label-width="80px" prop="submit">
            <el-radio-group v-model="debugForm.submit">
              <label v-for="(val,key) in type.submit" :key="key" class="el-radio">
                <el-radio :label="key">{{val}}</el-radio>
              </label>
            </el-radio-group>
          </el-form-item>
        </el-form>
      </div>
      <div class="result" v-loading='debugLoding'>
        <el-scrollbar style="height:100%" v-if="debugResult">
          <el-tag v-if="this.statusCode>=400"  effect="plain" type="danger" class="code">{{statusCode}}</el-tag>
          <el-tag v-else  effect="plain" type="success" class="code">{{statusCode}}</el-tag>
          <i class="el-icon-copy-document" @click="copyText" style="cursor:pointer"></i>
          <pre ref="result">{{debugResult}}</pre>
        </el-scrollbar>
      </div>
      <div class="debugButton">
        <el-button type="primary" @click="send" icon="el-icon-s-promotion" :loading='debugLoding'>{{ debugLoding ? 'sending...' : 'send' }}</el-button>
      </div>
    </div>
  </el-drawer>
</template>

<script>
import { post } from '@/lin/plugins/axios'

export default {
  // 用例信息，控制drawer是否显示，类型，控制是否进行server校验
  props: ['case', 'drawerShow', 'type', 'ruleShow'],
  data() {
    return {
      drawerVisible: this.drawerShow,
      statusCode: 200,
      debugLoding: false,
      debugResultDiv: false,
      debugResult: '',
      debugForm: {
        url: '',
        method: '',
        data: '',
        header: '',
        submit: '',
        server: '',
        name: '',
      },
      rules: {
        server: [
          { required: true, message: '请输入服务地址', trigger: 'blur' },
        ],
      },
    }
  },
  watch: {
    // 控制浮框显隐
    drawerShow(val) {
      this.drawerVisible = val
      this.debugForm.url = this.case.url
      this.debugForm.method = this.case.method.toString()
      this.debugForm.header = this.case.header
      this.debugForm.data = this.case.data
      this.debugForm.submit = this.case.submit.toString()
      this.debugForm.name = this.case.name
      this.debugResult = ''
    }
  },
  methods: {
    copyText() {
      const text = this.$refs.result.innerText
      if (text) {
        const input = document.createElement('input')
        input.value = text
        document.body.appendChild(input)
        input.select()
        document.execCommand('Copy')
        document.body.removeChild(input)
        this.$message({
          type: 'success',
          message: '复制文本成功',
        })
      }
    },
    send() {
      this.$refs.debugForm.validate(async valid => {
        if (valid) {
          this.debugResultDiv = false
          this.debugResult = ''
          this.debugLoding = true
          try {
            const result = await post('/v1/case/debug', {
              url: this.debugForm.server + this.debugForm.url,
              method: parseInt(this.debugForm.method, 10),
              submit: parseInt(this.debugForm.submit, 10),
              data: this.debugForm.data,
              header: this.debugForm.header,
            }, { showBackend: true })
            this.statusCode = result.statusCode
            if (result.body.constructor === String) {
              this.debugResult = result.body
            } else {
              this.debugResult = JSON.stringify(result.body, null, '\t')
            }
            this.debugResultDiv = true
            this.debugLoding = false
          } catch (error) {
            this.debugLoding = false
          }
        } else {
          return false
        }
      })
    },
    close() {
      this.$emit('closed')
    },
  },
}
</script>

<style lang="scss" scoped>
.debug {
  padding: 25px;
  height: 100vh;
  display: flex;
  flex-direction: column;

  .title {
    color: $parent-title-color;
    font-size: 18px;
    font-weight: 600;
  }

  .debugForm {
    margin-top: 20px;
  }

  .result {
    flex: 1;
    overflow: auto;

    .el-scrollbar__view {
      position: relative;
      i {
        position: absolute;
        right: 0;
        top: 5px;
      }
      .code {
        position: absolute;
        right: 30px;
        top: 0;
      }
    }

  }

  .debugButton {
    display: flex;
    button {
      flex: 1;
    }
  }

}
.el-drawer .ltr {
  left: 0;
  overflow: scroll;
}
</style>
