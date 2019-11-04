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
                "type":"text"
            },{
                "text":"献血量",
                "type":"radioBox",
                "options":[
                        {name: '100', value: '0'},
                        {name: '200', value: '1', checked: true}
                ]
            },{
                "text":"献血量",
                "type":"checkBox",
                "options":[
                        {name: '100', value: '0'},
                        {name: '200', value: '1', checked: true}
                ]
            },{
                "text":"献血量",
                "type":"radioBox",
                "options":[
                        {name: '100', value: '0'},
                        {name: '200', value: '1', checked: true}
                ]
            }
        ],
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
    radioChange: function (e) {
        if(this.data.status=='joined')return;
        console.log('radio',e.currentTarget.id,'发生change事件，携带value值为：', e.detail.value);
        var new_form=this.data.form;
        var radioItems = new_form[e.currentTarget.id].options;
        for (var i = 0, len = radioItems.length; i < len; ++i) {
            radioItems[i].checked = radioItems[i].value == e.detail.value;
        }

        this.setData({
            form: new_form
        });
    },

    checkboxChange: function (e) {
        if(this.data.status=='joined')return;
        console.log('checkbox发生change事件，携带value值为：', e.detail.value);
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

        this.setData({
            form: new_form
        });
    },

    on_submit:function(e){
        wx.showToast({
            title: '报名成功',
            icon: 'success',
            duration: 2000
        });
        this.setData({"status":"joined"});
        setTimeout(function(){
            console.log("返回主界面");
            wx.navigateBack();
        },2000);
    }
})