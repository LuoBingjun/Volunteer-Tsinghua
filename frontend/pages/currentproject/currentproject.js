Page({
  /**
   * 页面的初始数据
   */
  data: {
    "projectID": 0,
    signList: {},
    activeNames: []
  },
  onChange(event) {
    this.setData({
      activeNames: event.detail
    });
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    console.log(options)
    this.setData({ 'projectID': options.projectID })
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
    var app = getApp();
    const getUrl = `${app.globalData.backEndUrl}/my/processrecorddetail?project_id=${this.data.projectID}`
    var that = this;
    wx.request({
      url: getUrl,
      method: 'get',
      header: {
        'content-type': 'application/json', // 提交的数据类型
        'cookie': app.globalData.cookies //读取cookie
      },
      success(res) {  // 成功回调
        console.log("得到的数据为", res);
        if (res.statusCode == 200) {
          that.setData({
            'projectID': res.data.project.id,
            'project': res.data.project,
            'num_sign': res.data.signproject.length
          });
          let signList = {}
          that.reslen = res.data.signproject.length
          for (let item of res.data.signproject) {
            signList[item.id] = item

            let now = new Date()
            item.begin_time = new Date(item.begin_time)
            item.end_time = new Date(item.end_time)
            if (now.getTime() < item.begin_time.getTime()) {
              item.status = 3
            }
            else if (now.getTime() > item.end_time.getTime()) {
              item.status = 0
            }
            else {
              that.data.activeNames.push(item.id)
              that.setData({
                activeNames: that.data.activeNames
              })

              item.status = 1



              // wx.request({
              //     url: `${app.globalData.backEndUrl}/my/signrecord?signproject=${item.id}`,
              //     method: 'get',
              //     header: {
              //     'content-type': 'application/json', // 提交的数据类型
              //     'cookie': app.globalData.cookies //读取cookie
              //     },
              //     success(res2) {
              //     console.log(res2)
              //     if (res2.statusCode == 200) {
              //         signList[res2.data.sign_project].status = 2  
              //         //that.setData({ 'signList': signsList })
              //     }
              //     else if (res2.statusCode != 404) {
              //         wx.showModal({
              //         title: '错误',
              //         content: JSON.stringify(res2.data),
              //         });
              //     }

              //     },
              //     fail() { // 失败回调
              //     wx.showModal({
              //         title: '错误',
              //         content: '无法发送数据，请检查网络状态'
              //     });
              //     that.setData({ 'signList': {} })
              //     }
              // })
            }
            item.begin_time = item.begin_time.Format("yyyy-MM-dd HH:mm:ss")
            item.end_time = item.end_time.Format("yyyy-MM-dd HH:mm:ss")
          }

          for (let item of res.data.signrecord_set) {
            if (item.sign_out_time) {
              //  已签退
              signList[item.sign_project].status = 4
            }
            else {
              //  未签退
              signList[item.sign_project].status = 2
              signList[item.sign_project].signrecordid = item.id
            }
          }


          that.setData({
            'signList': signList
          });
        }
        else if (res.statusCode == 403) {
          wx.reLaunch({
            url: `/pages/login/login?page=currentproject&projectID=` + that.data.projectID,
          })
        }
        else {
          wx.reLaunch({ "url": "/pages/project/project?projectID=" + that.data.projectID })
        }
      },
      fail() { // 失败回调
        wx.showModal({
          title: '错误',
          content: '无法发送数据，请检查网络状态'
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
      title: '志愿清华: ' + that.data.title
    }

  },
  sign: function (e) {
    if (this.data.disabled) return;
    var app = getApp();
    console.log(e.currentTarget)
    var that = this
    wx.getLocation({
      type: 'wgs84',
      isHighAccuracy: true,
      success(res) {
        var latitude = res.latitude
        var longitude = res.longitude
        var accuracy = res.accuracy
        var horizontalAccuracy = res.horizontalAccuracy
        console.log("获得地理位置1：latitude", latitude, "longitude", longitude, "accuracy", accuracy, "horizontalAccuracy", horizontalAccuracy)

        wx.request({
          url: `${app.globalData.backEndUrl}/sign/signin`,
          method: 'post',
          header: {
            'content-type': 'application/json', // 提交的数据类型
            'cookie': app.globalData.cookies //读取cookie
          },
          data: {
            'sign_project_id': e.currentTarget.id,
            "longitude": longitude,
            "latitude": latitude
          },
          success(res) {  // 成功回调
            console.log("得到的数据为", res);
            if (res.statusCode == 200) {
              that.setData({ 'disabled': true })
              wx.showToast({
                title: "签到成功",
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
              content: '无法发送数据，请检查网络状态'
            });
          }
        })
      },
      fail(res) {
        wx.showModal({
          title: '错误',
          content: '无法获得您的地理位置，请打开手机定位'
        });
        return
      }
    })
  },
  previewImg: function (e) {
    console.log(e.currentTarget.dataset.index);
    var index = e.currentTarget.dataset.index;
    let url = this.data.project.qrcode_1
    if (index == 2) {
      url = this.data.project.qrcode_2
    }
    wx.previewImage({
      current: url,     //当前图片地址
      urls: [this.data.project.qrcode_1, this.data.project.qrcode_2],               //所有要预览的图片的地址集合 数组形式
      success: function (res) { },
      fail: function (res) { },
      complete: function (res) { },
    })
  },
  projectcancel() {
    var that = this
    var app = getApp()
    wx.showModal({
      title: '危险操作！',
      content: '退出项目后将无法恢复！',
      confirmText: "我再想想",
      cancelText: "退出项目",
      success: function (res) {
        console.log(res);
        if (res.confirm) {
          console.log('用户点击我再想想')
        } else {
          console.log('用户点击退出项目')
          wx.request({
            url: `${app.globalData.backEndUrl}/project/cancel`,
            method: 'post',
            header: {
              'content-type': 'application/json', // 提交的数据类型
              'cookie': app.globalData.cookies //读取cookie
            },
            data: {
              "project_id": that.data.projectID
            },
            success(res) {  // 成功回调
              console.log("得到的数据为", res);
              if (res.statusCode == 200) {
                wx.showToast({
                  title: "已退出此项目",
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
                content: '无法发送数据，请检查网络状态'
              });
            }
          })
        }
      }
    });
  },
  signout: function (e) {
    let dataset = e.currentTarget.dataset
    console.log("signout函数触发！,signrecordid=", dataset.signrecordid)
    var that = this
    var app = getApp()
    wx.showModal({
      title: '确认签退',
      content: '签退时间将可能作为工时计算的依据，您确定要签退吗？',
      confirmText: "我再想想",
      cancelText: "确认签退",
      success: function (res) {
        console.log(res);
        if (res.confirm) {
          console.log('用户点击我再想想')
        } else {
          console.log('用户点击签退')


          wx.request({
            url: `${app.globalData.backEndUrl}/sign/signout`,
            method: 'post',
            header: {
              'content-type': 'application/json', // 提交的数据类型
              'cookie': app.globalData.cookies //读取cookie
            },
            data: {
              "sign_record_id": dataset.signrecordid
            },
            success(res) {  // 成功回调
              console.log("得到的数据为", res);
              if (res.statusCode == 200) {
                wx.showToast({
                  title: "已成功签退",
                  icon: "success",
                  duration: 2000
                });
                setTimeout(function () {
                  console.log("返回主界面")
                  wx.navigateBack()
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
                content: '无法发送数据，请检查网络状态'
              });
            }
          })
        }
      }
    });
  }
});