// pages/login.js
Page({

  /**
   * 页面的初始数据
   */
  data: {

  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) 
  {
    console.log("login界面onLoad完成")
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
    var that = this;
    console.log("login界面onShow开始")

    /*
    var app=getApp();
    const loginUrl = `${app.globalData.backEndUrl}/auth/login`
    console.log("得到URL：",url)

    wx.request({
      url: loginUrl,
      method: 'post',// 请求方式
      data: { // 想接口提交的数据
        'token':token
      },
      header: {
        'content-type': 'application/json'// 提交的数据类型
      },
      success(res) {  // 成功回调
        console.log('向后端发送数据成功！', res.data);
        // res.data 包含了后端传回的学号等信息。

      },
      fail() { // 失败回调
        console.log('向后端发送数据失败！');
      }
    })

    */
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

  kindToggle: function (e) {
    console.log("ok!!")
    wx.switchTab({"url":"/pages/home/home"})
  },
  onLoginPushed: function(e){
    //  跳转到助教“清华人”小程序
    wx.navigateToMiniProgram(    
      {   
        "appId": "wx1ebe3b2266f4afe0",
        "path": "pages/index/index",
        "envVersion": "trial",
        "extraData": 
          {    
            "origin": "miniapp",
            "type": "id.tsinghua"
          },
          success(res) {
            console.log("跳转到助教小程序成功！", res)
          },
          fail(res){
            console.log("跳转到助教小程序失败！", res)
          }
      } 
    )
  }
})