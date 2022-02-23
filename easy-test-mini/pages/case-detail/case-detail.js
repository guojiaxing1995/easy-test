// pages/case-detail/case-detail.js
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    detail: {}
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.getType()
    console.log(options)
    this.getDetail(options.cid)
    this.getCollect(options.cid)
  },
  getCollect(cid) {
    var that = this;
    wx.request({
      url: app.globalData.apiBase + '/v1/case/collect/' + cid,
      method: "GET",
      header: {
        "Authorization": "Bearer " + wx.getStorageSync('access_token')
      },
      success: function(res){
        that.setData({collect: res.data})
      }
    })
  },
  getType() {
    var that = this;
    wx.request({
      url: app.globalData.apiBase + '/v1/case/type',
      method: "GET",
      header: {
        "Authorization": "Bearer " + wx.getStorageSync('access_token')
      },
      success: function(res){
        that.setData({type: res.data})
      }
    })
  },
  getDetail(cid) {
    var that = this;
    wx.request({
      url: app.globalData.apiBase + `/v1/case?id=` + cid,
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
        that.setData({detail: res.data.data[0]})
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

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})