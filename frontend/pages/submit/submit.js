Page({

    /**
     * 页面的初始数据
     */
    data: {
        "projectID":0,
        "form" : [
            {
                "text":"姓名",
                "type":"text"
            },{
                "text":"献血量",
                "type":"options",
                "options":[
                    "200","300","400"
                ]
            }
        ]
    },
  
    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
  
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
            /*
        wx.showToast({
            title: '报名成功',
            icon: 'success',
            duration: 3000
        });
        // post: ok
        // this.setData({"can_signin":false,"already_signin":true})
        */
    
})