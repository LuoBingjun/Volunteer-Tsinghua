Page({

  /**
   * 页面的初始数据
   */
  data: {
    current: "message",
    "name": "FTP server",
    "messages":[
      {"projectName": "献血志愿者", "messageTitle": "8点开始献血！！！"},
      {"projectName": "校园讲解志愿者", "messageTitle": "后天培训会取消！！！"},
      {"projectName": "pn1rqwr", "messageTitle": "please qiandao3!"},
    ]
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

  },

  enterProject: function (e) {
    //console.log("-------"+e.currentTarget.id)
    wx.navigateTo({ "url": "/pages/project/project?projectID=" + e.currentTarget.id })
  },
})