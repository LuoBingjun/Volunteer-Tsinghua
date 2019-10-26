Page({

    /**
     * 页面的初始数据
     */
    data: {
        "projectID": 123,
        "imageUrl":"/pages/current_project/img1.jpg",
        "title":"项目1",
        "description":"这里有很多很多很多很多很多很多很多很多很多很多很多很多很多很多很多很多很多很多很多很多很多很多很多很多很多很多很多很多总之非常多的描述",
        "requirement":["需求1","需求2","需求3"],
        "other_info":"假装没有其他需求",
        "can_signin":true,
        "already_signin":false,
        "already_passed":false,
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

    signin:function(){
        wx.navigateTo({"url":"/pages/submit/submit?projectID="+this.data.projectID});
    }
})