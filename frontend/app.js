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
        console.log("得到URL：",loginUrl)

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
        backEndUrl: "http://www.lbjthu.tech:8080"
    }
});