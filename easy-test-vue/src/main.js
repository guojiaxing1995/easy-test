import '@babel/polyfill'
import Vue from 'vue'
import ElementUI from 'element-ui'

import VueCodemirror from 'vue-codemirror'


import '@/lin/mixin'
import '@/lin/filter'
import '@/lin/plugins'
import '@/lin/directives'

import echarts from 'echarts'

import xss from 'xss'

import VueSocketIO from 'vue-socket.io'
import CollapseTransition from 'element-ui/lib/transitions/collapse-transition'
import router from '@/router'
import store from '@/store'
import App from '@/App.vue'

import StickyTop from '@/components/base/sticky-top/sticky-top'
import LIcon from '@/components/base/icon/lin-icon'
import SourceCode from '@/components/base/source-code/source-code'

import '@/assets/styles/index.scss' // eslint-disable-line
import '@/assets/styles/realize/element-variables.scss'
import 'element-ui/lib/theme-chalk/display.css'

/* eslint-disable*/
import 'codemirror/lib/codemirror.css'

Vue.prototype.$echarts = echarts
Vue.prototype.$xss = xss

Vue.config.productionTip = false

Vue.use(ElementUI)

Vue.use(VueCodemirror)

Vue.component(CollapseTransition.name, CollapseTransition)

// base 组件注册
Vue.component('sticky-top', StickyTop)
Vue.component('l-icon', LIcon)
Vue.component('source-code', SourceCode)

Vue.use(new VueSocketIO({
  debug: true,
  connection: process.env.VUE_APP_SOCKETIO_URL,
  // connection: 'http://127.0.0.1:5000/',
}))

/* eslint no-unused-vars: 0 */
const AppInstance = new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')

// 设置 App 实例
window.App = AppInstance
