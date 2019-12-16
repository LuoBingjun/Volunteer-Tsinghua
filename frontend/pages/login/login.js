// pages/login.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    loginStatus: true
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    let that = this;
    let app = getApp()
    console.log("login界面onShow开始")
    if (!options.token) {
      // 检查用户是否登录
      wx.login({
        timeout: 1000,
        success(res) {
          console.log('wx.login success成功!, res.code:', res.code)
          if (res.code) {
            wx.request({
              url: `${app.globalData.backEndUrl}/auth/prelogin`,
              method: 'post',
              data: {
                code: res.code
              },
              header: {
                'content-type': 'application/json'// 提交的数据类型
              },
              success(res) {
                console.log('wx.login success里面的prelogin请求成功了！res.statusCode为：', res.statusCode)
                if (res.statusCode == 200) {
                  console.log('wx.login success里面的prelogin请求成功了！并且状态码为200，得到的cookies为：', res.header['Set-Cookie'])
                  app.globalData.cookies = res.header['Set-Cookie']
                  if (res.data.login_status) {
                    console.log('res.data.login_status为true')
                    if(!options.page)
                    {
                      wx.reLaunch({ 'url': "/pages/home/home" })
                    }
                    else
                    {
                      wx.request({
                        url: `${app.globalData.backEndUrl}/auth/user`,
                        method: 'get',
                        header: {
                          'content-type': 'application/json', // 提交的数据类型
                          'cookie': app.globalData.cookies //读取cookie
                        },
                        success(res) {  // 成功回调
                          console.log("home.js 获取用户信息：", res.data)
                          app.globalData.userInfo = JSON.parse(JSON.stringify(res.data))
                          that.setData({
                            "username": app.globalData.userInfo.name,
                          })
                          wx.reLaunch({ "url": `/pages/${options.page}/${options.page}?projectID=${options.projectID}`})
                        },
                        fail() { // 失败回调
                          console.log('向后端发送数据失败！');
                        }
                      })
                    }

                  }
                  else {
                    console.log('res.data.login_status为false还未登录')
                    that.setData({
                      loginStatus: false
                    })
                  }
                }
              }
            })
          }
          else {
            console.log('wx.login success res.code == false: res.errMsg为' + res.errMsg)
          }
        },
        fail() {
          console.log('wx.login中fail函数被调用。')
          // wx.reLaunch({ "url": "/pages/login/login" })
        }
      })
    }
    else {
      // 跳转回来带token参数
      console.log('app.onshow校友总会助手小程序跳转回模块开始！')
      console.log("App得到THU校友总会助手小程序发回的extraData", options.token)
      let token = options.token
      console.log("App得到THU校友总会助手小程序发回的token:", token)

      wx.request({
        url: `${app.globalData.backEndUrl}/auth/login`,
        method: 'post',// 请求方式
        data: { // 想接口提交的数据
          'token': token
        },
        header: {
          'content-type': 'application/json',// 提交的数据类型
          'cookie': app.globalData.cookies //读取cookie
        },
        success(res) {  // 成功回调
          console.log('向后端发送数据成功！', res.data);
          // app.globalData.cookies=res.header['Set-Cookie'];
          // res.data 包含了后端传回的学号等信息。
          //app.globalData.userInfo = JSON.parse(JSON.stringify(res.data))
          // console.log('拷贝globalData.userInfo:', app.globalData.userInfo)
          if (res.data.first_login) {
            wx.reLaunch({
              "url": "/pages/fillUserInfo/fillUserInfo?department="
                + res.data.department + "&id=" + res.data.id + "&name=" + res.data.name
            })
          }
          else {
            wx.reLaunch({ "url": "/pages/home/home" })
          }
        },
        fail() { // 失败回调
          console.log('向后端发送数据失败！');
        }
      })
    }
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
  // // 这个函数只是注释，将来删掉！！！
  // kindToggle: function (e) {
  //   var app=getApp();
  //       const myUrl = `${app.globalData.backEndUrl}/auth/login`

  //       wx.request({
  //           url: myUrl,
  //           method: 'post',
  //           data:{
  //             'token':'null'
  //           },
  //           success(res) {  // 成功回调
  //             if(res.statusCode==200)
  //             {
  //               console.log("得到的cookies为",res.header['Set-Cookie']);
  //               //console.log(res);
  //               if('data' in res)
  //               {
  //                 app.globalData.name=res.data.name;
  //                 app.globalData.id=res.data.id;
  //                 app.globalData.department=res.data.department;
  //                 wx.switchTab({'url':"/pages/home/home"});
  //                 app.globalData.cookies=res.header['Set-Cookie'];
  //               }
  //               return;
  //             }
  //             else {
  //               wx.showModal({
  //                 title: '错误',
  //                 content: JSON.stringify(res.data)
  //                 });
  //             }
  //           },
  //           fail() { // 失败回调
  //             wx.showModal({
  //               title: '错误',
  //               content: '无法发送数据，请检查网络状态（也有可能是我们服务器挂了）'
  //               });
  //           }
  //           })

  // },







  onLoginPushed: function (e) {
    //     // TODO: 下面几行是测试使用，跳过了登录，将来用下面登录的。
    //     wx.navigateTo({"url":"/pages/fillUserInfo/fillUserInfo?department="
    //                 +"软件学院" + "&id="+ "2017126112" + "&name="+ "清华小"})


    //  跳转到助教“清华人”小程序
    wx.navigateToMiniProgram(
      {
        "appId": "wx1ebe3b2266f4afe0",
        "path": "pages/index/index",
        "envVersion": "trial",
        "extraData":
        {
          "origin": "miniapp",
          "type": "id.tsinghua"
        },
        success(res) {
          console.log("跳转到助教小程序成功！", res)
        },
        fail(res) {
          console.log("跳转到助教小程序失败！", res)
          wx.showModal({
            title: '网络异常',
            content: '网络异常',
            success(res) {
              if (res.confirm) {
                console.log('用户点击确定')
              } else if (res.cancel) {
                console.log('用户点击取消')
              }
            }
          })
        }
      }
    )

  }
})