(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-66024f2e"],{2017:function(e,t,r){"use strict";var n=r("b12d"),s=r.n(n);s.a},"2d6f":function(e,t,r){},"9ed6":function(e,t,r){"use strict";r.r(t);var n=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{staticClass:"login-container"},[r("el-form",{ref:"loginForm",staticClass:"login-form",attrs:{model:e.loginForm,"auto-complete":"on","label-position":"left"}},[r("div",{staticClass:"title-container"},[r("h3",{staticClass:"title"},[e._v("Login Form")])]),e._v(" "),r("el-form-item",{attrs:{prop:"username"}},[r("span",{staticClass:"svg-container"},[r("svg-icon",{attrs:{"icon-class":"user"}})],1),e._v(" "),r("el-input",{ref:"username",attrs:{placeholder:"Username",name:"username",type:"text",tabindex:"1","auto-complete":"on"},model:{value:e.loginForm.username,callback:function(t){e.$set(e.loginForm,"username",t)},expression:"loginForm.username"}})],1),e._v(" "),r("el-form-item",{attrs:{prop:"password"}},[r("span",{staticClass:"svg-container"},[r("svg-icon",{attrs:{"icon-class":"password"}})],1),e._v(" "),r("el-input",{key:e.passwordType,ref:"password",attrs:{type:e.passwordType,placeholder:"Password",name:"password",tabindex:"2","auto-complete":"on"},nativeOn:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.handleLogin(t)}},model:{value:e.loginForm.password,callback:function(t){e.$set(e.loginForm,"password",t)},expression:"loginForm.password"}}),e._v(" "),r("span",{staticClass:"show-pwd",on:{click:e.showPwd}},[r("svg-icon",{attrs:{"icon-class":"password"===e.passwordType?"eye":"eye-open"}})],1)],1),e._v(" "),r("el-button",{staticStyle:{width:"100%","margin-bottom":"30px"},attrs:{loading:e.loading,type:"primary"},nativeOn:{click:function(t){return t.preventDefault(),e.handleLogin(t)}}},[e._v("Login")]),e._v(" "),r("div",{staticClass:"tips"},[r("span",{staticStyle:{"margin-right":"20px"}},[e._v("username: admin")]),e._v(" "),r("span",[e._v(" password: admin")])])],1)],1)},s=[],o=r("c24f"),a=r("5c96"),i={name:"Login",data:function(){return{loginForm:{username:"admin",password:"admin"},loginRules:{username:[{required:!0,trigger:"blur"}],password:[{required:!0,trigger:"blur"}]},loading:!1,passwordType:"password",redirect:void 0}},watch:{$route:{handler:function(e){console.log("redirect是",this.redirect,e.query,e.query.redirect),this.redirect=e.query&&e.query.redirect,console.log("新的redirect是",this.redirect)},immediate:!0}},methods:{showPwd:function(){var e=this;"password"===this.passwordType?this.passwordType="":this.passwordType="password",this.$nextTick((function(){e.$refs.password.focus()}))},handleLogin:function(){var e=this;this.loading=!0,Object(o["e"])(this.loginForm).then((function(t){console.log("出现了",void 0!==t.data.is_superuser&&t.data.is_superuser),Object(o["g"])(t.data.is_superuser),e.$router.push({path:"/dashboard"}),e.loading=!1})).catch((function(t){Object(a["Message"])({message:"用户名或密码错误",type:"error",duration:5e3}),e.loading=!1}))}}},u=i,c=(r("2017"),r("e4b9"),r("2877")),d=Object(c["a"])(u,n,s,!1,null,"76e54fec",null);t["default"]=d.exports},b12d:function(e,t,r){},b775:function(e,t,r){"use strict";var n=r("bc3a"),s=r.n(n),o=(r("5c96"),s.a.create({baseURL:"/api",timeout:5e3}));o.interceptors.request.use((function(e){return e}),(function(e){return Promise.reject(e)})),o.interceptors.response.use((function(e){return 200!==e.status?Promise.reject(new Error(e.data||"Error")):e}),(function(e){return Promise.reject(e)})),t["a"]=o},c24f:function(e,t,r){"use strict";r.d(t,"e",(function(){return i})),r.d(t,"b",(function(){return u})),r.d(t,"f",(function(){return c})),r.d(t,"c",(function(){return d})),r.d(t,"a",(function(){return l})),r.d(t,"g",(function(){return p})),r.d(t,"d",(function(){return m}));var n=r("b775"),s=r("a78e"),o=r.n(s),a="isSuperUser";function i(e){return console.log(e),Object(n["a"])({url:"/auth/weblogin",method:"post",data:e})}function u(e){return void 0!==e?Object(n["a"])({url:"/auth/webuser?id=".concat(e),method:"get"}):Object(n["a"])({url:"/auth/webuser",method:"get"})}function c(e,t){return void 0!==t?Object(n["a"])({url:"/auth/webuser?id=".concat(t),method:"put",data:e}):(console.log(e),Object(n["a"])({url:"/auth/webuser",method:"put",data:e}))}function d(){return Object(n["a"])({url:"/auth/listwebuser",method:"get"})}function l(e){return Object(n["a"])({url:"/auth/webuser?id=".concat(e),method:"delete"})}function p(e){o.a.set(a,e)}function m(){return o.a.get(a)}},e4b9:function(e,t,r){"use strict";var n=r("2d6f"),s=r.n(n);s.a}}]);