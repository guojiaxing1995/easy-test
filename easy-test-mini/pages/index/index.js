// index.js
// 获取应用实例
const app = getApp()

Page({
  data: {
    motto: '开启自动化测试之旅',
    username: null,
    password: null,
    userRule:[{
      required: true,
      message: "必填",
      whitespace: true
    }],
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    canIUseGetUserProfile: false,
    canIUseOpenData: wx.canIUse('open-data.type.userAvatarUrl') && wx.canIUse('open-data.type.userNickName'), // 如需尝试获取用户信息可改为false
    showBind: false,
    msgShow: false,
    loading: false
  },
  // 事件处理函数
  bindViewTap() {
    wx.switchTab({
      url: '/pages/home/home',
    })
  },
  // 用户校验 校验成功登录成功  校验失败弹出绑定账号弹框
  login(){
    var that = this;
    this.setData({loading: true});
    wx.login({
      success: function (res) {
        console.log(res)
        //用户登录凭证（有效期五分钟）
        var code = res.code;
        //调用后端，获取openid 和 session_key 
        wx.request({
          url: app.globalData.apiBase + "/cms/user/login/mini",
          method: "POST",
          header: {
            "Content-Type": "application/json"
          },
          data: {
            code: code
          },
          success: function(res){
            console.log(res)
            if(res.statusCode===404){
              that.setData({showBind: true});
              that.setData({loading: false});
            }else if(res.statusCode===200){
              // 缓存用户token
              wx.setStorageSync('access_token', res.data["access_token"])
              wx.setStorageSync('refresh_token', res.data["refresh_token"])
              that.bindViewTap();
              that.setData({loading: false});
            }else {
              const toast = that.selectComponent('#toast');
              toast.linShow({
                title: res.data["msg"],
                icon: "error",
                placement: "right"
              });
              that.setData({loading: false});
            }
          },
        })
      }
    })
  },
  usernameInput(e){
    this.setData({username: e.detail.value})
  },
  passwordInput(e){
    this.setData({password: e.detail.value})
  },
  bindUser() {
    var that = this;
    this.setData({loading: true});
    wx.login({
      success: function (res) {
        console.log(res)
        //用户登录凭证（有效期五分钟）
        var code = res.code;
        //调用后端，获取openid 和 session_key 
        wx.request({
          url: app.globalData.apiBase + "/cms/user/bind/mini",
          method: "POST",
          header: {
            "Content-Type": "application/json"
          },
          data: {
            code: code,
            username: that.data.username,
            password: that.data.password
          },
          success: function(res){
            console.log(res)
            if(res.statusCode === 201){
              const toast = that.selectComponent('#toast');
              toast.linShow({
                title: res.data["msg"],
                icon: "success",
                placement: "right"
              });
            }else {
              that.setData({showBind: true});
              const toast = that.selectComponent('#toast');
              if (typeof(res.data["msg"]) === "string") {
                toast.linShow({
                  title: res.data["msg"],
                  icon: "error",
                  placement: "right",
                  offsetY: -500
                });
              }
            }
            that.setData({loading: false});
            that.login();
          },
        })
      }
    })
  },
  onLoad() {
    if (wx.getUserProfile) {
      this.setData({
        canIUseGetUserProfile: true
      })
    }
  },
  onShow() {
    if(wx.getStorageSync('unauthorized')){
      this.setData({msgShow: true})
     }
     wx.removeStorageSync('unauthorized')
  },
  getUserProfile(e) {
    // 推荐使用wx.getUserProfile获取用户信息，开发者每次通过该接口获取用户个人信息均需用户确认，开发者妥善保管用户快速填写的头像昵称，避免重复弹窗
    wx.getUserProfile({
      desc: '展示用户信息', // 声明获取用户个人信息后的用途，后续会展示在弹窗中，请谨慎填写
      success: (res) => {
        console.log(res)
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    })
  },
  getUserInfo(e) {
    // 不推荐使用getUserInfo获取用户信息，预计自2021年4月13日起，getUserInfo将不再弹出弹窗，并直接返回匿名的用户个人信息
    console.log(e)
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  }
})
