App({
    onLaunch: function () {
        console.log('App Launch')
    },
    onShow: function (options) {
        var that = this
        console.log('App Show')
        console.log("App得到THU校友总会助手小程序发回的extraData",options.referrerInfo.extraData)       
        var token = options.referrerInfo.extraData.token
        console.log("App得到THU校友总会助手小程序发回的token:",token)



        var app=getApp();
        const loginUrl = `${app.globalData.backEndUrl}/auth/login`

        wx.request({
        url: loginUrl,
        method: 'post',// 请求方式
        data: { // 想接口提交的数据
            'token':token
        },
        header: {
            'content-type': 'application/json'// 提交的数据类型
        },
        success(res) {  // 成功回调
            console.log('向后端发送数据成功！', res.data);
            // res.data 包含了后端传回的学号等信息。
            //app.globalData.userInfo = JSON.parse(JSON.stringify(res.data))
            // console.log('拷贝globalData.userInfo:', app.globalData.userInfo)
            if (res.data.first_login){
                wx.navigateTo({"url":"/pages/fillUserInfo/fillUserInfo?department="
                +res.data.department + "&id="+ res.data.id + "&name="+ res.data.name})
            }
        },
        fail() { // 失败回调
            console.log('向后端发送数据失败！');
        }
        })
    },
    onHide: function () {
        console.log('App Hide')
    },
    globalData: {
        hasLogin: false,
        backEndUrl: "http://62.234.0.237:80/api",
        userInfo:{
            department: "一二三学院",
            id: "12345678",
            name: "哈哈哈",
            email: "lbj17@mails.tsinghua.edu.cm",
            phone: "13888888888"
        }
    }
});