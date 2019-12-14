Page({

  /**
   * 页面的初始数据
   */
  data: {
    current: 'home',
    projectsKind: 0,
    showLeft1: false,
    username: undefined,
    projects: []/*[
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
    ]*/,
    inputShowed: false,
    inputVal: "",
    page:0,
    type:0,
    lastPage: false,
    loadingPage: false,
    typeText: "按标签筛选"
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
  updateList(){
    var that = this
    var app = getApp()
    let isIphoneX = app.globalData.isIphoneX;
    console.log("主页：isIphoneX:", isIphoneX)
    this.setData({
      isIphoneX: isIphoneX
    })
    this.setData({
      page:this.data.page+1
    })
    
    var typeParam=""
    if(this.data.type==1)typeParam="&type=WH"
    else if(this.data.type==2)typeParam="&type=SH"
    else if(this.data.type==3)typeParam="&type=SQ"
    else if (this.data.type==4)typeParam="&type=YL"
    else if (this.data.type==5)typeParam="&type=JK"
    else if (this.data.type==6)typeParam="&type=XY"
    else if (this.data.type==7)typeParam="&type=QT"

    var searchParam=""
    if(this.data.inputVal.length>0)searchParam=`&search=${this.data.inputVal}`
    
    var getUrl=`${app.globalData.backEndUrl}/project/list?page=${this.data.page}${typeParam}${searchParam}`
    console.log("请求页面，url为",getUrl)

    this.setData({loadingPage:true})
    setTimeout(
      function(){
            wx.request({
          url: getUrl,
          method: 'get',
          header: {
            'content-type': 'application/json', // 提交的数据类型
            'cookie': app.globalData.cookies //读取cookie
          },
          success(res) {  // 成功回调
            if(res.statusCode==200)
            {
              console.log("得到的数据为", res)
              that.setData({
                projects: that.data.projects.concat(res.data.results),
                lastPage: res.data.next===null,
                loadingPage: false
              })
            }
            else if(res.statusCode==404)
            {
              console.log("无数据")
              that.setData({
                lastPage: true,
                loadingPage: false
              })
            }
          },
          fail() { // 失败回调
            console.log('向后端发送数据失败！');
            that.setData({loadingPage:false})
          }
        })
      },100
    )
  },

  onLoad: function (options) {
    let app = getApp()
    let that = this
    this.updateList()
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
    console.log("pull down")
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
    if(!this.data.lastPage)
      this.updateList()
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
  },
  showKinds() {
    this.setData({
        showLeft1: !this.data.showLeft1
    });
  },
  kindChange(event) {
    console.log(event)
    var typeText="按标签筛选"
    if(event.detail==1)typeText="文化教育"
    else if(event.detail==2)typeText="赛会服务"
    else if(event.detail==3)typeText="社区服务"
    else if(event.detail==4)typeText="医疗卫生"
    else if(event.detail==5)typeText="健康残障"
    else if(event.detail==6)typeText="校园讲解"
    else if(event.detail==7)typeText="其他项目"

    this.setData({
      showLeft1: false,
      type:event.detail,
      page:0,
      lastPage:false,
      projects:[],
      typeText:typeText
    });
    this.updateList()
    wx.showToast({
      icon: 'none',
      title: `切换至第${event.detail}项`
    });
  }
})