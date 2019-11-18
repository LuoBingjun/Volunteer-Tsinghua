App({
    onLaunch: function () {
        console.log('App Launch')
    },
    onShow: function (options) {
        var that = this
        console.log('App Show')
        console.log('onShow中globaldata:',that.globalData)
        if(!options.referrerInfo.extraData)
        {
            console.log('app.onshow登录模块开始！')
            // 检查用户是否登录
            wx.login({
                timeout: 1000, 
                success (res) {
                    console.log('wx.login success成功!, res.code:',res.code)
                    if (res.code) {
                        //发起网络请求
                        const preloginUrl = `${that.globalData.backEndUrl}/auth/prelogin`
                        wx.request({
                            url: preloginUrl,
                            method: 'post',
                            data: {
                                code: res.code
                            },
                            header: {
                                'content-type': 'application/json'// 提交的数据类型
                            },
                            success(res){
                                console.log('wx.login success里面的prelogin请求成功了！res.statusCode为：',res.statusCode)
                                if(res.statusCode == 200)
                                {
                                    console.log('wx.login success里面的prelogin请求成功了！并且状态码为200，得到的cookies为：',res.header['Set-Cookie'])
                                    that.globalData.cookies=res.header['Set-Cookie']
                                    if(res.data.login_status)
                                    {
                                        console.log('res.data.login_status为true')
                                        wx.reLaunch({'url':"/pages/home/home"})
                                    }
                                    else
                                    {
                                        console.log('res.data.login_status为false还未登录')
                                        wx.reLaunch({"url":"/pages/login/login"})
                                    }
                                }
                            }

                        })
                    } 
                    else {
                        console.log('wx.login success res.code == false: res.errMsg为' + res.errMsg)
                        wx.reLaunch({"url":"/pages/login/login"})
                    }
                },
                fail() {
                    console.log('wx.login中fail函数被调用。')
                    wx.reLaunch({"url":"/pages/login/login"})
                }
            })



        }
        else
        {
            console.log('app.onshow校友总会助手小程序跳转回模块开始！')
            console.log("App得到THU校友总会助手小程序发回的extraData",options.referrerInfo.extraData)       
            var token = options.referrerInfo.extraData.token
            console.log("App得到THU校友总会助手小程序发回的token:",token)
            
            const loginUrl = `${that.globalData.backEndUrl}/auth/login`
            wx.request({
            url: loginUrl,
            method: 'post',// 请求方式
            data: { // 想接口提交的数据
                'token':token
            },
            header: {
                'content-type': 'application/json',// 提交的数据类型
                'cookie':that.globalData.cookies //读取cookie
            },
            success(res) {  // 成功回调
                console.log('向后端发送数据成功！', res.data);
                // app.globalData.cookies=res.header['Set-Cookie'];
                // res.data 包含了后端传回的学号等信息。
                //app.globalData.userInfo = JSON.parse(JSON.stringify(res.data))
                // console.log('拷贝globalData.userInfo:', app.globalData.userInfo)
                if (res.data.first_login){
                    wx.navigateTo({"url":"/pages/fillUserInfo/fillUserInfo?department="
                    +res.data.department + "&id="+ res.data.id + "&name="+ res.data.name})
                }
                else
                {
                    wx.switchTab({"url":"/pages/home/home"})
                }
            },
            fail() { // 失败回调
                console.log('向后端发送数据失败！');
            }
            })
        }
    },
    onHide: function () {
        console.log('App Hide')
    },
    globalData: {
        hasLogin: false,
        backEndUrl: "https://2019-a15.iterator-traits.com/api",
        userInfo:{
            department: "一二三学院",
            id: "12345678",
            name: "哈哈哈",
            email: "lbj17@mails.tsinghua.edu.cm",
            phone: "13888888888"
        },
        cookies: "?"
    }


    
});