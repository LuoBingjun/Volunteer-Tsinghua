Array.prototype.remove = function (b) {
  var a = this.indexOf(b);
  if (a >= 0) {
    this.splice(a, 1);
    return true;
  }
  return false;
};


Date.prototype.Format = function (fmt) {
  var o = {
    "M+": this.getMonth() + 1,
    "d+": this.getDate(),
    "H+": this.getHours(),
    "m+": this.getMinutes(),
    "s+": this.getSeconds(),
    "S+": this.getMilliseconds()
  };

  //因位date.getFullYear()出来的结果是number类型的,所以为了让结果变成字符串型，下面有两种方法：



  if (/(y+)/.test(fmt)) {
    //第一种：利用字符串连接符“+”给date.getFullYear()+""，加一个空字符串便可以将number类型转换成字符串。

    fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
  }
  for (var k in o) {
    if (new RegExp("(" + k + ")").test(fmt)) {

      //第二种：使用String()类型进行强制数据类型转换String(date.getFullYear())，这种更容易理解。

      fmt  =  fmt.replace(RegExp.$1,  (RegExp.$1.length  ==  1)  ?  (o[k])  :  (("00"  +  o[k]).substr(String(o[k]).length)));
    }
  }
  return fmt;
}

App({
  onLaunch: function () {
    console.log('App Launch')

    let that = this;
    wx.getSystemInfo({
      success: res => {
        let modelmes = res.model;
        if (modelmes.search('iPhone X') != -1 || modelmes.search('iPhone 11') != -1 || modelmes.search('unknown') != -1) {
          that.globalData.isIphoneX = true
        }
        wx.setStorageSync('modelmes', modelmes)
      }
    })

  },
  onShow: function (options) {
    if (options.referrerInfo.extraData) {
      let token = options.referrerInfo.extraData.token
      wx.reLaunch({
        url: `/pages/login/login?token=${token}`,
      })
    }
    else {
      console.log('onShow中globaldata:', this.globalData)
    }
  },
  onHide: function () {
    console.log('App Hide')
  },
  globalData: {
    hasLogin: false,
    backEndUrl: "https://2019-a15.iterator-traits.com/api",
    // backEndUrl: "http://2019-a15.iterator-traits.com:3389",
    tmplIds: ['JRmcDj_rRLknyYVevU-iNgosYQ7cm88cs2UTS89B2-o', 
      'z7xt4wI2pFXsbFsI3pdDhzJ5LYcQh9KU5EaiOKg1aRM'],
    userInfo: {
      department: "",
      id: "",
      name: "",
      email: "",
      phone: ""
    },
    cookies: ""
  }



});