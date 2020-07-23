<template>
  <div class="container">
    <div class="title">
      <span>日志详情</span> <span class="back" @click="back">
      <i class="iconfont icon-fanhui"></i> 返回 </span>
      <el-button @click="handleDebug" class="debug" type="warning" plain  icon="el-icon-thumb">调试</el-button>
    </div>
    <el-divider></el-divider>
    <div class="wrap">
      <el-row>
        <el-col :lg="16" :md="20" :sm="24" :xs="24">
          <el-form label-position="left" inline class="demo-table-expand" :model="detail">
            <el-form-item label="任务编号">
              {{ detail.task_no }}
            </el-form-item>
            <el-form-item label="">
            </el-form-item>
            <el-form-item label="测试结果">
              <div v-if="detail.actual_result" style="color:#009d72;font-weight: 600;">成功</div>
              <div v-else style="color:#d62f40;font-weight: 600;">失败</div>
            </el-form-item>
            <el-form-item label="失败原因" v-if="!detail.actual_result">
              {{ detail.reason }}
            </el-form-item>
            <el-form-item label="" v-else>
            </el-form-item>
            <el-form-item label="测试时间">
              {{ detail.create_time/1000 | filterTimeYmdHms }}
            </el-form-item>
            <el-form-item label="测试人员">
              {{ detail.username }}
            </el-form-item>
          </el-form>
        </el-col>
      </el-row>
    </div>
    <el-divider content-position="left" @click="resultShow=!resultShow">接口返回</el-divider>
    <div class="wrap">
      <el-row v-show="resultShow">
        <el-col :lg="16" :md="20" :sm="24" :xs="24">
          <el-form label-position="left" inline class="demo-table-expand" :model="detail">
            <el-form-item label="状态码" v-if="detail.result.statusCode">
              <el-tag v-if="detail.result.statusCode>=400" type="danger">{{detail.result.statusCode}}</el-tag>
              <el-tag v-else type="success">{{detail.result.statusCode}}</el-tag>
            </el-form-item>
            <el-form-item label="状态码" v-else>
            </el-form-item>
            <el-form-item label="响应时间" v-if="detail.result.totalSeconds">
              {{ detail.result.totalSeconds }} 秒
            </el-form-item>
            <el-form-item label="响应时间" v-else>
            </el-form-item>
            <el-form-item label="响应头" v-if="detail.result.headers">
              <pre>{{ detail.result.headers }}</pre>
            </el-form-item>
            <el-form-item label="" v-if="detail.result.headers">
            </el-form-item>
            <el-form-item label="响应体" v-if="detail.result.body">
              <pre>{{ detail.result.body }}</pre>
            </el-form-item>
            <el-form-item label="响应体" v-else>
              {{ detail.result.text }}
            </el-form-item>
            <el-form-item label="">
            </el-form-item>
            <el-form-item label="cookies" v-if="detail.result.cookies">
              <pre>{{ detail.result.cookies }}</pre>
            </el-form-item>
            <el-form-item label="" v-if="detail.result.cookies">
            </el-form-item>
          </el-form>
        </el-col>
      </el-row>
    </div>
    <el-divider content-position="left" @click="projectShow=!projectShow">工程信息</el-divider>
    <div class="wrap">
      <el-row v-show="projectShow">
        <el-col :lg="16" :md="20" :sm="24" :xs="24">
          <el-form label-position="left" inline class="demo-table-expand" :model="detail">
            <el-form-item label="工程名称">
              <el-button type="primary" plain v-if="!detail.case_group_name" @click="toProjectConfig(detail.project_id, detail.name)">{{ detail.project_name }}</el-button>
              <div v-else>{{ detail.project_name }}</div>
            </el-form-item>
            <el-form-item label="工程类型">
              {{ detail.project_type_name }}
            </el-form-item>
          </el-form>
        </el-col>
      </el-row>
    </div>
    <el-divider content-position="left" @click="caseShow=!caseShow">用例信息</el-divider>
    <div class="wrap">
      <el-row v-show="caseShow">
        <el-col :lg="16" :md="20" :sm="24" :xs="24">
          <el-form label-position="left" inline class="demo-table-expand" :model="detail">
            <el-form-item label="用例名称">
              <el-button type="primary" plain v-if="detail.case_group_name" @click="toCaseList(detail.case_group, detail.name)">{{ detail.name }}</el-button>
              <div v-else>{{ detail.name }}</div>
            </el-form-item>
            <el-form-item label="用例分组" v-if="detail.case_group_name">
              {{ detail.case_group_name }}
            </el-form-item>
            <el-form-item label="" v-else>
            </el-form-item>
            <el-form-item label="请求方法">
              {{ detail.method_text }}
            </el-form-item>
            <el-form-item label="接口地址">
              {{ detail.url }}
            </el-form-item>
            <el-form-item label="后置处理">
              {{ detail.deal_text }}
            </el-form-item>
            <el-form-item label="处理语句" v-if="detail.condition">
              {{ detail.condition }}
            </el-form-item>
            <el-form-item label="" v-else>
            </el-form-item>
            <el-form-item label="提交方式">
              {{ detail.submit_text }}
            </el-form-item>
            <el-form-item label="用例描述" v-if="detail.info">
              {{ detail.info }}
            </el-form-item>
            <el-form-item label="" v-else>
            </el-form-item>
            <el-form-item label="断言方式">
              {{ detail.assertion_text }}
            </el-form-item>
            <el-form-item label="预期结果">
              {{ detail.expect }}
            </el-form-item>
            <el-form-item label="请求头">
              <pre>{{ detail.header }}</pre>
            </el-form-item>
            <el-form-item label="">
            </el-form-item>
            <el-form-item label="请求体">
              <pre>{{ detail.data }}</pre>
            </el-form-item>
          </el-form>
        </el-col>
      </el-row>
    </div>
    <!-- 調試框 -->
    <debug-case :case="debugCase" :drawerShow="drawer" :type="type" @closed="drawerClose" :ruleShow="ruleShow"></debug-case>
  </div>
</template>

<script>
import DebugCase from '../../../components/DebugCase'

export default {
  components: {
    DebugCase
  },
  props: {
    detail: {
      type: Object,
    },
    type: {
      type: Object,
    },
  },
  data() {
    return {
      debugCase: {
        url: '',
        method: '',
        data: '',
        header: '',
        submit: '',
        server: '',
        name: '',
      },
      drawer: false,
      resultShow: true,
      projectShow: true,
      caseShow: true,
      ruleShow: false,
    }
  },
  async mounted() {
    this.loading = true
    this.loading = false
  },
  methods: {
    back() {
      this.$emit('detailClose')
    },
    toProjectConfig(projectId, caseName) {
      this.$router.push({ path: '/project/config', query: { pid: projectId, case: caseName } })
    },
    toCaseList(groupId, caseName) {
      this.$router.push({ path: '/case/case/list', query: { group: groupId, case: caseName } })
    },
    handleDebug() {
      this.drawer = true
      this.debugCase.url = this.detail.url
      this.debugCase.method = this.detail.method
      if (this.detail.data) {
        this.debugCase.data = JSON.stringify(this.detail.data, null, 2)
      }
      if (this.detail.header) {
        this.debugCase.header = JSON.stringify(this.detail.header, null, 2)
      }
      this.debugCase.submit = this.detail.submit
      this.debugCase.name = this.detail.name
    },
    drawerClose() {
      this.drawer = false
    },
  },
}
</script>

<style lang="scss" scoped>
.el-divider--horizontal {
  margin: 0;
}

.container /deep/ .el-divider__text {
  cursor: pointer;
}

.container {
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
      position: relative;
    }

    .debug {
      position: absolute;
      right: 60px;
      top: 120px;
      z-index: 999;
    }
  }

  .wrap {
    padding: 20px;
  }

  .wrap /deep/ .demo-table-expand {
    font-size: 0;

    label {
      width: 100px;
      font-size: 15px;
      // font-weight: 600;
      color: #3963bc;
    }

    .el-form-item {
      margin-right: 0;
      margin-bottom: 0 !important;
      width: 50%;
      .el-form-item__content {
        width: 80%;
        font-size: 15px;
        word-break: break-all;
      }
    }
  }

}
</style>
