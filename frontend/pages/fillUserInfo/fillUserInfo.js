Page({

    /**
     * 页面的初始数据
     */
    data: {
        'department': "一二三学院",
        'id': "1234567438",
        'name': "哈哈哈",

        "projects":[
            {"name": "我是一个项目","description":"没有描述","projectID":123, "imageUrl": "/src/img2.jpg"},
            {"name": "我也是一个项目","description":"懒得描述","projectID":143, "imageUrl": ""},
            {"name": "我不是一个项目","description":"上面那句话是假话","projectID":179, "imageUrl": ""}
        ],
        "searchbar":false
    },
  
    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        console.log("fillUserInfo获取传来的用户信息：",options)
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
    enterProject:function(e){
        console.log(e.currentTarget.id)
        wx.navigateTo({"url":"/pages/project/project?projectID="+e.currentTarget.id})
        
    },
    formSubmit: function(e){
        var that = this
        
        console.log("fillUserInfo.js: formSubmit函数开始", e.detail.value)
        let {phone, email} = e.detail.value

        // 检测用户是否填写完全信息
        if(!phone || !email)
        {
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
        

        var app=getApp();
        const userUrl = `${app.globalData.backEndUrl}/auth/user`
        console.log('fillUserInfo中formSubmit函数，cookie为：',app.globalData.cookies)
        // 向后端发送填写信息请求
        wx.request({
            url: userUrl,
            method: 'post',// 请求方式
            data: { // 想接口提交的数据
                'name': that.data.name,
                'id': that.data.id,
                'department': that.data.department,
                'email': email,
                'phone': phone
            },
            header: {
                'content-type': 'application/json',// 提交的数据类型
                'cookie':app.globalData.cookies //读取cookie
            },
            success(res) {  // 成功回调
                console.log('填写用户信息向后端发送请求成功', res.data);
                if(res.statusCode != 200)
                {
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
                    return
                }
                wx.switchTab({"url":"/pages/home/home"})
            },
            fail() { // 失败回调
                console.log('填写用户信息向后端发送数据失败！');
            }
            })
    }
})