Page({
  /**
   * 页面的初始数据
   */
  data: {
    current: "me",
    userInfo: {
      department: "一二三学院",
      id: "12345678",
      name: "哈哈哈",
      email: "lbj17@mails.tsinghua.edu.cm",
      phone: "13888888888"
    }
  },

  handleChange({ detail }) {
    if (detail.key != this.data.current) {
      this.setData({
        current: detail.key
      });
      wx.reLaunch({
        url: `/pages/${detail.key}/${detail.key}`,
      })
    }
  },

  /*
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this;
    var app = getApp()
    that.setData({
      userInfo: app.globalData.userInfo
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
    console.log("ok2!!!")
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
  onShareAppMessage: function (res) {
    return {
        path: '/pages/login/login'
    }

  },
  changeInfo: function(){
    wx.navigateTo({ "url": "/pages/changeUserInfo/changeUserInfo"})
  },
  unbundling:function(){
    console.log("unbundling函数触发！")
    var that = this
    var app = getApp()
    wx.showModal({
      title: '用户解绑',
      content: '您确定要解绑此学号吗？',
      confirmText: "我再想想",
      cancelText: "解绑",
      success: function (res) {
        console.log(res);
        if (res.confirm) {
          console.log('用户点击我再想想')
        } else {
          console.log('用户点击解绑')


          wx.request({
            url: `${app.globalData.backEndUrl}/auth/unbundling`,
            method: 'post',
            header: {
              'content-type': 'application/json', // 提交的数据类型
              'cookie': app.globalData.cookies //读取cookie
            },
            data: {
            },
            success(res) {  // 成功回调
              console.log("得到的数据为", res);
              if (res.statusCode == 200) {
                wx.showToast({
                  title: "已成功解绑",
                  icon: "success",
                  duration: 2000
                });
                setTimeout(function () {
                  console.log("返回登录");
                  wx.reLaunch({
                    url: `/pages/login/login`
                  })
                }, 2000);
              }
              else {
                wx.showModal({
                  title: '错误',
                  content: res.data.error,
                });
              }
            },
            fail() { // 失败回调
              wx.showModal({
                title: '错误',
                content: '无法发送数据，请检查网络状态'
              });
            }
          })
        }
      }
    });
  }
})