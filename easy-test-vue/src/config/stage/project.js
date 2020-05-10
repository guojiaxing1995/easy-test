const projectRouter = {
  route: null,
  name: null,
  title: '工程管理',
  type: 'folder',
  icon: 'iconfont icon-caseStore',
  filePath: 'views/project/',
  order: null,
  inNav: true,
  children: [
    {
      title: '工程配置',
      type: 'view',
      name: 'projectConfig',
      route: '/project/config',
      filePath: 'views/project/ProjectConfig.vue',
      inNav: true,
      icon: 'iconfont icon-caseGroup',
      keepAlive: true,
      permission: ['工程配置'],
    },
    {
      route: '/project/list',
      name: null,
      title: '工程列表',
      type: 'tab', // 取 route 为默认加载页
      icon: 'iconfont icon-fenzu',
      filePath: 'views/case/group',
      inNav: true,
      permission: ['工程列表'],
      children: [
        {
          route: '/project/list',
          type: 'view',
          name: 'projectList',
          inNav: true,
          filePath: 'views/project/ProjectList.vue',
          title: '工程列表',
          icon: 'iconfont icon-fenzu',
          keepAlive: false,
        },
        {
          route: '/project/add',
          type: 'view',
          name: 'projectAdd',
          filePath: 'views/project/ProjectAdd.vue',
          inNav: true,
          title: '添加工程',
          icon: 'iconfont icon-add',
          keepAlive: false,
        },
      ],
    },
  ],
}

export default projectRouter
