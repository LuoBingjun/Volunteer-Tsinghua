Page({

    /**
     * 页面的初始数据
     */
    data: {
        "projects":[
            {"name": "我是一个项目","description":"没有描述","projectID":123, "imageUrl": "img2.jpg"},
            {"name": "我也是一个项目","description":"懒得描述","projectID":143, "imageUrl": ""},
            {"name": "我不是一个项目","description":"上面那句话是假话","projectID":179, "imageUrl": ""}
        ]
    },
  
    /*
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        var that = this;
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
    onClickOneProject: function(){
        console.log("current_projects onClickOneProject!")
        wx.navigateTo({"url":"current_one_project/current_one_project"})
    }
    
})