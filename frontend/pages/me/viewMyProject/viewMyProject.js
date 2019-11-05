Page({

    /**
     * 页面的初始数据
     */
    data: {
        "type":"ALL",
        "projects":[
            {
                "id": 1,
                "form": "{}",
                "submit_time": "2019-11-05T17:32:36.000059+08:00",
                "status": "B",
                "project":{
                    "id": 1,
                    "title": "3123123",
                    "content": "31232131",
                    "cover": "",
                    "require_num": 5,
                    "requirements": "123456",
                    "form": "adasdadadadadad",
                    "time": "2019-10-26T19:52:57+08:00",
                    "deadline": "2019-11-06T06:00:00+08:00",
                    "finished": false
                }
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
            urlWhole = `${app.globalData.backEndUrl}/my/applyrecord`
        }
        else if(that.data.type == "CURRENT")
        {
            urlWhole = `${app.globalData.backEndUrl}/my/processrecord`
        }        
        else if(that.data.type == "HISTORY")
        {
            urlWhole = `${app.globalData.backEndUrl}/my/historyrecord`
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