// pages/home/home.js
// 获取应用实例
const app = getApp()
import * as echarts from '../../ec-canvas/echarts';

Page({

  /**
   * 页面的初始数据
   */
  data: {
    ecPie: {
      //disableTouch: true,//禁止触摸事件，修复ios无法滑动
      lazyLoad: true
    },
    ecLine: {
      disableTouch: true
    },
    total: {"case":0,"mock":0,"project":0,"scheduler":0},
    today: {"case_add_count":0,"test_count":0,"test_project_count":0},
    projectData: {
      successTotal: 0,
      executeTotal: 0,
      failTotal: 0,
      currentSuccessRate: 0,
      yoyGrowth: 0,
      dayExecute: [],
      radarChart: {
        indicator: [
          { text: '成功率', max: 0 },
          { text: '用例数', max: 0 },
          { text: '执行频率', max: 0 },
          { text: '定时任务', max: 0 },
          { text: '测试人数', max: 0 }
        ],
      },
      successRate: 0,
    },
    projectList: [],
    barData: {
      xAxis: [],
      success: [],
      fail: [],
      total: []
    },
    project: {
      id: 0,
      name: '工程'
    },
    showPopup: false
  },
  showPopup(){
    this.setData({showPopup: true})
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this;
    this.getTotal();
    this.getToday();
    this.getProjects();
    var times = setInterval(function(){
      if (that.data.project["id"] != 0) {
        that.getProjectData(that.data.project["id"]);
        clearTimeout(times);
      }
    },500)
    this.pieComponnet = this.selectComponent('#mychart-dom-pie');
    this.radarComponnet = this.selectComponent('#mychart-dom-radar');
    this.barComponnet = this.selectComponent('#mychart-dom-bar');
  },
  getProjectData(pid){
    wx.showNavigationBarLoading();
    var that = this;
    wx.request({
      url: app.globalData.apiBase + `/v1/overview/project/` + pid + '?showBackend=true',
      method: "GET",
      header: {
        "Authorization": "Bearer " + wx.getStorageSync('access_token')
      },
      success: function(res){
        var result = {}
        result.successTotal = res.data.success_total
        result.executeTotal = res.data.execute_total
        result.currentSuccessRate = res.data.current_success_rate
        result.yoyGrowth = res.data.yoy_growth
        result.dayExecute = res.data.day_execute
        result.radarChart = res.data.radar_chart
        result.failTotal = res.data.execute_total - res.data.success_total
        if (res.data.execute_total === 0) {
          result.successRate = 0
        } else {
          result.successRate = (result.successTotal / result.executeTotal * 100).toFixed(2)
        }
        that.setData({projectData: result})
        that.initPie();
        that.initRadar();
        that.barDataDeal(that.data.projectData.dayExecute);
        that.initBar();
      }
    })
    wx.hideNavigationBarLoading();
  },
  timestampToTime(timestamp) {
    // 过滤时间戳，返回值mm-dd
    if (!timestamp) {
      return timestamp
    }
    const date = new Date(timestamp * 1000)
    const m = `0${date.getMonth() + 1}`
    const d = `0${date.getDate()}`
    const val = `${m.substring(m.length - 2, m.length)}-${d.substring(d.length - 2, d.length)}`
    return val
  },
  barDataDeal(data) {
    this.data.barData.xAxis = []
    this.data.barData.success = []
    this.data.barData.fail = []
    this.data.barData.total = []
    for (let index = 0; index < data.length; index++) {
      this.data.barData.xAxis.push(this.timestampToTime(data[index].create_time / 1000))
      this.data.barData.success.push(data[index].success)
      this.data.barData.fail.push(data[index].fail)
      this.data.barData.total.push(data[index].total)
    }
  },
  getProjects(){
    var that = this;
    wx.request({
      url: app.globalData.apiBase + "/v1/project?showBackend=true",
      method: "GET",
      header: {
        "Authorization": "Bearer " + wx.getStorageSync('access_token')
      },
      success: function(res){
        that.setData({projectList: res.data})
        if (JSON.stringify(res.data)!=="{}") {
          that.setData({project: {id :res.data[0]['id'], name: res.data[0]['name']}})
        }
      }
    })
  },
  getTotal(){
    var that = this;
    wx.request({
      url: app.globalData.apiBase + "/v1/overview/total?showBackend=true",
      method: "GET",
      header: {
        "Authorization": "Bearer " + wx.getStorageSync('access_token')
      },
      success: function(res){
        if (res.statusCode === 401 || res.statusCode === 422) {
          wx.setStorageSync('unauthorized', true)
          wx.redirectTo({
            url: '/pages/index/index',
          })
        }
        that.setData({total: res.data})
      }
    })
  },
  getToday(){
    var that = this;
    wx.request({
      url: app.globalData.apiBase + "/v1/overview/today?showBackend=true",
      method: "GET",
      header: {
        "Authorization": "Bearer " + wx.getStorageSync('access_token')
      },
      success: function(res){
        that.setData({today: res.data})
      }
    })
  },
  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    var that = this;
    this.getTotal();
    this.getToday();
    this.getProjects();
    var times = setInterval(function(){
      if (that.data.project["id"] != 0) {
        that.getProjectData(that.data.project["id"]);
        clearTimeout(times);
      }
    },500)
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },
  chooseProject(e){
    console.log(e.currentTarget.dataset)
    this.getProjectData(e.currentTarget.dataset.project.id);
    this.setData({
      showPopup: false, 
      project: {
        id: e.currentTarget.dataset.project.id,
        name: e.currentTarget.dataset.project.name
      }
    });
  },
  initBar(){
    this.barComponnet.init((canvas, width, height, dpr) => {
      const that = this
      // 初始化图表
      const Chart = echarts.init(canvas, null, {
        width: width,
        height: height,
        devicePixelRatio: dpr
      });
      var option = {
        title: {
          text: '近7次执行',
          textStyle: {
            fontSize: 12,
            color: '#4577ff'
          }
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['成功数', '失败数', '总用例数']
        },
        toolbox: {
          show: true,
          feature: {
            magicType: { show: true, type: ['line', 'bar'] },
          }
        },
        calculable: true,
        xAxis: [
          {
            type: 'category',
            data: that.data.barData.xAxis
          }
        ],
        yAxis: [
          {
            type: 'value'
          }
        ],
        series: [
          {
            name: '成功数',
            itemStyle: {
              color: '#00C292'
            },
            type: 'bar',
            data: that.data.barData.success,
            markPoint: {
              data: [
                { type: 'max', name: '最大值' },
                { type: 'min', name: '最小值' }
              ]
            },
            markLine: {
              data: [
                { type: 'average', name: '平均值' }
              ]
            }
          },
          {
            name: '失败数',
            itemStyle: {
              color: '#E46A76'
            },
            type: 'bar',
            data: that.data.barData.fail,
            markPoint: {
              data: [
                { type: 'max', name: '最大值' },
                { type: 'min', name: '最小值' }
              ]
            },
            markLine: {
              data: [
                { type: 'average', name: '平均值' }
              ]
            }
          },
          {
            name: '总用例数',
            itemStyle: {
              color: '#4577ff'
            },
            type: 'bar',
            data: that.data.barData.total,
            markPoint: {
              data: [
                { type: 'max', name: '最大值' },
                { type: 'min', name: '最小值' }
              ]
            },
            markLine: {
              data: [
                { type: 'average', name: '平均值' }
              ]
            }
          },
        ]
      }
      Chart.setOption(option);
      return Chart;
    });
  },
  initRadar(){
    this.radarComponnet.init((canvas, width, height, dpr) => {
      const that = this
      // 初始化图表
      const Chart = echarts.init(canvas, null, {
        width: width,
        height: height,
        devicePixelRatio: dpr
      });
      var option = {
        radar: [
          {
            indicator: that.data.projectData.radarChart.indicator,
            center: ['45%', '50%'],
            radius: 40,
          }
        ],
        series: [
          {
            name: '工程分析',
            type: 'radar',
            data: [
              {
                value: that.data.projectData.radarChart.value,
                name: 'project',
                areaStyle: {
                  opacity: 0.7,
                  color: '#4577ff'
                }
              }
            ]
          }
        ]
      }
      Chart.setOption(option);
      return Chart;
    });
  },
  initPie(){
    this.pieComponnet.init((canvas, width, height, dpr) => {
      const that = this
      // 初始化图表
      const Chart = echarts.init(canvas, null, {
        width: width,
        height: height,
        devicePixelRatio: dpr
      });
      var option = {
        tooltip: {
          trigger: 'item',
          formatter: '{b} : {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 10,
          data: ['成功', '失败']
        },
        graphic: [{
          type: 'text',
          left: 'center',
          top: '50%',
          style: {
            text: `总成功率\n${that.data.projectData.successRate}%`,
            textAlign: 'center',
            fill: '#4577ff',
            width: 30,
            height: 30,
            fontSize: 12,
            fontWeight: 'bold'
          }
        }],
        series: [
          {
            name: '测试结果占比',
            type: 'pie',
            radius: ['40%', '70%'],
            center: ['50%', '55%'],
            avoidLabelOverlap: false,
            label: {
              show: false,
              position: 'center'
            },
            data: [
              { value: that.data.projectData.successTotal, name: '成功', itemStyle: { color: '#00C292' } },
              { value: that.data.projectData.failTotal, name: '失败', itemStyle: { color: '#E46A76' } },
            ],
            emphasis: {
              // label: {
              //   show: true,
              //   fontSize: '30',
              //   fontWeight: 'bold'
              // },
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
      Chart.setOption(option);
      return Chart;
    });
  },
  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})