Page({

  /**
   * 页面的初始数据
   */
  data: {
    "type": "ALL",
    "records": []
  },

  /*
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    console.log("viewMyProject页面加载： ", options)
    let title = {
      'ALL': '所有项目',
      'CHECKING': '待审核项目',
      'CURRENT': '进行中项目',
      'HISTORY': '已完成项目'
    }[options.type]
    wx.setNavigationBarTitle({
      title: title
    })

    
    this.setData(options)
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
    
    let that = this;
    var app = getApp()
    let urlWhole = "null"
    if (that.data.type == "ALL") {
      urlWhole = `${app.globalData.backEndUrl}/my/allrecord`
    }
    else if (that.data.type == "CHECKING") {
      urlWhole = `${app.globalData.backEndUrl}/my/applyrecord`
    }
    else if (that.data.type == "CURRENT") {
      urlWhole = `${app.globalData.backEndUrl}/my/processrecord`
    }
    else if (that.data.type == "HISTORY") {
      urlWhole = `${app.globalData.backEndUrl}/my/historyrecord`
    }

    console.log("viewMyProject得到完整URL：", urlWhole)
    wx.request({
      url: urlWhole,
      method: 'get',
      header: {
        'content-type': 'application/json', // 提交的数据类型
        'cookie': app.globalData.cookies //读取cookie
      },
      success(res) {  // 成功回调
        console.log("得到的数据为", res)
        that.setData({
          "records": res.data
        })
      },
      fail() { // 失败回调
        console.log('向后端发送数据失败！');
        wx.showModal({
          title: '错误',
          content: '无法发送数据，请检查网络状态'
        })
      }
    })
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
  
  enterProject: function (e) {
    //console.log("-------"+e.currentTarget.id)
    console.log("viewMyProject this.data.type:",this.data.type)
    if(this.data.type == "CURRENT")
    {
      wx.navigateTo({ "url": "/pages/currentproject/currentproject?projectID=" + e.currentTarget.id })
    }
    else
    {
      wx.navigateTo({ "url": "/pages/project/project?projectID=" + e.currentTarget.id })
    }
    
  },
  comment:function(e){
    let dataset = e.currentTarget.dataset
    console.log("点击了评价按钮！,dataset:", dataset)
    wx.navigateTo({ "url": "/pages/comment/comment?joinrecordid=" + dataset.joinrecordid + '&title='+dataset.title })
  },
  worktimeprove:function(e){
    let dataset = e.currentTarget.dataset
    console.log("点击了评价按钮！,dataset:", dataset)
    wx.navigateTo({ "url": "/pages/worktimeprove/worktimeprove?title="+dataset.title + "&worktime="+dataset.worktime})
  }
})