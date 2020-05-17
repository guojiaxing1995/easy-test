<template>
  <div class="container">
    <div class="header">
      <span class="title">工程配置</span>
      <el-tooltip effect="dark" placement="top-start">
        <div slot="content">在左侧通过分组查询用例，将目标用例拖拽添加至右侧工程中<br>工程列表中可通过上下拖动用例排序来修改用例执行顺序<br>分组用例列表有查看用例详情按钮，工程用例列表有用例执行开关按钮
        <br>副本类型工程可点击编辑按钮修改用例，关联类型工程需在用例管理页修改用例</div>
        <div class="info"><i class="iconfont icon-Info2" style="font-size:1.2em"></i></div>
      </el-tooltip>
      <el-select size="small" v-model="selectProject" filterable placeholder="请输入工程名称查询" class="select">
        <el-option
          v-for="item in selecProjectData"
          :key="item.id"
          :label="item.name"
          :value="item.id">
        </el-option>
      </el-select>
    </div>
    <el-divider>
      <div :key="key" v-for="(val,key) in type.project">
        <div v-show="parseInt(currentProject.type)  === parseInt(key)">{{val}}</div>
      </div>
    </el-divider>
    <div class="transfer">
      <el-row type="flex" justify="space-around">
        <el-col :span="7">
          <div class="selectGroup">
            <el-select v-model="selectGroup" filterable placeholder="请输入分组名称查询" class="select" style="width:100%">
              <el-option
                v-for="item in selecGroupData"
                :key="item.id"
                :label="item.name"
                :value="item.id">
              </el-option>
            </el-select>
          </div>
        </el-col>
        <el-col :span="7">
          <div class="config">
            <div class="switch"><el-switch v-model="editable" active-text="用例拖动"></el-switch></div>
            <div class="submit"><el-button type="primary" @click="saveConfig" plain v-loading="projectCaseLoading">保存配置</el-button></div>
          </div>
        </el-col>
      </el-row>
      <el-row type="flex" justify="space-around">
        <el-col :span="7">
          <div class="search"><el-input v-model="searchGroupCase" placeholder="输入用例名称搜索" ></el-input></div>
        </el-col>
        <el-col :span="7">
          <div class="search"><el-input v-model="searchProjectCase" placeholder="输入用例名称搜索"></el-input></div>
        </el-col>
      </el-row>
      <el-row type="flex" justify="space-around">
        <el-col :span="7">
          <!-- 分组用例列表 -->
          <draggable v-model="groupCases" v-bind="dragOptions" @start="isDragging=true" @end="isDragging=false" v-loading="groupCaseLoading">
            <transition-group name="no" class="list-group" tag="ul">
              <li class="list-group-item item-color-normal" v-for="element in groupCases" :key="element.name" v-show="element.show">
                <span class="name">{{element.name}}</span>
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
          </draggable>
        </el-col>
        <el-col :span="7">
          <!-- 工程用例列表 -->
          <draggable v-model="projectCases" v-bind="dragOptions" @start="isDragging=true" @end="isDragging=false" v-loading="projectCaseLoading">
            <transition-group type="transition" :name="'flip-list'" class="list-group" tag="ul">
              <li class="list-group-item" v-bind:class="{ 'item-color-normal': element.is_run, 'item-color-stop': !element.is_run }"
              v-for="element in projectCases" :key="element.random" v-show="element.show">
                <span class="name">{{element.name}}</span>
                <el-popover
                  placement="right-end"
                  width="500"
                  trigger="click">
                  <!-- 编辑 -->
                  <project-case-edit :caseDate="element" :caseTypeCode="type" :projectId="selectProject"></project-case-edit>
                  <i slot="reference" class="el-icon-edit-outline" v-show="currentProject.type === 2"></i>
                </el-popover>
                <!-- 调试 -->
                <i class="el-icon-thumb" @click="handleDebug(element)"></i>
                <!-- 是否运行开关 -->
                <i class="el-icon-switch-button" @click=" element.is_run=! element.is_run"></i>
              </li>
            </transition-group>
          </draggable>
        </el-col>
      </el-row>
    </div>
    <!-- 調試框 -->
    <debug-case :case="debugCase" :drawerShow="drawer" :type="type" @closed="drawerClose" :ruleShow="ruleShow"></debug-case>
  </div>
</template>

<script>
import draggable from 'vuedraggable'
import ProjectCaseInfo from './ProjectCaseInfo'
import ProjectCaseEdit from './ProjectCaseEdit'
import DebugCase from '../../components/DebugCase'
import { get, post } from '@/lin/plugins/axios'

export default {
  components: {
    draggable,
    ProjectCaseInfo,
    ProjectCaseEdit,
    DebugCase
  },
  data() {
    return {
      ruleShow: true,
      debugCase: {
        url: '',
        method: '',
        data: '',
        header: '',
        submit: '',
        server: '',
        name: '',
      },
      // 控制调试框是否显示
      drawer: false,
      groupCaseLoading: false,
      projectCaseLoading: false,
      searchGroupCase: '',
      searchProjectCase: '',
      selectGroup: '',
      selecGroupData: [],
      // 当前的工程id
      selectProject: null,
      selecProjectData: [],
      loading: false,
      editable: true,
      isDragging: false,
      delayedDragging: false,
      // 左边用例列表
      groupCases: [],
      // 右边工程配置列表
      projectCases: [],
      type: {
        method: {},
        submit: {},
        deal: {},
        assert: {},
        project: {}
      },
      // 当前的工程
      currentProject: {}
    }
  },
  computed: {
    dragOptions() {
      return {
        animation: 300,
        group: 'description',
        disabled: !this.editable,
        ghostClass: 'ghost'
      }
    },
  },
  methods: {
    async getType() {
      const type = await get('/v1/case/type', { showBackend: true })
      this.type.method = type.METHOD
      this.type.submit = type.SUBMIT
      this.type.deal = type.DEAL
      this.type.assert = type.ASSERT
    },
    async getProjectType() {
      const type = await get('/v1/project/type', { type: 'TYPE' }, { showBackend: true })
      this.type.project = type
    },
    // 获取当前用户授权的所有工程并传给table渲染
    async getAllProjects() {
      try {
        this.selecProjectData = await get('/v1/project/auth', { showBackend: true })
        this.selectProject = this.selecProjectData[0].id
      } catch (error) {
        console.log(error)
      }
    },
    // 获取工程配置
    async getProjectConfig() {
      try {
        this.projectCaseLoading = true
        const configs = await get(`/v1/project/getConfig/${this.selectProject}`, { showBackend: true })
        this.projectCases = this.dealConfigs(configs)
        this.projectCaseLoading = false
      } catch (error) {
        this.projectCaseLoading = false
      }
    },
    // 获取所有的用例组
    async getAllGroups() {
      try {
        this.selecGroupData = await get('/v1/caseGroup/auth', { showBackend: true })
        this.selectGroup = this.selecGroupData[0].id
      } catch (e) {
        this.selecGroupData = []
      }
    },
    // 对用例列表进行处理，给列表添加 是否运行 和 是否在列表中显示 属性
    dealCases(testCases) {
      for (const testCase of testCases) {
        testCase.show = true
        testCase.is_run = true
        testCase.case_id = testCase.id
        testCase.id = null
        testCase.random = Math.random().toString(36).substr(2)
      }
      return testCases
    },
    // 对工程用例列表进行处理，给列表添加 随机数 和 是否在列表中显示 属性
    dealConfigs(testCases) {
      for (const testCase of testCases) {
        testCase.show = true
        testCase.random = Math.random().toString(36).substr(2)
      }
      return testCases
    },
    // 生成工程配置入参
    configParameterDeal(testCases) {
      const configs = []
      for (let i = 0; i < testCases.length; i++) {
        const config = []
        config.push(testCases[i].id)
        config.push(testCases[i].case_id)
        config.push(testCases[i].is_run)
        config.push(i + 1)
        configs.push(config)
      }
      return configs
    },
    // 保存配置
    async saveConfig() {
      const configsPara = this.configParameterDeal(this.projectCases)
      let res
      try {
        this.projectCaseLoading = true
        res = await post('/v1/project/saveConfig', {
          projectId: this.selectProject,
          configs: configsPara
        }, { showBackend: true })
        this.projectCaseLoading = false
      } catch (e) {
        this.projectCaseLoading = false
      }
      if (res.error_code === 0) {
        this.$message.success(`${res.msg}`)
        this.getProjectConfig()
      } else {
        this.$message.error(`${res.msg}`)
      }
    },
    // 打开调试框
    handleDebug(val) {
      this.drawer = true
      this.debugCase = val
    },
    // 关闭调试框后父组件修改状态
    drawerClose() {
      this.drawer = false
    },
  },
  watch: {
    isDragging(newValue) {
      if (newValue) {
        this.delayedDragging = true
        return
      }
      this.$nextTick(() => {
        this.delayedDragging = false
      })
    },
    // 通过用例分组下拉框获取分组用例
    async selectGroup() {
      try {
        this.groupCaseLoading = true
        const cases = await get('/v1/case/casesByGroup', { caseGroup: this.selectGroup }, { showBackend: true })
        this.groupCases = this.dealCases(cases)
        this.groupCaseLoading = false
      } catch (e) {
        this.groupCases = []
        this.groupCaseLoading = false
      }
    },
    async selectProject(value) {
      this.getProjectConfig()
      for (const project of this.selecProjectData) {
        if (project.id === value) {
          this.currentProject = project
        }
      }
    },
    searchProjectCase(value) {
      if (value === '') {
        for (const testCase of this.projectCases) {
          testCase.show = true
        }
      } else {
        for (const testCase of this.projectCases) {
          if (testCase.name.indexOf(value) === -1) {
            testCase.show = false
          } else {
            testCase.show = true
          }
        }
      }
    },
    searchGroupCase(value) {
      if (value === '') {
        for (const testCase of this.groupCases) {
          testCase.show = true
        }
      } else {
        for (const testCase of this.groupCases) {
          if (testCase.name.indexOf(value) === -1) {
            testCase.show = false
          } else {
            testCase.show = true
          }
        }
      }
    },
  },
  async created() {
    await this.getAllProjects()
    await this.getAllGroups()
    await this.getType()
    await this.getProjectType()
    if (this.$route.query.pid) {
      for (let index = 0; index < this.selecProjectData.length; index++) {
        if (this.$route.query.pid === this.selecProjectData[index].id) {
          this.selectProject = this.$route.query.pid
        }
      }
    }
  },
  activated() {
    if (this.$route.query.pid) {
      for (let index = 0; index < this.selecProjectData.length; index++) {
        if (this.$route.query.pid === this.selecProjectData[index].id) {
          this.selectProject = this.$route.query.pid
        }
      }
    }
  },
}
</script>

<style lang="scss" scoped>
.container {
  padding: 0 30px;

  .header {
    height: 65px;
    line-height: 65px;
    color: $parent-title-color;
    position: relative;
    width: 100%;
    text-align: center;
    .title {
      font-size: 22px;
      font-weight: 500;
      position: relative;
    }
    .select {
      position: absolute;
      right: 0;
    }
    .info {
      display: inline-block;
      margin-left: 10px;
    }
  }

  .transfer {
      /*修改滚动条样式*/
    .list-group::-webkit-scrollbar{
      width:10px;
      height:10px;
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

  .config {
    height: 100%;
    margin: 5px;
    width: 100%;
    display: flex;
    justify-content: space-around;
    align-items: center;
  }

  .selectGroup {
    margin: 5px;
  }
  .search {
    margin: 5px;
  }

  .flip-list-move {
    transition: transform 0.6s;
  }

  .no-move {
    transition: transform 0s;
  }

  .list-group {
    background: rgba(236, 245, 255, 0.5);
    border-radius: 4px;
    overflow-y: auto;
    height: 600px;

    .item-color-normal {
      color: #409EFF;
      background: #ecf5ff;
      border:1px solid #b3d8ff;
    }

    .item-color-stop {
      color: #909399;
      background: #f4f4f5;
      border:1px solid #d3d4d6;
    }

    .list-group-item {
      height: 35px;
      line-height: 35px;
      font-weight: 500;
      cursor: move;
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
}
</style>
