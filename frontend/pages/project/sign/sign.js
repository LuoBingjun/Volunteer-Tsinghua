Page({
  /**
   * 页面的初始数据
   */
  data: {
    projectID: 0,
    list: {},
    activeNames: []
  },
  onChange(event) {
    this.setData({
      activeNames: event.detail
    });
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    console.log("选项：", options)
    this.setData({ 'projectID': options.projectID })
    let app = getApp()
    let that = this
    wx.request({
      url: `${app.globalData.backEndUrl}/sign/list?project=${this.data.projectID}`,
      method: 'get',
      header: {
        'content-type': 'application/json', // 提交的数据类型
        'cookie': app.globalData.cookies //读取cookie
      },
      success(res) {  // 成功回调
        console.log("得到的数据为", res);

        if (res.statusCode == 200) {
          let list = {}
          that.reslen = res.data.length
          for (let item of res.data) {
            list[item.id] = item

            let now = new Date()
            item.begin_time = new Date(item.begin_time)
            item.end_time = new Date(item.end_time)
            if (now.getTime() < item.begin_time.getTime()) {
              item.status = 3
            }
            else if (now.getTime() > item.end_time.getTime()) {
              item.status = 0
            }
            else {
              that.data.activeNames.push(item.id)
              that.setData({
                activeNames: that.data.activeNames
              })

              item.status = 1
              wx.request({
                url: `${app.globalData.backEndUrl}/my/signrecord?signproject=${item.id}`,
                method: 'get',
                header: {
                  'content-type': 'application/json', // 提交的数据类型
                  'cookie': app.globalData.cookies //读取cookie
                },
                success(res2) {
                  console.log(res2)
                  if (res2.statusCode == 200) {
                    list[res2.data.sign_project].status = 2
                    that.setData({ 'list': list })
                  }
                  else if (res2.statusCode != 404) {
                    wx.showModal({
                      title: '错误',
                      content: JSON.stringify(res2.data),
                    });
                  }
                },
                fail() { // 失败回调
                  wx.showModal({
                    title: '错误',
                    content: '无法发送数据，请检查网络状态（也有可能是我们服务器挂了）'
                  });
                  that.setData({ 'list': [] })
                }
              })
            }
            item.begin_time = item.begin_time.Format("yyyy-MM-dd HH:mm:ss")
            item.end_time = item.end_time.Format("yyyy-MM-dd HH:mm:ss")
          }
          that.setData({
            list: list
          });
          // console.log(list)
          // setTimeout(function () { console.log(that.data.list) }, 1000)
        }
        else {
          wx.showModal({
            title: '错误',
            content: JSON.stringify(res.data),
          });
        }

      },
      fail() { // 失败回调
        wx.showModal({
          title: '错误',
          content: '无法发送数据，请检查网络状态（也有可能是我们服务器挂了）'
        });
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
  onShow: function (options) {

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

  },

  // switchOpen: function (e) {
  //   var id = e.currentTarget.id
  //   var list = this.data.list
  //   console.log("拿到的id", id)
  //   list[id].open = list[id].open == 'true' ? 'false' : 'true'
  //   console.log("修改后：", list)
  //   this.setData({ 'list': list })
  // },

  sign: function (e) {
    if (this.data.disabled) return;
    var app = getApp();
    console.log(e.currentTarget)
    var that = this
    wx.request({
      url: `${app.globalData.backEndUrl}/sign/signin`,
      method: 'post',
      header: {
        'content-type': 'application/json', // 提交的数据类型
        'cookie': app.globalData.cookies //读取cookie
      },
      data: {
        'sign_project': e.currentTarget.id
      },
      success(res) {  // 成功回调
        console.log("得到的数据为", res);
        if (res.statusCode == 200) {
          that.setData({ 'disabled': true })
          wx.showToast({
            title: "签到成功",
            icon: "success",
            duration: 2000
          });
          setTimeout(function () {
            console.log("返回主界面");
            wx.navigateBack();
          }, 2000);
        }
        else {
          wx.showModal({
            title: '错误',
            content: JSON.stringify(res.data),
          });
        }
      },
      fail() { // 失败回调
        wx.showModal({
          title: '错误',
          content: '无法发送数据，请检查网络状态（也有可能是我们服务器挂了）'
        });
      }
    })
  }
})