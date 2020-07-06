const analysisRouter = {
  route: '/analysis/case',
  name: 'analysis',
  title: '用例分析',
  type: 'view', // 类型: folder, tab, view
  icon: 'iconfont icon-analysis',
  filePath: 'views/analysis/CaseAnalysis.vue', // 文件路径
  order: 7,
  inNav: true,
  keepAlive: true,
  permission: ['用例分析'],
}

export default analysisRouter
