(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-5e352c39"],{"03f4":function(e,t,o){"use strict";o.r(t);var r=function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",{staticStyle:{margin:"40px"}},[o("launchform")],1)},n=[],i=o("5c96"),l=(o("b775"),o("24d2")),a=function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("el-form",{ref:"mainform",attrs:{model:e.form,rules:e.rules,"label-width":"auto"}},[o("h2",[o("i",{staticClass:"el-icon-news"}),e._v(" 基本信息\n  ")]),e._v(" "),o("el-form-item",{staticClass:"short",attrs:{label:"项目标题",prop:"title"}},[o("el-input",{attrs:{placeholder:"请输入项目标题"},model:{value:e.form.title,callback:function(t){e.$set(e.form,"title",t)},expression:"form.title"}})],1),e._v(" "),o("el-form-item",{attrs:{label:"项目简介",prop:"introduction"}},[o("el-input",{attrs:{placeholder:"请输入项目简介"},model:{value:e.form.introduction,callback:function(t){e.$set(e.form,"introduction",t)},expression:"form.introduction"}})],1),e._v(" "),o("el-form-item",{attrs:{label:"选择标签",prop:"type"}},[o("el-select",{attrs:{placeholder:"请选择项目标签"},on:{input:function(t){return e.clearValidate("type")}},model:{value:e.form.type,callback:function(t){e.$set(e.form,"type",t)},expression:"form.type"}},[o("el-option",{attrs:{label:"文化教育",value:"WH"}}),e._v(" "),o("el-option",{attrs:{label:"赛会服务",value:"SH"}}),e._v(" "),o("el-option",{attrs:{label:"社区服务",value:"SQ"}}),e._v(" "),o("el-option",{attrs:{label:"医疗健康",value:"YL"}}),e._v(" "),o("el-option",{attrs:{label:"健康残障",value:"JK"}}),e._v(" "),o("el-option",{attrs:{label:"校园讲解",value:"XY"}}),e._v(" "),o("el-option",{attrs:{label:"其他项目",value:"QT"}})],1)],1),e._v(" "),o("el-form-item",{attrs:{label:"项目详情",prop:"content"}},[o("el-input",{attrs:{type:"textarea",rows:6},model:{value:e.form.content,callback:function(t){e.$set(e.form,"content",t)},expression:"form.content"}})],1),e._v(" "),o("el-form-item",{attrs:{label:"项目需求",prop:"requirements"}},[o("el-input",{attrs:{type:"textarea",rows:6},model:{value:e.form.requirements,callback:function(t){e.$set(e.form,"requirements",t)},expression:"form.requirements"}})],1),e._v(" "),o("el-form-item",{ref:"upload_item",attrs:{label:"封面图片",prop:"cover"}},[o("el-upload",{ref:"uploader",attrs:{action:"#","list-type":"picture-card","auto-upload":!0,multiple:!1,limit:1,name:"cover","http-request":e.getFile,"on-remove":e.handleCoverRemove,accept:"image/*"}},[o("i",{class:e.form.cover?"el-icon-close":"el-icon-plus",attrs:{slot:"default"},slot:"default"})])],1),e._v(" "),o("el-form-item",{ref:"upload_qrcode1"},[o("div",{attrs:{slot:"label"},slot:"label"},[o("span",[e._v("\n        活动群二维码\n        "),o("el-tooltip",{attrs:{content:"不是必填项，仅报名成功后可见"}},[o("i",{staticClass:"el-icon-question"})])],1)]),e._v(" "),o("el-upload",{ref:"uploader",attrs:{action:"#","list-type":"picture-card","auto-upload":!0,multiple:!1,limit:1,name:"cover","http-request":e.getQrcode1,"on-remove":e.handleQrcode1Remove,accept:"image/*"}},[o("i",{class:e.form.qrcode1?"el-icon-close":"el-icon-plus",attrs:{slot:"default"},slot:"default"})])],1),e._v(" "),o("el-form-item",{ref:"upload_qrcode2"},[o("div",{attrs:{slot:"label"},slot:"label"},[o("span",[e._v("\n        负责人二维码\n        "),o("el-tooltip",{attrs:{content:"不是必填项，仅报名成功后可见"}},[o("i",{staticClass:"el-icon-question"})])],1)]),e._v(" "),o("el-upload",{ref:"uploader",attrs:{action:"#","list-type":"picture-card","auto-upload":!0,multiple:!1,limit:1,name:"cover","http-request":e.getQrcode2,"on-remove":e.handleQrcode2Remove,accept:"image/*"}},[o("i",{class:e.form.qrcode2?"el-icon-close":"el-icon-plus",attrs:{slot:"default"},slot:"default"})])],1),e._v(" "),o("el-form-item",{attrs:{label:"报名截止时间",prop:"deadline"}},[o("el-date-picker",{attrs:{type:"datetime",placeholder:"选择日期时间"},model:{value:e.form.deadline,callback:function(t){e.$set(e.form,"deadline",t)},expression:"form.deadline"}})],1),e._v(" "),o("el-form-item",{attrs:{label:"活动起止时间",prop:"time_range"}},[o("el-date-picker",{attrs:{type:"datetimerange","range-separator":"至","start-placeholder":"开始日期","end-placeholder":"结束日期"},model:{value:e.form.time_range,callback:function(t){e.$set(e.form,"time_range",t)},expression:"form.time_range"}})],1),e._v(" "),o("h2",[o("i",{staticClass:"el-icon-document"}),e._v(" 岗位设置\n  ")]),e._v(" "),e._l(e.form.jobs,(function(t,r){return o("el-card",{key:r,staticStyle:{"margin-bottom":"20px"}},[o("div",{staticClass:"clearfix",attrs:{slot:"header"},slot:"header"},[o("span",[o("i",{staticClass:"el-icon-setting"}),e._v("\n        岗位"+e._s(r+1)+"\n      ")]),e._v(" "),o("el-button",{staticStyle:{float:"right",padding:"3px 0"},attrs:{type:"text"},on:{click:function(o){return e.rmjob(t)}}},[o("i",{staticClass:"el-icon-delete"}),e._v(" 删除岗位\n      ")])],1),e._v(" "),o("el-form-item",{attrs:{rules:{required:!0,message:"请输入岗位名称",trigger:"blur"},label:"名称"}},[o("el-input",{staticClass:"short",model:{value:t.job_name,callback:function(o){e.$set(t,"job_name",o)},expression:"job.job_name"}})],1),e._v(" "),o("el-form-item",{attrs:{rules:{required:!0,message:"请选择岗位工时",trigger:"blur"},label:"工时"}},[o("el-input",{staticClass:"short",model:{value:t.job_worktime,callback:function(o){e.$set(t,"job_worktime",o)},expression:"job.job_worktime"}})],1),e._v(" "),o("el-form-item",{attrs:{rules:{required:!0,message:"请输入岗位描述",trigger:"blur"},label:"描述"}},[o("el-input",{staticClass:"short",model:{value:t.job_content,callback:function(o){e.$set(t,"job_content",o)},expression:"job.job_content"}})],1),e._v(" "),o("el-form-item",{attrs:{rules:{required:!0,message:"请设置岗位人数",trigger:"blur"},label:"人数"}},[o("el-input",{staticClass:"short",model:{value:t.job_require_num,callback:function(o){e.$set(t,"job_require_num",o)},expression:"job.job_require_num"}})],1)],1)})),e._v(" "),o("div",{staticStyle:{margin:"20px"}},[o("el-button",{on:{click:e.addJob}},[o("i",{staticClass:"el-icon-plus"},[e._v("新增岗位")])])],1),e._v(" "),o("h2",[o("i",{staticClass:"el-icon-edit"}),e._v(" 报名问卷\n  ")]),e._v(" "),e._l(e.form.form,(function(t,r){return o("el-card",{key:t.index,staticStyle:{"margin-bottom":"20px"}},[o("div",{staticClass:"clearfix",attrs:{slot:"header"},slot:"header"},[o("span",[o("i",{staticClass:"el-icon-setting"}),e._v(" "),"name"==t.bind?o("span",[e._v("\n          报名表单项"+e._s(r+1)+"（该选项以姓名为默认值）\n          "),o("el-tooltip",{attrs:{content:"填写时默认填充项为报名者姓名",placement:"top"}},[o("i",{staticClass:"el-icon-info hb"})])],1):"phone"==t.bind?o("span",[e._v("\n          报名表单项"+e._s(r+1)+"（该选项以电话为默认值）\n          "),o("el-tooltip",{attrs:{content:"填写时默认填充项为报名者联系电话",placement:"top"}},[o("i",{staticClass:"el-icon-info hb"})])],1):"department"==t.bind?o("span",[e._v("\n          报名表单项"+e._s(r+1)+"（该选项以院系为默认值）\n          "),o("el-tooltip",{attrs:{content:"填写时默认填充项为报名者院系",placement:"top"}},[o("i",{staticClass:"el-icon-info hb"})])],1):"text"==t.type?o("span",[e._v("报名表单项"+e._s(r+1)+"（文本）")]):"radioBox"==t.type?o("span",[e._v("报名表单项"+e._s(r+1)+"（单选）")]):"checkBox"==t.type?o("span",[e._v("报名表单项"+e._s(r+1)+"（多选）")]):e._e()]),e._v(" "),o("el-button",{staticStyle:{float:"right",padding:"3px 0"},attrs:{type:"text"},on:{click:function(o){return e.rmForm(t)}}},[o("i",{staticClass:"el-icon-delete"}),e._v(" 删除表单项\n    ")])],1),e._v(" "),o("el-form-item",{staticStyle:{margin:"10px 0px"},attrs:{label:"文字描述",rules:{required:!0,message:"请输入表单项名称",trigger:"blur"}}},[o("el-input",{staticClass:"short",model:{value:t.text,callback:function(o){e.$set(t,"text",o)},expression:"item.text"}})],1),e._v(" "),o("el-form-item",{attrs:{label:"是否必填"}},[o("el-switch",{model:{value:t.required,callback:function(o){e.$set(t,"required",o)},expression:"item.required"}})],1),e._v(" "),"text"!=t.type?o("el-form-item",{attrs:{label:"设置选项"}},["text"!=t.type?o("el-button",{on:{click:function(o){return e.addFormOption(t)}}},[o("i",{staticClass:"el-icon-plus"},[e._v("添加选项")])]):e._e()],1):e._e(),e._v(" "),e._l(t.options,(function(r,n){return o("el-form-item",{key:r.index,attrs:{label:"选项"+(n+1)}},[o("el-input",{staticClass:"short",model:{value:r.name,callback:function(t){e.$set(r,"name",t)},expression:"option.name"}}),e._v(" "),o("el-button",{on:{click:function(o){return e.rmFormOption(t,r)}}},[o("i",{staticClass:"el-icon-delete"})])],1)}))],2)})),e._v(" "),o("div",{staticStyle:{margin:"25px"}},[o("el-button",{on:{click:function(t){return e.addForm(0)}}},[o("i",{staticClass:"el-icon-plus"},[e._v("新增文本项")])]),e._v(" "),o("el-button",{on:{click:function(t){return e.addForm(1)}}},[o("i",{staticClass:"el-icon-plus"},[e._v("新增单选项")])]),e._v(" "),o("el-button",{on:{click:function(t){return e.addForm(2)}}},[o("i",{staticClass:"el-icon-plus"},[e._v("新增多选项")])])],1),e._v(" "),o("el-button",{attrs:{type:"primary"},on:{click:e.submitform}},[e._v("发起项目")])],2)},s=[],c={name:"launchform",data:function(){return{form:{title:void 0,content:void 0,requirements:void 0,cover:void 0,introduction:void 0,type:void 0,form:[{text:"姓名",required:!0,type:"text",bind:"name"},{text:"联系方式",required:!0,type:"text",bind:"phone"},{text:"院系",required:!0,type:"text",bind:"department"}],deadline:void 0,time_range:void 0,jobs:[{job_name:"job1",job_worktime:2.5,job_content:"job1content1",job_require_num:250}],qrcode1:void 0,qrcode2:void 0},rules:{title:[{required:!0,message:"请输入项目标题",trigger:"blur"}],content:{required:!0,message:"请输入项目详情",trigger:"blur"},introduction:{required:!0,message:"请输入项目简介",trigger:"blur"},type:{required:!0,message:"请选择项目标签",trigger:"blul"},requirements:{required:!0,message:"请输入项目需求",trigger:"blur"},deadline:{required:!0,message:"请选择报名截止时间",trigger:"blur"},time_range:{required:!0,message:"请选择活动起止时间",trigger:"blur"},jobs:{required:!0,message:"请添加至少一个岗位",trigger:"blur"},form_content:{required:!0,message:"请输入表单项名称",trigger:"blur"},form_option:{required:!0,message:"请输入选项名称",trigger:"blur"},job_name:{required:!0,message:"请输入岗位名称",trigger:"blur"},job_content:{required:!0,message:"请输入岗位描述",trigger:"blur"},cover:{required:!0,message:"请上传封面图片",trigger:"blur"}}}},methods:{rmjob:function(e){console.log(e);var t=this.form.jobs.indexOf(e);-1!==t&&this.form.jobs.splice(t,1)},addJob:function(){this.form.jobs.push({})},clearValidate:function(e){this.$refs.mainform.clearValidate(e)},addForm:function(e){0==e?this.form.form.push({type:"text"}):1==e?this.form.form.push({type:"radioBox",options:[]}):2==e&&this.form.form.push({type:"checkBox",options:[]})},rmForm:function(e){var t=this.form.form.indexOf(e);-1!=t&&this.form.form.splice(t,1)},addFormOption:function(e){var t=this.form.form.indexOf(e);-1!=t&&this.form.form[t].options.push({name:""})},rmFormOption:function(e,t){var o=e.options.indexOf(t);-1!=o&&e.options.splice(o,1)},submitform:function(){var e=this,t=this;this.$refs.uploader.submit(),console.log(this.form),this.$refs.mainform.validate((function(o){if(console.log(o),o){console.log("旧：",e.form);var r=new FormData;r.append("title",e.form.title),r.append("content",e.form.content),r.append("introduction",e.form.introduction),r.append("requirements",e.form.requirements),r.append("type",e.form.type),r.append("cover",e.form.cover),r.append("deadline",new Date(e.form.deadline).toISOString()),r.append("begin_datetime",new Date(e.form.time_range[0]).toISOString()),r.append("end_datetime",new Date(e.form.time_range[1]).toISOString()),r.append("jobs",JSON.stringify(e.form.jobs)),r.append("form",JSON.stringify(e.form.form)),e.form.qrcode1&&(r.append("qrcode_1",e.form.qrcode1),console.log("qrcode1 added")),e.form.qrcode2&&(r.append("qrcode_2",e.form.qrcode2),console.log("qrcode2 added")),Object(l["g"])(r).then((function(e){Object(i["Message"])({message:"成功发起项目",type:"success",duration:5e3}),t.$router.push({path:"/dashboard"})})).catch((function(e){Object(i["Message"])({message:"错误："+e,type:"error",duration:5e3})}))}}))},getFile:function(e){console.log("重置cover！"),this.$refs.mainform.clearValidate("cover"),this.form.cover=e.file},handleCoverRemove:function(){console.log("清除cover！"),this.form.cover=void 0},getQrcode1:function(e){console.log("重置qrcode1"),this.form.qrcode1=e.file},handleQrcode1Remove:function(){console.log("清除qrcode1"),this.form.qrcode1=void 0},getQrcode2:function(e){console.log("重置qrcode2"),this.form.qrcode2=e.file},handleQrcode2Remove:function(){console.log("清除qrcode2"),this.form.qrcode2=void 0}}},u=c,m=(o("df49"),o("2877")),d=Object(m["a"])(u,a,s,!1,null,null,null),p=d.exports,f={name:"Project",components:{launchform:p},data:function(){return{}},methods:{}},b=f,v=Object(m["a"])(b,r,n,!1,null,null,null);t["default"]=v.exports},"24d2":function(e,t,o){"use strict";o.d(t,"e",(function(){return n})),o.d(t,"d",(function(){return i})),o.d(t,"a",(function(){return l})),o.d(t,"f",(function(){return a})),o.d(t,"b",(function(){return s})),o.d(t,"i",(function(){return c})),o.d(t,"h",(function(){return u})),o.d(t,"g",(function(){return m})),o.d(t,"c",(function(){return d}));var r=o("b775");function n(e){return Object(r["a"])({url:"/project/detail?id=".concat(e),method:"get"})}function i(e){return Object(r["a"])({url:"/check/ViewApplyInfo?project_id=".concat(e),method:"get"})}function l(e,t){return Object(r["a"])({url:"/check/CheckOp",method:"post",data:{apply_id:e,checked:t}})}function a(){return Object(r["a"])({url:"/my/allproject",method:"get"})}function s(e){return Object(r["a"])({url:"/worktime/Export?project_id=".concat(e),method:"get"})}function c(e){return Object(r["a"])({url:"/worktime/import",method:"post",data:e})}function u(e){return Object(r["a"])({url:"/sign/project",method:"post",data:e})}function m(e){return Object(r["a"])({method:"post",url:"/project/detail",data:e})}function d(e,t){return Object(r["a"])({method:"put",url:"/project/detail?id=".concat(e),data:{finished:!0}})}},"745c":function(e,t,o){},b775:function(e,t,o){"use strict";var r=o("bc3a"),n=o.n(r),i=(o("5c96"),n.a.create({baseURL:"/api",timeout:5e3}));i.interceptors.request.use((function(e){return e}),(function(e){return Promise.reject(e)})),i.interceptors.response.use((function(e){return 200!==e.status?Promise.reject(new Error(e.data||"Error")):e}),(function(e){return Promise.reject(e)})),t["a"]=i},df49:function(e,t,o){"use strict";var r=o("745c"),n=o.n(r);n.a}}]);