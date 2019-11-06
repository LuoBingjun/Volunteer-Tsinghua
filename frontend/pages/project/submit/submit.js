Page({
    /**
     * 页面的初始数据
     */
    data: {
        "projectID":0,
        "title":"我是一个莫得感情的项目",
        "status":"not_joined",
        "form" : [
            {
                "text":"姓名",
                "required":"true",
                "type":"text",
                "value":""
            },{
                "text":"献血量",
                "required":"true",
                "type":"radioBox",
                "options":[
                        {"name": "100", "value": "1"},
                        {"name": "200", "value": "2"}
                ],
                "value":""
            },{
                "text":"献血量",
                "required":"true",
                "type":"checkBox",
                "options":[
                        {"name": "100", "value": "1"},
                        {"name": "200", "value": "2"}
                ],
                "value":""
            },{
                "text":"献血量",
                "type":"radioBox",
                "options":[
                        {"name": "100", "value": "1"},
                        {"name": "200", "value": "2"}
                ],
                "value":""
            }
        ],
    },
  
    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        console.log("submit.js onLoad函数开始,options:",options)
        var app=getApp();
        const getUrl = `${app.globalData.backEndUrl}/project/detail?id=${options.projectID}`
        console.log("从project跳转到URL：",getUrl)
        var that=this;
        wx.request({
            url: getUrl,
            method: "get",
            header: {
                "content-type": "application/json", // 提交的数据类型
                "cookie":app.globalData.cookies //读取cookie
            },
            success(res) {  // 成功回调
                console.log("得到的数据为",res);
                if(res.statusCode==200)
                {
                    that.setData({
                        "projectID":options.projectID,
                        "status":"not_joined",
                        "title":res.data.title,
                        "form":JSON.parse(res.data.form),
                    });
                }
                else 
                {
                    wx.showModal({
                        title: "错误",
                        content: JSON.stringify(res.data),
                        });
                }
            },
            fail() { // 失败回调
                wx.showModal({
                    title: "错误",
                    content: "无法发送数据，请检查网络状态（也有可能是我们服务器挂了）"
                    });
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
    onShow: function (options) {
        
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
    radioChange: function (e) {
        if(this.data.status=="joined")return;
        console.log("radio",e.currentTarget.id,"发生change事件，携带value值为：", e.detail.value);
        var new_form=this.data.form;
        var radioItems = new_form[e.currentTarget.id].options;
        for (var i = 0, len = radioItems.length; i < len; ++i) {
            radioItems[i].checked = radioItems[i].value == e.detail.value;
        }
        new_form[e.currentTarget.id].value=e.detail.value;
        this.setData({
            form: new_form
        });
    },

    checkboxChange: function (e) {
        if(this.data.status=="joined")return;
        console.log("checkbox发生change事件，携带value值为：", e.detail.value);
        var new_form=this.data.form;
        var values = e.detail.value
        var checkboxItems = new_form[e.currentTarget.id].options;
        for (var i = 0, lenI = checkboxItems.length; i < lenI; ++i) {
            checkboxItems[i].checked = false;
            for (var j = 0, lenJ = values.length; j < lenJ; ++j) {
                if(checkboxItems[i].value == values[j]){
                    checkboxItems[i].checked = true;
                    break;
                }
            }
        }
        new_form[e.currentTarget.id].value=e.detail.value;
        this.setData({
            form: new_form
        });
    },
    on_text_changed: function(e){
        var t=e.currentTarget.id;
        var new_form=this.data.form;
        new_form[t].value=e.detail.value;
        this.setData({"form":new_form})
    },
    on_submit:function(e){
        var index=0;
        const form=this.data.form;
        for(var idx in this.data.form)
        {
            console.log(idx,form[idx]);
            if(form[idx].required&&!form[idx].value)
            {
                this.setData({"error_prompt":`第${parseInt(idx)+1}项为必填项`})
                return;            
            }
        }
        var values=[];
        for(var idx in this.data.form)
        {
            values[idx]=this.data.form[idx].value
        }
        console.log("表单页汇总：",values);

        var app=getApp();
        const postUrl = `${app.globalData.backEndUrl}/apply/fillform`
        var that=this;
        console.log("index是",this.data.projectID)
        wx.request({
            url: postUrl,
            method: 'post',
            header: {
                'content-type': 'application/json', // 提交的数据类型
                'cookie':app.globalData.cookies, //读取cookie
            },
            data:{
                'project_id':this.data.projectID,
                'form':JSON.stringify(values)
            },
            success(res) {  // 成功回调
                console.log("得到的数据为",res);
                if(res.statusCode==200)
                {
                    wx.showToast({
                        title: "报名成功",
                        icon: "success",
                        duration: 2000
                    });
                    that.setData({"status":"joined"});
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