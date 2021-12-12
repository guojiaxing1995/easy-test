<template>
  <div>
    <div class="container">
      <el-row :gutter="30">
        <el-col :span="6">
          <div><el-input placeholder="输入用例名称、分组名称进行过滤" v-model="filterText" size="small" style="width:90%"></el-input></div>
          <div class="tree">
            <el-tree v-loading="treeLoading" :data="treeData" ref="tree" :props="treeProps" accordion highlight-current @node-click="handleNodeClick" :filter-node-method="filterNode"></el-tree>
          </div>
        </el-col>
        <el-col :span="18">
          <el-row :gutter="30">
            <el-col :span="16">
              <el-row :gutter="30">
                <el-col :span="12" style="padding-left:0px">
                  <div style="height: 25vh;" class="box" v-loading="loading">
                    <div style="height: 125px;line-height: 125px">
                      <span style="margin-left:10px" class="label">总执行次数</span><span style="font-size:30px;margin-left:10px;color: #3963BC">{{ collect.count }}</span>
                    </div>
                    <div class="result">
                      <div style="width:50%"><span class="label">成功次数</span><span style="font-size:30px;color: #00C292">{{ collect.true_count }}</span></div>
                      <div style="width:50%"><span class="label">失败次数</span><span style="font-size:30px;color: #E46A76">{{ collect.false_count }}</span></div>
                    </div>
                  </div>
                </el-col>
                <el-col :span="12" style="padding-right:0px"><div style="height: 25vh;width:100%" class="box" id="result-circle"></div></el-col>
              </el-row>
            </el-col>
            <el-col :span="8">
              <div style="height: 25vh;" class="box">
                <div style="height: 25px;line-height: 25px;text-align:center">
                  <span style="margin-left:10px" class="label">加入<span style="font-size:25px;margin-left:5px;margin-right:5px;color: #3963BC">{{ userdProject.length }}</span>个工程</span>
                </div>
                <div style="height:85%;margin-top:10px" v-show="userdProject.length">
                  <el-scrollbar style="height:100%">
                  <el-table
                    :data="userdProject"
                    stripe
                    v-loading="loading"
                    style="width: 100%;height:100%">
                    <el-table-column
                      prop="name"
                      label="工程名称"
                      :show-overflow-tooltip="true"
                      min-width="230">
                    </el-table-column>
                    <el-table-column
                      prop="type_name"
                      label="工程类型"
                      :show-overflow-tooltip="true"
                      width="100">
                    </el-table-column>
                  </el-table>
                  </el-scrollbar>
                </div>
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="30" style="margin-top:30px">
            <el-col :span="16">
              <el-row :gutter="30">
                <div style="height: 7vh;" class="box" v-loading="loading">
                  <div style="height: 7vh;line-height: 7vh;width:100%;display:flex">
                    <div style="width:50%"><span style="margin-left:20px" class="label">用例修改次数</span><span style="font-size:20px;margin-left:10px;color: #3963BC">{{ collect.edit_count }}</span></div>
                    <div style="width:50%">
                      <span style="margin-left:20px" class="label">上次修改时间</span>
                      <span style="font-size:20px;margin-left:10px;color: #3963BC">{{ collect.last_modify_time/1000 | filterTimeYmdHms }}</span>
                    </div>
                  </div>
                </div>
              </el-row>
              <el-row :gutter="30" style="margin-top:3vh">
                <div style="height: 45vh;" class="box">
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
                              <pre>{{ detail.condition }}</pre>
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
              </el-row>
            </el-col>
            <el-col :span="8">
              <div style="height: 55vh;" class="box" v-loading="loading">
                <el-tabs v-model="activeModel">
                  <el-tab-pane label="近10次失败记录" name="first">
                    <transition-group type="transition" :name="'flip-list'" class="list-group" tag="ul" element-loading-background="rgba(236, 245, 255, 0.5">
                      <li class="list-group-item item-color-normal" v-for="element in failLogData" :key="element.create_time"
                        v-bind:class="{ 'item-color-normal': !element.is_choose, 'item-color-choose': element.is_choose }"
                        @click="handleFailChoose(element)">
                        <i class="el-icon-check" v-if="element.actual_result && element.is_choose"></i>
                        <i class="el-icon-success" v-else-if="element.actual_result" style="color: #00C292"></i>
                        <i class="el-icon-error" v-else-if="!element.actual_result && !element.is_choose" style="color: #E46A76"></i>
                        <i class="el-icon-close" v-else-if="!element.actual_result && element.is_choose"></i>
                        <span class="name">{{element.create_time/1000 | filterTimeYmdHms}}</span>
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
                  </el-tab-pane>
                  <el-tab-pane label="近10次成功记录" name="second">
                    <transition-group type="transition" :name="'flip-list'" class="list-group" tag="ul" element-loading-background="rgba(236, 245, 255, 0.5">
                      <li class="list-group-item item-color-normal" v-for="element in successLogData" :key="element.create_time"
                        v-bind:class="{ 'item-color-normal': !element.is_choose, 'item-color-choose': element.is_choose }"
                        @click="handleSuccessChoose(element)">
                        <i class="el-icon-check" v-if="element.actual_result && element.is_choose"></i>
                        <i class="el-icon-success" v-else-if="element.actual_result" style="color: #00C292"></i>
                        <i class="el-icon-error" v-else-if="!element.actual_result && !element.is_choose" style="color: #E46A76"></i>
                        <i class="el-icon-close" v-else-if="!element.actual_result && element.is_choose"></i>
                        <span class="name">{{element.create_time/1000 | filterTimeYmdHms}}</span>
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
                  </el-tab-pane>
                </el-tabs>
              </div>
            </el-col>
          </el-row>
        </el-col>
      </el-row>
    </div>
    <!-- 調試框 -->
    <debug-case :case="debugCase" :drawerShow="drawer" :type="type" @closed="drawerClose" :ruleShow="ruleShow"></debug-case>
  </div>
</template>

<script>
import ProjectCaseInfo from '../project/ProjectCaseInfo'
import DebugCase from '../../components/DebugCase'

import { get, post } from '@/lin/plugins/axios'

export default {
  components: {
    ProjectCaseInfo,
    DebugCase
  },
  data() {
    return {
      filterText: '',
      treeLoading: false,
      loading: false,
      cid: null,
      url: null,
      treeData: [],
      treeProps: {
        children: 'cases',
        label: 'name',
      },
      successLogData: [],
      failLogData: [],
      type: {
        method: {},
        submit: {},
        deal: {},
        assert: {},
        project: {}
      },
      userdProject: [],
      activeModel: 'first',
      collect: {
        true_count: 0,
        false_count: 0,
        count: 0,
        last_modify_time: null,
        edit_count: 0
      },
      detail: {
        result: {
          statusCode: null,
        }
      },
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
      ruleShow: false,
      logShow: {
        resultShow: true,
        projectShow: true,
        caseShow: true,
      },
    }
  },
  activated() {
  },
  async created() {
    await this.groupByCaseGroup()
    await this.getType()
  },
  methods: {
    filterNode(value, data) {
      if (!value) return true
      return data.name.indexOf(value) !== -1
    },
    async getCaseCollect() {
      this.collect = await get(`/v1/case/collect/${this.cid}`, { showBackend: true })
    },
    async getUsedByProject() {
      this.userdProject = await get(`/v1/case/usedByProject/${this.cid}`, { showBackend: true })
    },
    async groupByCaseGroup() {
      this.treeLoading = true
      try {
        this.treeData = await get('/v1/case/groupByCaseGroup', { showBackend: true })
        this.treeLoading = false
      } catch (e) {
        this.loading = false
        this.treeLoading = false
      }
    },
    handleNodeClick(obj) {
      if (obj.cases === undefined) {
        this.cid = obj.id
      }
    },
    async getCaseLogs() {
      try {
        const successData = await post('/v1/case/logs', {
          id: this.cid,
          result: true,
        }, { showBackend: true })
        this.successLogData = successData.data
        const failData = await post('/v1/case/logs', {
          id: this.cid,
          result: false,
        }, { showBackend: true })
        this.failLogData = failData.data
      } catch (error) {
        if (error.error_code !== 0) {
          this.successLogData = []
          this.failLogData = []
        }
      }
    },
    handleSuccessChoose(log) {
      for (let index = 0; index < this.successLogData.length; index++) {
        this.$set(this.successLogData[index], 'is_choose', false)
      }
      log.is_choose = true
      this.detail = log
    },
    handleFailChoose(log) {
      for (let index = 0; index < this.failLogData.length; index++) {
        this.$set(this.failLogData[index], 'is_choose', false)
      }
      log.is_choose = true
      this.detail = log
    },
    async getType() {
      const type = await get('/v1/case/type', { showBackend: true })
      this.type.method = type.METHOD
      this.type.submit = type.SUBMIT
      this.type.deal = type.DEAL
      this.type.assert = type.ASSERT
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
  },
  watch: {
    filterText(val) {
      this.$refs.tree.filter(val)
    },
    async cid() {
      this.detail.id = null
      this.loading = true
      await this.getCaseCollect()
      await this.getUsedByProject()
      await this.getCaseLogs()
      this.loading = false
      // 刷新饼图
      this.circle.setOption(this.circle_option)
    },
  },
  mounted() {
    this.circle = this.$echarts.init(document.getElementById('result-circle'))
    this.circle.setOption(this.circle_option)

    window.onresize = () => {
      this.circle.resize()
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
              { value: that.collect.true_count, name: '成功', itemStyle: { color: '#00C292' } },
              { value: that.collect.false_count, name: '失败', itemStyle: { color: '#E46A76' } },
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
  }
}
</script>

<style lang="scss" scoped>
.container {
  padding: 30px;

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
      height: 125px;
      line-height: 125px;
      display:flex;

      span {
        margin-left: 10px;
      }
    }

    label {
      width: 100px;
      font-size: 15px;
      // font-weight: 600;
      color: #3963bc;
    }

    .logDetail {
      overflow-y: auto;
      height: 45vh;
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

  .tree {
    height: 80vh;
    width: 100%;
    margin-top:30px;
    overflow-y: auto;
  }

  .tree::-webkit-scrollbar{
    width:8px;
    height:8px;
    /**/
  }
  .tree::-webkit-scrollbar-track{
    background: rgb(239, 239, 239);
    border-radius:2px;
  }
  .tree::-webkit-scrollbar-thumb{
    background: #dad4d4;
    border-radius:10px;
  }
  .tree::-webkit-scrollbar-thumb:hover{
    background: rgb(175, 173, 173);
  }

  .el-table {
    border: none;
  }

  .box /deep/ .el-tabs__nav {
    width: 100% !important;
  }

  .box /deep/ .el-tabs__active-bar .is-top {
    width: 50% !important;
  }

  .box /deep/ .el-tabs__item{
    padding: 0 !important;
    width: 50%;
    text-align: center;
  }


}
</style>
