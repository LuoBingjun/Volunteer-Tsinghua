Page({
    /**
     * 页面的初始数据
     */
    data: {
        "projectID": 0,
        "cover":"",
        "title":"",
        "description":"",
        "requirement":"",
        "job_set": [
            {
                "id": 1,
                "job_name": "job1",
                "job_worktime": 2.5,
                "job_content": "job1content1",
                "job_require_num": 250,
                "project": 1
            },
            {
                "id": 2,
                "job_name": "job2",
                "job_worktime": 250.0,
                "job_content": "job2content2",
                "job_require_num": 25,
                "project": 1
            }
        ]
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
                    that.setData({
                        'projectID':res.data.id,
                        'cover':res.data.cover,
                        'title':res.data.title,
                        'description':res.data.content,
                        'requirement':res.data.requirements,
                        'introduction':res.data.introduction,
                        "job_set":res.data.job_set,
                        "deadline": res.data.deadline,
                        "finished": res.data.finished,

                        "begin_datetime": res.data.begin_datetime,
                        "end_datetime": res.data.end_datetime
                    });
                    let now = new Date()
                    let deadline = new Date(that.data.deadline)
                    that.setData({"beforedeadline": now.getTime() < deadline.getTime()})
                    console.log("now:",now, "deadline:",deadline,"beforedeadline:",that.data.beforedeadline)
                }
                else if(res.statusCode==403)
                {
                    wx.reLaunch({
                        url: `/pages/login/login?page=project&projectID=`+that.data.projectID,
                    })
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
    onShareAppMessage: function (res) {
        var that = this;
        return {
            title: '志愿清华: '+that.data.title
        }
  
    },

    signin:function(e){
        let dataset = e.currentTarget.dataset
        wx.navigateTo({"url":"submit/submit?"+"projectID="+this.data.projectID+"&jobID="+dataset.jobindex});
    },
    gotoCurrentProject:function(e){
        wx.navigateTo({ "url": "/pages/currentproject/currentproject?projectID=" + this.data.projectID })
    },
    // sign:function(){
    //     wx.navigateTo({"url":"sign/sign?projectID="+this.data.projectID});
    // }
    cancelApply:function(e){
        let dataset = e.currentTarget.dataset

        var that = this
        var app = getApp()
        wx.showModal({
            title: '危险操作！',
            content: '您确定要取消申请吗？',
            confirmText: "我再想想",
            cancelText: "取消申请",
            success: function (res) {
                console.log(res);
                if (res.confirm) {
                    console.log('用户点击我再想想')
                }else{
                    console.log('用户点击退出项目')


                    wx.request({
                    url: `${app.globalData.backEndUrl}/apply/cancelapply`,
                    method: 'post',
                    header: {
                        'content-type': 'application/json', // 提交的数据类型
                        'cookie': app.globalData.cookies //读取cookie
                    },
                    data: {
                        "project_id":that.data.projectID,
                        "job_id":dataset.jobindex
                    },
                    success(res) {  // 成功回调
                        console.log("得到的数据为", res);
                        if (res.statusCode == 200) {
                        wx.showToast({
                            title: "已取消申请",
                            icon: "success",
                            duration: 2000
                        });
                        setTimeout(function () {
                            console.log("返回主界面");
                            wx.navigateBack();
                        }, 2000);
                        }
                        else {
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
                }
            }
        });
    }
})