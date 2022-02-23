// pages/case/case.js
const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    showPopup: false,
    caseGroups: [],
    group: {
      id: 0,
      name: null
    },
    showCaseList: true,
    showNoData: false,
    caseName: '',
    page: 1,
    pages: 1,
    caseList: [],
    loadmoreShow: false,
    loadmoreType: "loading"
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.caseGroup()
  },
  clickGroup(e){
    this.setData({page: 1, group: e.currentTarget.dataset.group,showPopup: false})
    this.setData({loadmoreShow: false})
    this.caseList()
  },
  showCaseGroup() {
    this.setData({showPopup: true})
  },
  caseGroup() {
    wx.showNavigationBarLoading();
    this.setData({loadmoreShow: false})
    var that = this;
    wx.request({
      url: app.globalData.apiBase + "/v1/caseGroup?showBackend=true",
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
        }else{
          that.setData({caseGroups: res.data, page: 1})
          if (JSON.stringify(res.data)!=="{}") {
            that.setData({group: {id :res.data[0]['id'], name: res.data[0]['name']}})
          }
          that.caseList()
        }
      }
    })
    wx.hideNavigationBarLoading();
  },
  caseList(){
    var that = this;
    this.setData({showCaseList: false})
    wx.request({
      url: app.globalData.apiBase + "/v1/case?showBackend=true&count=15&caseGroup=" + this.data.group.id + "&name=" + this.data.caseName + "&page=" + this.data.page,
      method: "GET",
      header: {
        "Authorization": "Bearer " + wx.getStorageSync('access_token')
      },
      success: function(res){
        that.setData({caseList: res.data.data, page: res.data.page, pages: res.data.pages})
        that.setData({showCaseList: true})
        if (that.data.showCaseList && JSON.stringify(that.data.caseList)==='[]') {
          that.setData({showNoData: true})
        }else{
          that.setData({showNoData: false})
        }
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
  onGoToDetail(e){
    wx.navigateTo({
      url: '/pages/case-detail/case-detail?cid=' + e.currentTarget.dataset.case.id,
    })
  },
  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
    var that = this
    this.setData({page: this.data.page + 1, loadmoreShow: true, loadmoreType: "loading"})
    if (this.data.page < this.data.pages + 1) {
      wx.request({
        url: app.globalData.apiBase + "/v1/case?showBackend=true&count=15&caseGroup=" + this.data.group.id + "&name=" + this.data.caseName + "&page=" + this.data.page,
        method: "GET",
        header: {
          "Authorization": "Bearer " + wx.getStorageSync('access_token')
        },
        success: function(res){
          that.setData({caseList: that.data.caseList.concat(res.data.data),
             page: res.data.page, 
             pages: res.data.pages,
             loadmoreShow: false
            })
        }
      })
    } else {
      that.setData({loadmoreType: "end", loadmoreShow: true})
    }
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },
  confirm(e) {
    this.setData({caseName: e.detail.value, page: 1, loadmoreShow: false})
    this.caseList()
  },
  linblur(e) {
    this.setData({caseName: e.detail.value, page: 1})
  },
  clear() {
    this.setData({caseName: '', page: 1, loadmoreShow: false})
    this.caseList()
  }
})