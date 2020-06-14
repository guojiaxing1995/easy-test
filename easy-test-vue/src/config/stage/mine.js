const MineRouter = {
  route: null,
  name: null,
  title: '我的数据',
  type: 'tab',
  icon: 'iconfont icon-caseStore',
  filePath: 'views/mine/',
  order: null,
  inNav: true,
  children: [
    {
      route: '/mine/list',
      type: 'view',
      name: 'MineList',
      inNav: true,
      filePath: 'views/mine/MineList.vue',
      title: '我的数据',
      icon: 'iconfont icon-fenzu',
      keepAlive: true,
    }
  ],
}

export default MineRouter
