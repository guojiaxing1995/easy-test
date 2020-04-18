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
    <el-divider>副本</el-divider>
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
            <div class="submit"><el-button type="primary" plain>保存配置</el-button></div>
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
                  trigger="click">
                  <project-case-info :caseDate="element" :caseTypeCode="type"></project-case-info>
                  <i slot="reference" class="el-icon-view"></i>
                </el-popover>
              </li>
            </transition-group>
          </draggable>
        </el-col>
        <el-col :span="7">
          <!-- 工程用例列表 -->
          <draggable v-model="projectCases" v-bind="dragOptions" @start="isDragging=true" @end="isDragging=false">
            <transition-group type="transition" :name="'flip-list'" class="list-group" tag="ul">
              <li class="list-group-item" v-bind:class="{ 'item-color-normal': element.run, 'item-color-stop': !element.run }"
              v-for="element in projectCases" :key="element.random" v-show="element.show">
                <span class="name">{{element.name}}</span>
                <el-popover
                  placement="right-end"
                  width="500"
                  trigger="click">
                  <!-- 编辑 -->
                  <project-case-edit :caseDate="element" :caseTypeCode="type"></project-case-edit>
                  <i slot="reference" class="el-icon-edit-outline"></i>
                </el-popover>
                <i class="el-icon-switch-button"  @click=" element.run=! element.run"></i>
              </li>
            </transition-group>
          </draggable>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import draggable from 'vuedraggable'
import ProjectCaseInfo from './ProjectCaseInfo'
import ProjectCaseEdit from './ProjectCaseEdit'
import { get } from '@/lin/plugins/axios'

export default {
  components: {
    draggable,
    ProjectCaseInfo,
    ProjectCaseEdit
  },
  data() {
    return {
      groupCaseLoading: false,
      searchGroupCase: '',
      searchProjectCase: '',
      selectGroup: '',
      selecGroupData: [],
      selectProject: '',
      selecProjectData: [],
      loading: false,
      editable: true,
      isDragging: false,
      delayedDragging: false,
      groupCases: [],
      projectCases: [],
      type: {
        method: {},
        submit: {},
        deal: {},
        assert: {}
      }
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
    // 获取所有工程
    async getAllProjects() {
      try {
        this.selecProjectData = await get('/v1/project', { showBackend: true })
        this.selectProject = this.selecProjectData[0].name
      } catch (error) {
        console.log(error)
      }
    },
    async getAllGroups() {
      try {
        this.selecGroupData = await get('/v1/caseGroup', { showBackend: true })
        this.selectGroup = this.selecGroupData[0].id
      } catch (e) {
        this.selecGroupData = []
      }
    },
    // 对用例列表进行处理，给列表添加 是否运行 和 是否在列表中显示 属性
    dealCases(testCases) {
      for (const testCase of testCases) {
        testCase.show = true
        testCase.run = true
        testCase.random = Math.random().toString(36).substr(2)
      }
      return testCases
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
