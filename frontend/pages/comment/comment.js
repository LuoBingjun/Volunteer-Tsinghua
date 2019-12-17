Page({

  /**
   * 页面的初始数据
   */
  data: {
    input:{
      'starIndex': 0,
      'textcomment':''      
    }
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    console.log("comment获取传来的信息：", options)
    // joinrecordid: "10"
    // title: "北京南站志愿项目志愿者"
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
  // enterProject:function(e){
  //     console.log(e.currentTarget.id)
  //     wx.navigateTo({"url":"/pages/project/project?projectID="+e.currentTarget.id})

  // },
  onRateChange(e){
    const index = e.detail.index;
    this.data.input.starIndex = index
    this.setData({
      input: this.data.input
    })
    console.log("用户进行了评分：",this.data.input.starIndex)
},
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

    let app = getApp();
    const commentUrl = `${app.globalData.backEndUrl}/my/comment`
    wx.request({
      url: commentUrl,
      method: 'post',// 请求方式
      data: { // 想接口提交的数据
        "join_record_id":this.data.joinrecordid,
        "comment":this.data.input.textcomment,
        "comment_rank":this.data.input.starIndex
      },
      header: {
        'content-type': 'application/json',// 提交的数据类型
        'cookie': app.globalData.cookies //读取cookie
      },
      success(res) {  // 成功回调
        console.log("得到的数据为", res);
        if (res.statusCode == 200) {
          wx.showToast({
            title: "评价成功",
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