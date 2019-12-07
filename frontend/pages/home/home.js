Page({

  /**
   * 页面的初始数据
   */
  data: {
    current: 'home',
    "username": "FTP server",
    "projects": [
      {
        "id": 1,
        "cover": "封面图片url",
        "title": "标题",
        "content": "内容",
        "introduction":"简介",
        "require_num": 5, // "需求人数"
        "requirements": "需求",
        "form": "表单",
        "time": "发起时间",
        "deadline": "截止时间"
      },
    ],
    "searchbar": true,
    inputShowed: false,
    inputVal: ""
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

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this
    var app = getApp()
    let isIphoneX = app.globalData.isIphoneX;
    console.log("主页：isIphoneX:", isIphoneX)
    this.setData({
      isIphoneX: isIphoneX
    })

    wx.request({
      url: `${app.globalData.backEndUrl}/project/list`,
      method: 'get',
      header: {
        'content-type': 'application/json', // 提交的数据类型
        'cookie': app.globalData.cookies //读取cookie
      },
      success(res) {  // 成功回调
        console.log("得到的数据为", res)
        that.setData({
          "projects": res.data
        })
      },
      fail() { // 失败回调
        console.log('向后端发送数据失败！');
      }
    })

    // 请求用户信息：
    wx.request({
      url: `${app.globalData.backEndUrl}/auth/user`,
      method: 'get',
      header: {
        'content-type': 'application/json', // 提交的数据类型
        'cookie': app.globalData.cookies //读取cookie
      },
      success(res) {  // 成功回调
        console.log("home.js 获取用户信息：", res.data)
        app.globalData.userInfo = JSON.parse(JSON.stringify(res.data))
        that.setData({
          "username": app.globalData.userInfo.name,
        })
      },
      fail() { // 失败回调
        console.log('向后端发送数据失败！');
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


  showInput: function () {
    this.setData({
      inputShowed: true
    });
  },
  hideInput: function () {
    this.setData({
      inputVal: "",
      inputShowed: false
    });
  },
  clearInput: function () {
    this.setData({
      inputVal: ""
    });
  },
  inputTyping: function (e) {
    this.setData({
      inputVal: e.detail.value
    });
  }
})