Page({

  /**
   * 页面的初始数据
   */
  data: {
    'department': "",
    'id': "",
    'name': "",
    input:{
      'phone': '',
      'email': ''
    }
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    console.log("fillUserInfo获取传来的用户信息：", options)
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
  // enterProject:function(e){
  //     console.log(e.currentTarget.id)
  //     wx.navigateTo({"url":"/pages/project/project?projectID="+e.currentTarget.id})

  // },

  onValueChanged: function (e) {
    let dataset = e.currentTarget.dataset
    //data-开头的是自定义属性，可以通过dataset获取到，dataset是一个json对象，有obj和item属性，可以通过这两个实现双向数据绑定，通过更改这两个值，对不同name的变量赋值
    let value = e.detail.detail.value;
    this.data.input[dataset.item] = value
    this.setData({
      input: this.data.input
    })
  },

  onSubmit: function () {
    var that = this
    // console.log("fillUserInfo.js: formSubmit函数开始", e.detail.value)

    // 检测用户是否填写完全信息
    if (this.data.input.phone.length && this.data.input.email.length) {
      let app = getApp();
      const userUrl = `${app.globalData.backEndUrl}/auth/user`
      console.log('fillUserInfo中formSubmit函数，cookie为：', app.globalData.cookies)
      // 向后端发送填写信息请求
      wx.request({
        url: userUrl,
        method: 'post',// 请求方式
        data: { // 想接口提交的数据
          'name': that.data.name,
          'id': that.data.id,
          'department': that.data.department,
          'email': that.data.input.email,
          'phone': that.data.input.phone
        },
        header: {
          'content-type': 'application/json',// 提交的数据类型
          'cookie': app.globalData.cookies //读取cookie
        },
        success(res) {  // 成功回调
          console.log('填写用户信息向后端发送请求成功', res.data);
          if (res.statusCode == 200) {
            wx.reLaunch({
              url: '/pages/home/home',
            })
          }
          else{
            wx.showModal({
              title: '错误',
              content: '手机号或邮箱格式有误',
              success(res) {
                if (res.confirm) {
                  console.log('用户点击确定')
                } else if (res.cancel) {
                  console.log('用户点击取消')
                }
              }
            })
          }

        },
        fail() { // 失败回调
          console.log('填写用户信息向后端发送数据失败！');
        }
      })
    }
    else {
      wx.showModal({
        title: '提示',
        content: '请输入手机号和邮箱',
        success(res) {
          if (res.confirm) {
            console.log('用户点击确定')
          } else if (res.cancel) {
            console.log('用户点击取消')
          }
        }
      })
    }
  }
})