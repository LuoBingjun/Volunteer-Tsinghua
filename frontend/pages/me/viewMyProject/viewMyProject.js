Page({

    /**
     * 页面的初始数据
     */
    data: {
        "type":"ALL",
        "projects":[
            {
                "id": 1,
                "cover": "封面图片url",
                "title": "标题",
                "content": "内容",
                "require_num": 5, // "需求人数"
                "requirements": "需求" ,
                "form": "表单",
                "time": "发起时间",
                "deadline": "截止时间"
            },
            {
                "id": 1,
                "cover": "封面图片url",
                "title": "标题",
                "content": "内容",
                "require_num": 5, // "需求人数"
                "requirements": "需求" ,
                "form": "表单",
                "time": "发起时间",
                "deadline": "截止时间"
            },
        ]
    },
  
    /*
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        var that = this;
        console.log("viewMyProject页面加载： ",options)
        this.setData(options)

        var app=getApp()
        let urlWhole = "null"
        if(that.data.type == "ALL")
        {
            urlWhole = `${app.globalData.backEndUrl}/project/list`
        }
        else if(that.data.type == "CHECKING")
        {
            urlWhole = `${app.globalData.backEndUrl}/project/list`
        }
        else if(that.data.type == "CURRENT")
        {
            urlWhole = `${app.globalData.backEndUrl}/project/list`
        }        
        else if(that.data.type == "HISTORY")
        {
            urlWhole = `${app.globalData.backEndUrl}/project/list`
        }
        else
        {
            urlWhole = `${app.globalData.backEndUrl}/project/list`
        }



        console.log("viewMyProject得到完整URL：",urlWhole)
        wx.request({
            url: urlWhole,
            method: 'get',
            header: {
                'content-type': 'application/json', // 提交的数据类型
                'cookie':app.globalData.cookies //读取cookie
            },
            success(res) {  // 成功回调
                console.log("得到的数据为",res)
                that.setData({
                    "projects": res.data
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

    jumpPage: function(e)
    {
        wx.navigateTo({"url":"/pages/project/project?projectID="+e.currentTarget.id})
    }  
})