Page({

    /**
     * 页面的初始数据
     */
    data: {
        "projects":[
            {"name": "我是一个项目","description":"没有描述","projectID":123, "imageUrl": "img2.jpg"},
            {"name": "我也是一个项目","description":"懒得描述","projectID":143, "imageUrl": ""},
            {"name": "我不是一个项目","description":"上面那句话是假话","projectID":179, "imageUrl": ""}
        ],
        "searchbar":false
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
    enterProject:function(e){
        console.log(e.currentTarget.id)
        wx.navigateTo({"url":"/pages/project/project?projectID="+e.currentTarget.id})
        
    }
})