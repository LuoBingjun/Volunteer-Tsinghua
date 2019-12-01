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
  onShareAppMessage: function () {

  }
})