Page({
    /**
     * 页面的初始数据
     */
    data: {
        projectID:0,
        list: [
            {
                'signID':'0',
                'name':'第0次签到',
                'status':'0',   //无法签到
                'open':'false'
            },
            {
                'signID':'1',
                'name':'第1次签到',
                'status':'1',     //点击签到
                'open':'true'
            },{
                'signID':'2',
                'name':'第2次签到',
                'status':'2',     //已经签到
                'open':'false'
            },{
                'signID':'2',
                'name':'第2次签到',
                'status':'3',    //签到未开始
                'open':'false'
            }
        ]
    },
  
    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        console.log("选项：",options)
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
    onShow: function (options) {
        var app=getApp();
        const getUrl = `${app.globalData.backEndUrl}/sign/list?project=${this.data.projectID}`
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
                    var list=[]
                    that.reslen=res.data.length
                    for(var i in res.data)
                    {
                        var item={}
                        item.signID=res.data[i].id
                        item.name=res.data[i].title
                        item.content=res.data[i].content
                        item.has_sign_in=false
                        list.push(item)

                        var now=new Date().getTime()
                        var begin=new Date(res.data[i].begin_time).getTime()
                        var end=new Date(res.data[i].end_time).getTime()
                        that.setData({'list':[]})
                        if(now<begin)
                        {
                            item.status=3
                        }
                        else if(now>end)
                        {
                            item.status=0
                        }                            
                        else
                        {
                            item.status=1
                            wx.request({
                                url:`${app.globalData.backEndUrl}/my/signrecord?signproject=${item.signID}`,
                                method:'get',
                                header:{
                                    'content-type': 'application/json', // 提交的数据类型
                                    'cookie':app.globalData.cookies //读取cookie
                                },
                                success(res2){
                                    console.log(res2)
                                    if(res2.statusCode==200)
                                    {
                                        for (var j in list)
                                        {
                                            console.log(list[j].signID,res2.data.sign_project)
                                            if(list[j].signID==res2.data.sign_project)
                                            {
                                                list[j].status=2;
                                                that.setData({'list':list});
                                                break;
                                            }
                                        }
                                    }
                                    else if(res2.statusCode!=404){
                                        wx.showModal({
                                            title: '错误',
                                            content: JSON.stringify(res2.data),
                                            });
                                    }
                                }, 
                                fail() { // 失败回调
                                    wx.showModal({
                                        title: '错误',
                                        content: '无法发送数据，请检查网络状态（也有可能是我们服务器挂了）'
                                        });
                                    that.setData({'list':[]})
                                }
                            })
                        }
                        that.setData({'list':list});
                    }
                    console.log(list)
                    setTimeout(function(){console.log(that.data.list)},1000)
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

    switchOpen :function(e){
        var id=e.currentTarget.id
        var list=this.data.list
        console.log("拿到的id",id)
        list[id].open=list[id].open=='true'?'false':'true'
        console.log("修改后：",list)
        this.setData({'list':list})
    },

    sign:function(e)
    {
        if(this.data.disabled)return;
        var app=getApp();
        const postUrl = `${app.globalData.backEndUrl}/sign/signin`
        console.log(e.currentTarget)
        var that=this
        wx.request({
            url: postUrl,
            method: 'post',
            header: {
                'content-type': 'application/json', // 提交的数据类型
                'cookie':app.globalData.cookies //读取cookie
            },
            data:{
                'sign_project':e.currentTarget.id
            },
            success(res) {  // 成功回调
                console.log("得到的数据为",res);
                if(res.statusCode==200)
                {
                    that.setData({'disabled':true})
                    wx.showToast({
                        title: "签到成功",
                        icon: "success",
                        duration: 2000
                    });
                    setTimeout(function(){
                        console.log("返回主界面");
                        wx.navigateBack();
                    },2000);
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
    }
})
