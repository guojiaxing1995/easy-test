const caseRouter = {
  route: null,
  name: null,
  title: '用例管理',
  type: 'folder',
  icon: 'iconfont icon-caseStore',
  filePath: 'views/admin/',
  order: null,
  inNav: true,
  permission: ['测试用例'],
  children: [
    {
      route: null,
      name: null,
      title: '测试用例',
      type: 'folder', // 取 route 为默认加载页
      icon: 'iconfont icon-caseStore',
      filePath: 'views/case/case/',
      inNav: true,
      children: [
        {
          title: '用例列表',
          type: 'view',
          name: 'CaseList',
          route: '/case/case/list',
          filePath: 'views/case/case/CaseList.vue',
          inNav: true,
          icon: 'iconfont icon-caseGroup',
          keepAlive: true,
          permission: ['测试用例'],
        },
        {
          title: '添加用例',
          type: 'view',
          inNav: true,
          route: '/case/case/add',
          icon: 'iconfont icon-add',
          name: 'CaseAdd',
          filePath: 'views/case/case/CaseAddOrEdit.vue',
          permission: ['新增用例'],
        },
      ],
    },
    {
      route: '/case/group/list',
      name: null,
      title: '分组管理',
      type: 'tab', // 取 route 为默认加载页
      icon: 'iconfont icon-fenzu',
      filePath: 'views/case/group',
      inNav: true,
      permission: ['用例分组'],
      children: [
        {
          route: '/case/group/list',
          type: 'view',
          name: 'groupList',
          inNav: true,
          filePath: 'views/case/group/GroupList.vue',
          title: '分组列表',
          icon: 'iconfont icon-fenzu',
          keepAlive: false,
        },
        {
          route: '/case/group/add',
          type: 'view',
          name: 'groupAdd',
          filePath: 'views/case/group/GroupAdd.vue',
          inNav: true,
          title: '添加分组',
          icon: 'iconfont icon-add',
          keepAlive: false,
        },
      ],
    },
  ],
}

export default caseRouter
