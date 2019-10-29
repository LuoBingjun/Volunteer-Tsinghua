Page({

    /**
     * 页面的初始数据
     */
    data: {
        "type":"0",
        "projects":[
            {
                "projectID":"0",
                "title":"我是标题",
                "workTime":"-"
            },{
                "projectID":"1",
                "title":"我也是标题",
                "workTime":"10"
            }
        ]
    },
  
    /*
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        var that = this;
        console.log("WELL ",options)
        this.setData(options)
        /*
        wx.request({
            url: 'http://localhost:8000/image',// 我自己测试时用的接口地址
            method: 'post',// 请求方式
            data: { // 想接口提交的数据
                page: 1,
                pageSize: 2
            },
            header: {
                'content-type': 'application/json'// 提交的数据类型
            },
            success(res) {  // 成功回调
                console.log(res.data.result);
                that.setData({
                arrays: res.data.result,
                })
            },
            fail() { // 失败回调
                console.log('error');
            }

        })
        */
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