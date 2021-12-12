<template>
  <div class="caseInfo">
    <el-table :data="element"
              size="mini"
              :header-cell-style="headerClass"
              :cell-style="cellClass"
              :row-style="rowClass">
      <el-table-column width="125" property="method" label="请求方法" :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <div :key="key" v-for="(val,key) in type.method">
            <div v-show="parseInt(scope.row.method)  === parseInt(key)">{{val}}</div>
          </div>
        </template>
      </el-table-column>
      <el-table-column min-width="150" property="url" label="URL" :show-overflow-tooltip="true"></el-table-column>
    </el-table>
    <el-table :data="element"
              size="mini"
              :cell-style="cellClass"
              :header-cell-style="headerClass"
              :row-style="rowClass">
      <el-table-column width="125" property="deal" label="后置处理" :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <div :key="key" v-for="(val,key) in type.deal">
            <div v-show="parseInt(scope.row.deal)  === parseInt(key)">{{val}}</div>
          </div>
        </template>
      </el-table-column>
      <el-table-column min-width="150" property="condition" label="处理语句" :show-overflow-tooltip="true">
        <template slot-scope="scope">
            <pre>{{scope.row.condition}}</pre>
        </template>
      </el-table-column>
    </el-table>
    <el-table :data="element"
              size="mini"
              :cell-style="cellClass"
              :header-cell-style="headerClass"
              :row-style="rowClass">
      <el-table-column width="125" property="assertion" label="断言类型" :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <div :key="key" v-for="(val,key) in type.assert">
            <div v-show="parseInt(scope.row.assertion)  === parseInt(key)">{{val}}</div>
          </div>
        </template>
      </el-table-column>
      <el-table-column min-width="150" property="expect" label="预期结果" :show-overflow-tooltip="true"></el-table-column>
    </el-table>
    <el-table :data="element"
              size="mini"
              :show-header="false"
              :cell-style="cellClass"
              :row-style="headerClass">
      <el-table-column width="50" property="assertion" label="请求头" type="expand">
        <template slot-scope="scope">
          <pre style="color:#409EFF">{{scope.row.header}}</pre>
        </template>
      </el-table-column>
      <el-table-column min-width="150" property="expect" label="请求头" :show-overflow-tooltip="true">请求头</el-table-column>
    </el-table>
    <el-table :data="element"
              size="mini"
              :show-header="false"
              :cell-style="cellClass"
              :row-style="headerClass">
      <el-table-column width="50" property="assertion" label="请求体" type="expand">
        <template slot-scope="scope">
          <pre style="color:#409EFF">{{scope.row.data}}</pre>
        </template>
      </el-table-column>
      <el-table-column min-width="150" property="expect" label="请求体" :show-overflow-tooltip="true">请求体</el-table-column>
    </el-table>
  </div>
</template>

<script>

export default {
  props: {
    caseDate: {
      type: Object,
    },
    caseTypeCode: {
      type: Object,
    },
  },
  data() {
    return {
      element: [],
      type: []
    }
  },
  async mounted() {
    this.element = this.getArrayDate(this.caseDate)
    this.type = this.caseTypeCode
  },
  methods: {
    getArrayDate(value) {
      const arrayDate = []
      arrayDate.push(value)
      return arrayDate
    },
    headerClass() {
      return { background: 'rgba(236, 245, 255, 0.3)', height: '10%', padding: '3px' }
    },
    rowClass() {
      return { background: 'rgba(236, 245, 255, 0.3)', color: '#409EFF', height: '10%', padding: '3px' }
    },
    cellClass() {
      return { padding: '4px' }
    },
  },
}
</script>

<style lang="scss" scoped>
.caseInfo {
  .el-table {
    border: none;
  }
}
</style>
