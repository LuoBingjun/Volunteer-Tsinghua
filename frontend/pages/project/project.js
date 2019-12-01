Page({
    /**
     * 页面的初始数据
     */
    data: {
        "projectID": 0,
        "cover":"",
        "title":"",
        "description":"",
        "requirement":[],
        "status":"A"
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {        
        this.setData({'projectID':options.projectID})
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
        // console.log("烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫")
        var app=getApp();
        const getUrl = `${app.globalData.backEndUrl}/project/detail?id=${this.data.projectID}`
        console.log("从project跳转到URL：",getUrl)
        var that=this;
        wx.request({
            url: getUrl,
            method: 'get',
            header: {
                'content-type': 'application/json', // 提交的数据类型
                'cookie':app.globalData.cookies //读取cookie
            },
            success(res) {  // 成功回调
                console.log("得到的数据为",res);
                if(res.statusCode==200)
                {
                    var reqs=JSON.parse(res.data.requirements)
                    reqs.push(`最大报名人数为${res.data.require_num}人，报完即止。`);
                    that.setData({
                        'projectID':res.data.id,
                        'cover':res.data.cover,
                        'title':res.data.title,
                        'description':res.data.content,
                        'requirement':reqs,
                        'status':res.data.status
                    });
                    console.log("Status为：",that.data.status)
                }
                else 
                {
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
        wx.navigateTo({"url":"submit/submit?projectID="+this.data.projectID});
    },
    gotoCurrentProject:function(){
        wx.navigateTo({ "url": "/pages/currentproject/currentproject?projectID=" + this.data.projectID })
    },
    sign:function(){
        wx.navigateTo({"url":"sign/sign?projectID="+this.data.projectID});
    }
})