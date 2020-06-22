const schedulerRouter = {
  route: null,
  name: null,
  title: '定时任务',
  type: 'tab',
  icon: 'iconfont icon-caseStore',
  filePath: 'views/scheduler/',
  order: 6,
  inNav: true,
  permission: ['定时任务列表'],
  children: [
    {
      route: '/scheduler/list',
      type: 'view',
      name: 'schedulerList',
      inNav: true,
      filePath: 'views/scheduler/SchedulerList.vue',
      title: '任务列表',
      icon: 'iconfont icon-fenzu',
      keepAlive: true,
    },
    {
      route: '/scheduler/add',
      type: 'view',
      name: 'schedulerAdd',
      filePath: 'views/scheduler/SchedulerAdd.vue',
      inNav: true,
      title: '添加任务',
      icon: 'iconfont icon-add',
      keepAlive: false,
      permission: ['新增定时任务'],
    },
  ],
}

export default schedulerRouter
