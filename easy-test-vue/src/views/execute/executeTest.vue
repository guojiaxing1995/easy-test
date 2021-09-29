<template>
  <div class="container">
    <div class="title">
      工程进度信息
      <div class="audioState">
        <l-icon :name="audioState.name" color="#3963bc" height="1.6em" width="1.6em" style="margin:auto" @click="changeAudioState"></l-icon>
      </div>
      <el-input size="small" v-model="searchProject" filterable placeholder="请输入工程名称查询" class="search" clearable>
        <el-option
          v-for="item in selectData"
          :key="item.id"
          :label="item.name"
          :value="item.name">
        </el-option>
      </el-input>
    </div>
    <el-table
      :data="tableData"
      class="processTable"
      stripe
      v-loading="loading">
      <el-table-column
        fixed
        prop="name"
        label="名称"
        :show-overflow-tooltip="true"
        min-width="200">
      </el-table-column>
      <el-table-column
        prop="progress"
        label="进度"
        min-width="350">
        <template slot-scope="scope">
          <el-progress :text-inside="true" :stroke-width="22" :percentage="scope.row.progress" style="width:100%"></el-progress>
        </template>
      </el-table-column>
      <el-table-column
        width="500"
        align="center"
        fixed="right"
        label="操作">
        <template slot-scope="scope">
          <el-button
            size="small"
            type="primary"
            plain
            style="margin:auto"
            @click="toProjectConfig(scope.$index, scope.row)">工程配置</el-button>
          <el-button
            size="small"
            type="primary"
            plain
            style="margin:auto"
            @click="toProjectList(scope.$index, scope.row)">工程列表</el-button>
          <el-button
            size="small"
            type="primary"
            plain
            style="margin:auto"
            @click="toCaseLogList(scope.$index, scope.row)">用例日志</el-button>
          <el-button
            size="small"
            type="primary"
            plain
            style="margin:auto"
            @click="toRecordList(scope.$index, scope.row)">运行记录</el-button>
          <el-button
            size="small"
            type="primary"
            plain
            style="margin:auto"
            @click="toTestDetail(scope.$index, scope.row)">运行详情</el-button>
        </template>
      </el-table-column>
      <el-table-column
        width="150"
        align="center"
        fixed="right"
        label="启动">
        <template slot-scope="scope">
          <i class="el-icon-video-play" style="font-size:1.8em;margin:auto;color:rgb(47, 78, 140);cursor:pointer" @click="execute(scope.$index, scope.row)"></i>
        </template>
      </el-table-column>
    </el-table>
    <audio controls  :src="audioUrl" ref="audio" style="display:none;" preload="auto"></audio>
  </div>
</template>

<script>
import Utils from 'lin/utils/util'
import { get } from '@/lin/plugins/axios'
import over from '../../assets/video/over.wav'

export default {
  components: {
  },
  data() {
    return {
      id: 0, // 分组id
      tableData: [], // 表格数据
      selectData: [], // 拉框数据
      searchProject: '',
      loading: false,
      audioUrl: over,
      audioState: {
        name: 'audioOpen',
        state: true
      },
    }
  },
  sockets: {
    connect: function connect() {
      console.log('socket connected')
    },
    finish: function finish(data) {
      this.$notify({
        title: '执行完成',
        message: data.name,
        duration: 0,
        type: 'success'
      })
      // 播放完成提示音
      this.$refs.audio.currentTime = 0
      this.$refs.audio.play()
    },
    progress: function progress(data) {
      if (this.searchProject === '') {
        this.tableData = data
      } else {
        const projectData = []
        for (const i in data) {
          if (data[i].name.indexOf(this.searchProject) !== -1) {
            projectData.push(data[i])
          }
        }
        this.tableData = projectData
      }
    },
  },
  methods: {
    async getProjects() {
      try {
        this.loading = true
        this.tableData = await get('/v1/project/search', { name: this.searchProject }, { showBackend: true })
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    async execute(index, val) {
      const res = await get(`/v1/task/${val.id}`, { showBackend: true })
      if (res.error_code === 0) {
        this.$message({
          type: 'success',
          message: `${res.msg}`,
        })
      } else {
        this.$message({
          type: 'error',
          message: `${res.msg}`,
        })
      }
    },
    toProjectList(index, val) {
      this.$router.push({ path: '/project/list', query: { pname: val.name } })
    },
    toProjectConfig(index, val) {
      this.$router.push({ path: '/project/config', query: { pid: val.id } })
    },
    toCaseLogList(index, val) {
      this.$router.push({ path: '/test/log', query: { pname: val.name } })
    },
    toRecordList(index, val) {
      this.$router.push({ path: '/test/record', query: { pid: val.id } })
    },
    toTestDetail(index, val) {
      this.$router.push({ path: '/test/detail', query: { pid: val.id } })
    },
    changeAudioState() {
      if (this.audioState.state) {
        this.audioState.state = false
        this.audioState.name = 'audioClose'
        this.$refs.audio.muted = true
      } else {
        this.audioState.state = true
        this.audioState.name = 'audioOpen'
        this.$refs.audio.muted = false
      }
    }
  },
  async created() {
    await this.getProjects()
    // 节流搜素
    this.$watch(
      'searchProject',
      Utils.debounce(() => {
        this.getProjects()
      }, 1000),
    )
  },
  activated() {
  },
  deactivated() {
  },
  beforeDestroy() {
  },
}
</script>

<style lang="scss" scoped>
.container {
  padding: 0 30px;

  .processTable /deep/ .el-table__fixed-right {
    height: 100% !important;
  }
  .processTable /deep/ .el-table__fixed {
    height: 100% !important;
  }
  .processTable {
    width: 100%;
  }
  .title {
    height: 59px;
    line-height: 59px;
    color: $parent-title-color;
    font-size: 16px;
    font-weight: 500;
    position: relative;
    width: 100%;
    .search {
      position: absolute;
      width: 15%;
      right: 0;
    }
    .audioState {
      position: absolute;
      right: 16%;
      top: 8px;
      cursor:pointer;
    }
  }
}
</style>
