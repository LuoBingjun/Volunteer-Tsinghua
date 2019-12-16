Page({

  /**
   * 页面的初始数据
   */
  data: {
//     department: "软件学院"
// email: "yfthu@outlook.com"
// id: "2017010862"
// name: "杨帆"
// openid: "o0DCq5aq5gkSCcbp0iZsO-9iQDfs"
// phone: "18810063756"
// title: "北京南站志愿项目志愿者"
// worktime: "0"
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var app = getApp()
    console.log("worktimeprove获取传来的信息：", options)
    this.setData(options)
    // title: "北京南站志愿项目志愿者"
    // worktime: "0"
    this.setData(app.globalData.userInfo)
    console.log("worktimeProve this.data:",this.data)
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
  onShareAppMessage: function (res) {
    return {
        path: '/page/login/login'
    }

  }
})