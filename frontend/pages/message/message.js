Page({

  /**
   * 页面的初始数据
   */
  data: {
    current: "message",
    "name": "FTP server",
  //   "messages":[
  //     {
  //         "id": 1,
  //         "type": "P", // ('M', '模板消息'), ('P', '普通消息')
  //         "title": "测试项目",
  //         "content": "测试内容内容内容内容内容内容内容内容",
  //         "sender": {
  //             "description": '组织名称'
  //         },
  //         "project": {
  //             "id": 1,
  //             "title": "测试项目",
  //         }
  //     },
  //     {
  //         "id": 1,
  //         "type": "M", // ('M', '模板消息'), ('P', '普通消息')
  //         "title": "测试项目",
  //         "content": [{"key":"签到时间", "value":"2019-12-02"},{"key":"签到地点", "value":"6A305"}],
  //         "sender": {
  //             "description": '组织名称'
  //         },
  //         "project": {
  //             "id": 1,
  //             "title": "测试项目",
  //         }
  //     }
  // ]
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
    var that = this
    var app = getApp()

    wx.request({
      url: `${app.globalData.backEndUrl}/my/messages`,
      method: 'get',
      header: {
        'content-type': 'application/json', // 提交的数据类型
        'cookie': app.globalData.cookies //读取cookie
      },
      success(res) {  // 成功回调
        console.log("得到的数据为", res)

        for(var item of res.data)
        {
          if(item.type == 'M')
          {
            item.content = JSON.parse(item.content.replace(/\s+/g, ""))
          }
        }

        that.setData({
          "messages": res.data
        })
        

        console.log("解析后的messages请求：",that.data.messages)
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
    console.log("-------"+e.currentTarget.projectID)
    wx.navigateTo({ "url": "/pages/currentproject/currentproject?projectID=" + e.currentTarget.projectID })
  },
})