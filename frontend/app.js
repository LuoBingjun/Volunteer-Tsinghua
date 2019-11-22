Array.prototype.remove = function (b) {
  var a = this.indexOf(b);
  if (a >= 0) {
    this.splice(a, 1);
    return true;
  }
  return false;
};

App({
  onLaunch: function () {
    console.log('App Launch')
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