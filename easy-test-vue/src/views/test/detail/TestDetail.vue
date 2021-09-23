<template>
  <div>
    <div class="container" v-loading="loading">
      <el-row :gutter="30" style="margin-bottom:30px">
        <el-col :span="6">
          <label class="label" >测试工程</label>
          <el-select v-model="project" filterable placeholder="请选择工程" size="small" style="width:70%">
            <el-option
              v-for="item in projectList"
              :key="item.id"
              :label="item.name"
              :value="item.id">
            </el-option>
          </el-select>
        </el-col>
        <el-col :span="6">
          <label class="label" >记录编号</label>
          <el-select v-model="task" filterable placeholder="请选择运行记录" size="small" style="width:70%">
            <el-option
              v-for="item in taskList"
              :key="item.task_no"
              :label="item.task_no"
              :value="item.task_no">
            </el-option>
          </el-select>
        </el-col>
        <el-col :span="6">
          <div style="height: 32px;line-height: 32px"><label class="label" >测试时间</label>{{ currentTask.time/1000 | filterTimeYmdHms }}</div>
        </el-col>
        <el-col :span="4">
          <div style="height: 32px;line-height: 32px"><label class="label" >测试人员</label>{{ currentTask.user }}</div>
        </el-col>
        <el-col :span="2">
          <l-icon name="HTMLreport" height="1.9em" width="1.9em" style="cursor: pointer" @click="reportDownload" v-if="!this.currentProject.running"
          v-auth="{ auth: '报告下载', type: 'disabled'}"></l-icon>
        </el-col>
      </el-row>
      <el-row :gutter="30" style="margin-bottom:30px">
        <el-col :span="6">
          <div style="text-align: center;height: 20vh;" class="box" v-if="currentProject.running">
            <el-progress type="circle" :percentage="currentProject.progress" :width="160" style="margin-top:20px"></el-progress>
            <div style="position: absolute;top: 0;margin-left: 10px;margin-top: 10px;" class="label">运行进度</div>
          </div>
          <div id="result-circle" style="height: 20vh;" class="box" v-show="!currentProject.running">
          </div>
        </el-col>
        <el-col :span="6">
          <div style="height: 20vh;" class="box">
            <div style="height: 100px;line-height: 100px">
              <span style="margin-left:10px" class="label">总计</span><span style="font-size:30px;margin-left:10px;color: #3963BC">{{ currentTask.total }}</span>
            </div>
            <div class="result">
              <div style="width:50%"><span class="label">成功</span><span style="font-size:30px;color: #00C292">{{ currentTask.success }}</span></div>
              <div style="width:50%"><span class="label">失败</span><span style="font-size:30px;color: #E46A76">{{ currentTask.fail }}</span></div>
            </div>
          </div>
        </el-col>
        <el-col :span="12">
          <div style="height: 20vh;width:100%" class="box" id="result-line"></div>
        </el-col>
      </el-row>
      <el-row :gutter="30">
        <el-col :span="16">
          <!-- 结果详情 -->
          <div style="height: 52vh;" class="box">
            <div class="logDetail" v-show="detail.id">
              <div class="wrap">
                <el-row>
                  <el-col :lg="24" :md="24" :sm="24" :xs="24">
                    <el-form label-position="left" inline class="demo-table-expand" :model="detail">
                      <el-form-item label="测试结果">
                        <div v-if="detail.actual_result" style="color:#009d72;font-weight: 600;">成功</div>
                        <div v-else style="color:#d62f40;font-weight: 600;">失败</div>
                      </el-form-item>
                      <el-form-item label="失败原因" v-if="!detail.actual_result">
                        {{ detail.reason }}
                      </el-form-item>
                      <el-form-item label="" v-else>
                      </el-form-item>
                    </el-form>
                  </el-col>
                </el-row>
              </div>
              <div class="wrap">
                <el-divider content-position="left" @click="logShow.resultShow=!logShow.resultShow">接口返回</el-divider>
                <el-row v-show="logShow.resultShow">
                  <el-col :lg="24" :md="24" :sm="24" :xs="24">
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
              <div class="wrap">
                <el-divider content-position="left" @click="logShow.projectShow=!logShow.projectShow">工程信息</el-divider>
                <el-row v-show="logShow.projectShow">
                  <el-col :lg="24" :md="24" :sm="24" :xs="24">
                    <el-form label-position="left" inline class="demo-table-expand" :model="detail">
                      <el-form-item label="工程名称">
                        <el-button type="primary" plain v-if="!detail.case_group_name" size="small"
                        @click="toProjectConfig(detail.project_id, detail.name)">{{ detail.project_name }}</el-button>
                        <div v-else>{{ detail.project_name }}</div>
                      </el-form-item>
                      <el-form-item label="工程类型">
                        {{ detail.project_type_name }}
                      </el-form-item>
                    </el-form>
                  </el-col>
                </el-row>
              </div>
              <div class="wrap">
                <el-divider content-position="left" @click="logShow.caseShow=!logShow.caseShow">用例信息</el-divider>
                <el-row v-show="logShow.caseShow">
                  <el-col :lg="24" :md="24" :sm="24" :xs="24">
                    <el-form label-position="left" inline class="demo-table-expand" :model="detail">
                      <el-form-item label="用例名称">
                        <el-button type="primary" plain v-if="detail.case_group_name" size="small"
                        @click="toCaseList(detail.case_group, detail.name)">{{ detail.name }}</el-button>
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
            </div>
          </div>
        </el-col>
        <el-col :span="8">
          <div style="height: 52vh;" class="box">
            <transition-group type="transition" :name="'flip-list'" class="list-group" tag="ul" v-loading="logsLoading" element-loading-background="rgba(236, 245, 255, 0.5">
              <li class="list-group-item item-color-normal" v-for="element in CaseLogData" :key="element.name"
                v-bind:class="{ 'item-color-normal': !element.is_choose, 'item-color-choose': element.is_choose }"
                @click="handleChoose(element)">
                <i class="el-icon-check" v-if="element.actual_result && element.is_choose"></i>
                <i class="el-icon-success" v-else-if="element.actual_result" style="color: #00C292"></i>
                <i class="el-icon-error" v-else-if="!element.actual_result && !element.is_choose" style="color: #E46A76"></i>
                <i class="el-icon-close" v-else-if="!element.actual_result && element.is_choose"></i>
                <span class="name">{{element.name}}</span>
                <!-- 调试 -->
                <i class="el-icon-thumb" @click.stop="handleDebug(element)"></i>
                <!-- 鼠标移入查看按钮显示用例详情 -->
                <el-popover
                  placement="right-end"
                  width="450"
                  trigger="hover">
                  <project-case-info :caseDate="element" :caseTypeCode="type"></project-case-info>
                  <i slot="reference" class="el-icon-view"></i>
                </el-popover>
              </li>
            </transition-group>
          </div>
        </el-col>
      </el-row>
    </div>
    <!-- 調試框 -->
    <debug-case :case="debugCase" :drawerShow="drawer" :type="type" @closed="drawerClose" :ruleShow="ruleShow"></debug-case>
  </div>
</template>

<script>
import { get } from '@/lin/plugins/axios'
import ProjectCaseInfo from '../../project/ProjectCaseInfo'
import DebugCase from '../../../components/DebugCase'

export default {
  components: {
    ProjectCaseInfo,
    DebugCase
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
      loading: false,
      logsLoading: false,
      ruleShow: false,
      // 工程编号
      project: null,
      projectList: [],
      // 用例编号
      task: null,
      taskList: [],
      currentTask: {
        user: null,
        time: null,
        success: 0,
        fail: 0,
        total: 0,
      },
      currentProject: {
        running: false,
        progress: 0,
        name: null
      },
      CaseLogData: [],
      type: {
        method: {},
        submit: {},
        deal: {},
        assert: {},
        project: {}
      },
      detail: {
        result: {
          statusCode: null,
        }
      },
      logShow: {
        resultShow: true,
        projectShow: true,
        caseShow: true,
      },
      circle: {},
      line: {},
      linexAxis: [],
      lineSuccess: [],
      lineFail: [],
    }
  },
  async created() {
    this.loading = true
    await this.getType()
    await this.getAllProjects()

    if (this.$route.query.pid) {
      for (let index = 0; index < this.projectList.length; index++) {
        if (this.$route.query.pid === this.projectList[index].id) {
          this.project = this.$route.query.pid
        }
      }
    }

    if (this.$route.query.taskNo) {
      for (let index = 0; index < this.taskList.length; index++) {
        if (this.$route.query.taskNo === this.taskList[index].task_no) {
          this.task = this.$route.query.taskNo
        }
      }
    }
  },
  activated() {
    // 跳转进入页面选中工程和记录
    if (this.$route.query.pid) {
      for (let index = 0; index < this.projectList.length; index++) {
        if (this.$route.query.pid === this.projectList[index].id) {
          this.project = this.$route.query.pid
        }
      }
    }
    if (this.$route.query.taskNo) {
      for (let index = 0; index < this.taskList.length; index++) {
        if (this.$route.query.taskNo === this.taskList[index].task_no) {
          this.task = this.$route.query.taskNo
        }
      }
    }
  },
  watch: {
    project() {
      this.getTasks()
      if (this.project) {
        // 获取工程信息
        for (let index = 0; index < this.projectList.length; index++) {
          if (this.project === this.projectList[index].id) {
            this.currentProject.progress = this.projectList[index].progress
            this.currentProject.running = this.projectList[index].running
            this.currentProject.name = this.projectList[index].name
          }
        }
      } else {
        this.currentProject.progress = 0
        this.currentProject.running = false
        this.currentProject.name = null
      }
    },
    task() {
      // 重置详情
      this.detail.id = null
      if (this.task) {
        // 获取任务信息
        for (let index = 0; index < this.taskList.length; index++) {
          if (this.task === this.taskList[index].task_no) {
            this.currentTask.user = this.taskList[index].create_user_name
            this.currentTask.time = this.taskList[index].create_time
            this.currentTask.success = this.taskList[index].success
            this.currentTask.fail = this.taskList[index].fail
            this.currentTask.total = this.taskList[index].total
          }
        }
        this.getCaseLogs()
      } else {
        this.currentTask.user = null
        this.currentTask.time = null
        this.currentTask.success = null
        this.currentTask.fail = null
        this.currentTask.total = null
        this.CaseLogData = []
      }
      // 刷新饼图
      this.circle.setOption(this.circle_option)
      // 刷新折线图
      this.setLineDate()
    }
  },
  sockets: {
    progress: function progress(data) {
      this.projectList = data
      // 获取工程信息
      for (let index = 0; index < this.projectList.length; index++) {
        if (this.project === this.projectList[index].id) {
          this.currentProject.progress = this.projectList[index].progress
          this.currentProject.running = this.projectList[index].running
        }
      }
    },
    task: function task(data) {
      if (data.project_id === this.project) {
        this.taskList = data.tasks
      }
      for (let index = 0; index < this.taskList.length; index++) {
        if (this.task === this.taskList[index].task_no) {
          this.currentTask.user = this.taskList[index].create_user_name
          this.currentTask.time = this.taskList[index].create_time
          this.currentTask.success = this.taskList[index].success
          this.currentTask.fail = this.taskList[index].fail
          this.currentTask.total = this.taskList[index].total
        }
      }
      // 刷新饼图
      this.circle.setOption(this.circle_option)
      // 刷新折线图
      this.setLineDate()
    },
    log: function log(data) {
      if (data.task_no === this.task) {
        this.CaseLogData = data.logs
      }
    },
  },
  methods: {
    async getAllProjects() {
      try {
        this.projectList = await get('/v1/project', { showBackend: true })
        this.project = this.projectList[0].id
      } catch (e) {
        this.projectList = []
      }
    },
    async getTasks() {
      try {
        this.loading = true
        this.taskList = await get('/v1/task/all', {
          project: this.project
        }, { showBackend: true })
        if (this.taskList.length !== 0) {
          this.task = this.taskList[0].task_no
        } else {
          this.task = null
        }
        this.loading = false
      } catch (error) {
        if (error.error_code !== 0) {
          this.taskList = []
          this.loading = false
        }
      }
    },
    async getCaseLogs() {
      this.logsLoading = true
      try {
        const data = await get('/v1/case/logs/all', {
          task: this.task,
        }, { showBackend: true })
        this.CaseLogData = data
        this.logsLoading = false
      } catch (error) {
        if (error.error_code !== 0) {
          this.CaseLogData = []
          this.logsLoading = false
        }
      }
    },
    async getType() {
      const type = await get('/v1/case/type', { showBackend: true })
      this.type.method = type.METHOD
      this.type.submit = type.SUBMIT
      this.type.deal = type.DEAL
      this.type.assert = type.ASSERT
    },
    handleChoose(log) {
      for (let index = 0; index < this.CaseLogData.length; index++) {
        this.$set(this.CaseLogData[index], 'is_choose', false)
      }
      log.is_choose = true
      this.detail = log
    },
    toProjectConfig(projectId, caseName) {
      this.$router.push({ path: '/project/config', query: { pid: projectId, case: caseName } })
    },
    toCaseList(groupId, caseName) {
      this.$router.push({ path: '/case/case/list', query: { group: groupId, case: caseName } })
    },
    handleDebug(element) {
      this.drawer = true
      this.debugCase.url = element.url
      this.debugCase.method = element.method
      if (element.data) {
        this.debugCase.data = JSON.stringify(element.data, null, 2)
      }
      if (element.header) {
        this.debugCase.header = JSON.stringify(element.header, null, 2)
      }
      this.debugCase.submit = element.submit
      this.debugCase.name = element.name
    },
    drawerClose() {
      this.drawer = false
    },
    setLineDate() {
      this.linexAxis = []
      this.lineSuccess = []
      this.lineFail = []

      let taskLineList = []
      if (this.taskList.length >= 7) {
        taskLineList = this.taskList.slice(0, 7)
      } else {
        taskLineList = this.taskList
      }
      taskLineList.reverse()
      for (let index = 0; index < taskLineList.length; index++) {
        this.linexAxis.push(this.timestampToTime(taskLineList[index].create_time / 1000))
        this.lineSuccess.push(taskLineList[index].success)
        this.lineFail.push(taskLineList[index].fail)
      }
      this.line.setOption(this.line_option)
    },
    timestampToTime(timestamp) {
      // 过滤时间戳，返回值mm-dd ss
      if (!timestamp) {
        return timestamp
      }
      const date = new Date(timestamp * 1000)
      const m = `0${date.getMonth() + 1}`
      const d = `0${date.getDate()}`
      const hh = date.getHours()
      const mm = `${date.getMinutes()}`
      const val = `${m.substring(m.length - 2, m.length)}-${d.substring(d.length - 2, d.length)}  ${hh}:${mm}`
      return val
    },
    reportDownload() {
      this.$axios({
        baseURL: `${process.env.VUE_APP_BASE_URL}`,
        url: `/v1/task/report/${this.task}`,
        method: 'get',
        responseType: 'blob',
      }).then(res => {
        const fileName = `report_${this.currentProject.name}_${this.task}.html`
        const blob = new Blob([res])
        const link = document.createElement('a')
        link.download = fileName
        link.style.display = 'none'
        link.href = URL.createObjectURL(blob)
        document.body.appendChild(link)
        link.click()
        URL.revokeObjectURL(link.href)
        document.body.removeChild(link)
      }).catch(error => {
        const reader = new FileReader()
        reader.readAsText(error.data, 'utf-8')
        reader.onload = e => {
          this.$message.warning(JSON.parse(reader.result).msg)
          console.log(e.target.result)
        }
      })
    },
  },
  mounted() {
    this.circle = this.$echarts.init(document.getElementById('result-circle'))
    this.circle.setOption(this.circle_option)
    this.line = this.$echarts.init(document.getElementById('result-line'))
    this.line.setOption(this.line_option)

    window.onresize = () => {
      this.circle.resize()
      this.line.resize()
    }
  },
  computed: {
    circle_option() {
      const that = this
      const option = {
        title: {
          text: '结果占比',
          left: 'left',
          top: 5,
          textStyle: {
            fontSize: 12,
            color: '#3963bc'
          }
        },
        tooltip: {
          trigger: 'item',
          formatter: '{b} : {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 'right',
          data: ['成功', '失败']
        },
        series: [
          {
            name: '测试结果占比',
            type: 'pie',
            radius: '80%',
            center: ['50%', '50%'],
            data: [
              { value: that.currentTask.success, name: '成功', itemStyle: { color: '#00C292' } },
              { value: that.currentTask.fail, name: '失败', itemStyle: { color: '#E46A76' } },
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
      return option
    },
    line_option() {
      const that = this
      const option = {
        title: {
          text: '近7次执行记录',
          left: 'left',
          top: 5,
          textStyle: {
            fontSize: 12,
            color: '#3963bc'
          }
        },
        tooltip: {
          trigger: 'axis',
        },
        color: ['#00C292', '#E46A76'],
        legend: {
          data: ['成功', '失败']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: that.linexAxis
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: '成功',
            type: 'line',
            smooth: true,
            data: that.lineSuccess,
            lineStyle: {
              normal: {
                color: '#00C292'
              }
            },
          },
          {
            name: '失败',
            type: 'line',
            smooth: true,
            data: that.lineFail,
            lineStyle: {
              normal: {
                color: '#E46A76'
              }
            },
            markPoint: {
              data: [{ type: 'max' }]
            }
          },
        ]
      }
      return option
    },
  }
}
</script>

<style lang="scss" scoped>
.container /deep/ .el-divider__text {
  cursor: pointer;
}

.container {
  padding: 30px;

  .label {
    margin-right: 10px;
    color: #3963bc;
  }

  .box {
    width: 100%;
    background: #fff;
    border-radius:8px;
    box-shadow: 0 2px 14px 0 #f3f3f3;

    .wrap {
      padding: 10px 20px 10px 20px;
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
        margin-bottom: 10px;
      }
    }
  }

    .result {
      height: 100px;
      line-height: 100px;
      display:flex;

      span {
        margin-left: 10px;
      }
    }

    .logDetail {
      overflow-y: auto;
      height: 52vh;
      width: 100%;
    }

    .logDetail::-webkit-scrollbar{
      width:8px;
      height:8px;
      /**/
    }
    .logDetail::-webkit-scrollbar-track{
      background: rgb(239, 239, 239);
      border-radius:2px;
    }
    .logDetail::-webkit-scrollbar-thumb{
      background: #dad4d4;
      border-radius:10px;
    }
    .logDetail::-webkit-scrollbar-thumb:hover{
      background: rgb(175, 173, 173);
    }

    .list-group {
      background: rgba(236, 245, 255, 0.5);
      border-radius: 4px;
      overflow-y: auto;
      height: 52vh;
      width: 100%;
      margin: auto;

      .item-color-normal {
        color: #409EFF;
        background: #ecf5ff;
        border:1px solid #b3d8ff;
      }

      .item-color-choose {
        color: #ecf5ff;
        background: #409EFF;
        border:1px solid #b3d8ff;
      }

      .list-group-item {
        height: 35px;
        line-height: 35px;
        font-weight: 500;
        cursor: pointer;
        border-radius: 4px;
        padding: 0 5px;
        margin: 0 5px 5px 5px;
        display: flex;

        .name {
          flex: 1;
          white-space: nowrap;
          text-overflow: ellipsis;
          width: 100%;
          overflow: hidden;
        }

        i {
          margin: auto 2px;
          cursor: pointer
        }

      }
    }

    .flip-list-move {
      transition: transform 0.6s;
    }

    .list-group::-webkit-scrollbar{
      width:8px;
      height:8px;
      /**/
    }
    .list-group::-webkit-scrollbar-track{
      background: rgb(239, 239, 239);
      border-radius:2px;
    }
    .list-group::-webkit-scrollbar-thumb{
      background: #dad4d4;
      border-radius:10px;
    }
    .list-group::-webkit-scrollbar-thumb:hover{
      background: rgb(175, 173, 173);
    }
  }
}
</style>
