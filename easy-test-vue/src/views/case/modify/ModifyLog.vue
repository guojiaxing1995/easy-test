<template>
  <div>
    <div class="container">
      <div class="header">
        <el-row>
          <el-col :span="6">
            <label class="label" >URL</label>
            <el-input placeholder="请输入URL" v-model="url" clearable style="width:75%" size="small"></el-input>
          </el-col>
          <el-col :span="5">
            <label class="label">请求方法</label>
            <el-select v-model="method" filterable placeholder="请选择请求方法" clearable size="small" style="width:60%">
              <el-option
                :key="key" v-for="(val,key) in type.method"
                :label="val"
                :value="key">
              </el-option>
            </el-select>
          </el-col>
          <el-col :span="5">
            <label class="label">后置处理</label>
            <el-select v-model="deal" filterable placeholder="请选择处理方法" clearable size="small" style="width:60%">
              <el-option
                :key="key" v-for="(val,key) in type.deal"
                :label="val"
                :value="key">
              </el-option>
            </el-select>
          </el-col>
          <el-col :span="7">
          <label class="label" >修改时间</label>
          <el-date-picker
            v-model="datetime"
            clearable
            :default-time="['00:00:00', '23:59:59']"
            value-format="yyyy-MM-dd HH:mm:ss"
            size="small"
            style="width:70%"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期">
          </el-date-picker>
        </el-col>
        <el-col :span="1"><i class="el-icon-refresh" @click="handleRefresh" style="font-size:1.6em"></i></el-col>
      </el-row>
      </div>
      <el-row :gutter="30">
        <el-col :span="6">
          <div style="margin-top:30px"><el-input placeholder="输入用例名称、分组名称进行过滤" v-model="filterText" size="small" style="width:90%"></el-input></div>
          <div class="tree">
            <el-tree v-loading="treeLoading" :data="treeData" ref="tree" :props="treeProps" accordion highlight-current @node-click="handleNodeClick" :filter-node-method="filterNode"></el-tree>
          </div>
        </el-col>
        <el-col :span="18">
          <div class="btn"><el-button type="danger" @click="handleDelete" v-auth="{ auth: '删除修改记录', type: 'disabled'}" plain>删除记录</el-button></div>
          <!-- 列表页面 -->
          <div class="table">
            <el-table
              :data="tableData"
              stripe
              v-loading="loading"
              style="width: 100%">
              <el-table-column type="expand" fixed>
                <template slot-scope="props">
                  <el-form label-position="left" inline class="demo-table-expand">
                    <el-form-item label="处理方法">
                      <div v-for="(val,key) in type.deal" :key="key">
                        <span v-if="props.row.deal.val === parseInt(key)" :class="{'modify':props.row.deal.modify}">{{ val }}</span>
                      </div>
                    </el-form-item>
                    <el-form-item label="处理语句">
                      <span :class="{'modify':props.row.condition.modify}">{{ props.row.condition.val }}</span>
                    </el-form-item>
                    <el-form-item label="断言方式">
                      <div v-for="(val,key) in type.assert" :key="key">
                        <span v-if="props.row.assertion.val === parseInt(key)" :class="{'modify':props.row.assertion.modify}">{{ val }}</span>
                      </div>
                    </el-form-item>
                    <el-form-item label="预期结果">
                      <span :class="{'modify':props.row.expect.modify}">{{ props.row.expect.val }}</span>
                    </el-form-item>
                    <el-form-item label="data">
                      <pre :class="{'modify':props.row.data.modify}">{{ props.row.data.val }}</pre>
                    </el-form-item>
                    <el-form-item label="header">
                      <pre :class="{'modify':props.row.header.modify}">{{ props.row.header.val }}</pre>
                    </el-form-item>
                  </el-form>
                </template>
              </el-table-column>
              <el-table-column
                label="请求方法"
                :show-overflow-tooltip="true"
                width="130">
                <template slot-scope="scope">
                  <div :key="key" v-for="(val,key) in type.method">
                    <div v-if="scope.row.method.val === parseInt(key)" :class="{'modify':scope.row.method.modify}">{{val}}</div>
                  </div>
                </template>
              </el-table-column>
              <el-table-column
                prop="url.val"
                label="URL"
                :show-overflow-tooltip="true"
                min-width="260">
                <template slot-scope="scope">
                  <div  :class="{'modify':scope.row.url.modify}">{{scope.row.url.val}}</div>
                </template>
              </el-table-column>
              <el-table-column
                label="提交方式"
                :show-overflow-tooltip="true"
                width="130">
                <template slot-scope="scope">
                  <div :key="key" v-for="(val,key) in type.submit">
                    <div v-if="scope.row.submit.val === parseInt(key)" :class="{'modify':scope.row.submit.modify}">{{val}}</div>
                  </div>
                </template>
              </el-table-column>
              <el-table-column
                label="描述"
                align="center"
                width="100">
                <template slot-scope="scope">
                  <el-tooltip effect="dark" placement="top-start" v-if="scope.row.info.val">
                    <div slot="content">{{scope.row.info.val}}</div>
                    <l-icon name="info" color="#f4516c" height="1.6em" width="1.6em" style="margin:auto" v-if="scope.row.info.modify"></l-icon>
                    <l-icon name="info" color="#3963bc" height="1.6em" width="1.6em" style="margin:auto" v-else></l-icon>
                  </el-tooltip>
                  <l-icon name="info" color="#ccc" height="1.6em" width="1.6em" v-else style="margin:auto"></l-icon>
                </template>
              </el-table-column>
              <el-table-column
                prop="create_user_name"
                label="修改人"
                :show-overflow-tooltip="true"
                min-width="120">
              </el-table-column>
              <el-table-column
                prop="create_time"
                label="修改时间"
                :show-overflow-tooltip="true"
                min-width="120">
                <template slot-scope="scope">
                  <i class="el-icon-time" style="margin-top:auto;margin-bottom:auto"></i>
                  <span style="margin-left: 10px">{{ scope.row.create_time/1000 | filterTimeYmdHms }}</span>
                </template>
              </el-table-column>
            </el-table>
          </div>
          <div class="pagination">
            <el-pagination
              background
              :hide-on-single-page=true
              @current-change="handleCurrentChange"
              layout="prev, pager, next"
              :current-page="page"
              :page-size=10
              :total="total">
            </el-pagination>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import Utils from 'lin/utils/util'

import { get, post, _delete } from '@/lin/plugins/axios'

export default {
  data() {
    return {
      filterText: '',
      treeLoading: false,
      loading: false,
      cid: null,
      url: null,
      method: null,
      deal: null,
      datetime: null,
      startTime: null,
      endTime: null,
      tableData: [],
      page: 1,
      pages: 1,
      total: 0,
      type: {
        method: {},
        submit: {},
        deal: {},
        assert: {}
      },
      treeData: [],
      treeProps: {
        children: 'cases',
        label: 'name',
      }
    }
  },
  activated() {
  },
  async created() {
    await this.getType()
    await this.groupByCaseGroup()
    // 节流搜素
    this.$watch(
      'url',
      Utils.debounce(() => {
        this.page = 1
        this.getEditLogs()
      }, 1000),
    )
  },
  methods: {
    filterNode(value, data) {
      if (!value) return true
      return data.name.indexOf(value) !== -1
    },
    async handleRefresh() {
      this.page = 1
      await this.getEditLogs()
    },
    async getType() {
      const type = await get('/v1/case/type', { showBackend: true })
      this.type.method = type.METHOD
      this.type.submit = type.SUBMIT
      this.type.deal = type.DEAL
      this.type.assert = type.ASSERT
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
    async getEditLogs() {
      if (!this.cid) {
        this.$message({
          type: 'warning',
          message: '请选择用例',
        })
        return
      }
      this.loading = true
      if (this.datetime) {
        [this.startTime, this.endTime] = this.datetime
      } else {
        this.startTime = null
        this.endTime = null
      }
      let methodPara = null
      let dealPara = null
      if (this.method) {
        methodPara = parseInt(this.method, 10)
      }
      if (this.deal) {
        dealPara = parseInt(this.deal, 10)
      }
      try {
        const data = await post('/v1/case/search/editLogs', {
          id: this.cid,
          method: methodPara,
          deal: dealPara,
          url: this.url,
          start: this.startTime,
          end: this.endTime,
          page: this.page
        }, { showBackend: true })
        this.tableData = data.data
        this.total = data.total
        this.page = data.page
        this.pages = data.pages
        this.loading = false
      } catch (error) {
        if (error.error_code !== 0) {
          this.tableData = []
        }
        this.loading = false
      }
    },
    handleCurrentChange(val) {
      this.page = val
      this.getEditLogs()
    },
    handleNodeClick(obj) {
      if (obj.cases === undefined) {
        this.cid = obj.id
      }
    },
    handleDelete() {
      if (!this.cid) {
        this.$message({
          type: 'warning',
          message: '请选择用例',
        })
        return
      }
      this.$confirm('此操作将按当前查询条件永久删除用例修改记录, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }).then(async () => {
        if (this.datetime) {
          [this.startTime, this.endTime] = this.datetime
        } else {
          this.startTime = null
          this.endTime = null
        }
        let methodPara = null
        let dealPara = null
        if (this.method) {
          methodPara = parseInt(this.method, 10)
        }
        if (this.deal) {
          dealPara = parseInt(this.deal, 10)
        }
        const res = await _delete('/v1/case/editLogs/delete', {
          id: this.cid,
          method: methodPara,
          deal: dealPara,
          url: this.url,
          start: this.startTime,
          end: this.endTime,
        }, { showBackend: true })
        if (res.error_code === 0) {
          this.page = 1
          this.getEditLogs()
          this.$message({
            type: 'success',
            message: `${res.msg}`,
          })
        }
      })
    },
  },
  watch: {
    filterText(val) {
      this.$refs.tree.filter(val)
    },
    cid() {
      this.page = 1
      this.getEditLogs()
    },
    datetime() {
      this.page = 1
      this.getEditLogs()
    },
    method() {
      this.page = 1
      this.getEditLogs()
    },
    deal() {
      this.page = 1
      this.getEditLogs()
    }
  },
}
</script>

<style lang="scss" scoped>
.container {
  padding: 30px;

  .modify {
    color: #f4516c;
  }

  .header {
    color: $parent-title-color;
    font-size: 16px;
    font-weight: 500;

    .el-icon-refresh{
      font-size: 20px;
      cursor: pointer;
    }

    .label {
      margin-right: 10px;
    }
  }

  .btn {
    display: flex;
    justify-content: flex-start;
    margin-top: 30px;
  }

  .tree {
    height: 60vh;
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

  .table{
    margin-top: 30px;
  }

  .table /deep/ .demo-table-expand {
    font-size: 0;
  }
  .table /deep/ .demo-table-expand label {
    width: 80px;
    color: #3963bc;
  }
  .table /deep/ .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 50%;
  }
  .table /deep/ .el-form-item__content {
    margin-bottom: 0;
  }
  .table /deep/ .el-table .cell {
    padding-left: 20px;
  }
  // 滚动条优化
  .table /deep/ .el-table__body-wrapper::-webkit-scrollbar {
    width: 6px;
    height: 10px;
  }
  .table /deep/ .el-table__body-wrapper::-webkit-scrollbar-thumb {
    background-color: #ddd;
    border-radius: 5px;
  }

  .pagination {
    display: flex;
    justify-content: flex-end;
    margin-top: 30px;
    margin-bottom: 20px;
  }

}
</style>
