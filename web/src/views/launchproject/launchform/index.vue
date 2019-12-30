<template>
  <el-form :model="form" :rules="rules" label-width="auto" ref="mainform">
    <h2>
      <i class="el-icon-news" /> 基本信息
    </h2>
    <el-form-item label="项目标题" prop="title" class="short">
      <el-input v-model="form.title" placeholder="请输入项目标题"></el-input>
    </el-form-item>
    <el-form-item label="项目简介" prop="introduction">
      <el-input v-model="form.introduction" placeholder="请输入项目简介（不超过20个中文字符）"></el-input>
    </el-form-item>
    
    <el-form-item label="选择标签" prop="type">
      <el-select placeholder="请选择项目标签" v-model="form.type" @input="clearValidate('type')">
        <el-option label="文化教育" value="WH"></el-option>
        <el-option label="赛会服务" value="SH"></el-option>
        <el-option label="社区服务" value="SQ"></el-option>
        <el-option label="医疗健康" value="YL"></el-option>
        <el-option label="健康残障" value="JK"></el-option>
        <el-option label="校园讲解" value="XY"></el-option>
        <el-option label="其他项目" value="QT"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="项目地点" prop="loc">
      <el-input v-model="form.loc" placeholder="请填写活动地点"></el-input>
    </el-form-item>
    <el-form-item label="项目详情" prop="content">
      <el-input v-model="form.content" type="textarea" :rows="6"></el-input>
    </el-form-item>
    <el-form-item label="项目需求" prop="requirements">
      <el-input type="textarea" v-model="form.requirements" :rows="6"></el-input>
    </el-form-item>
    <el-form-item label="封面图片 (宽高比2:1)" prop="cover" ref="upload_item">
      <el-upload
        action="#"
        list-type="picture-card"
        :auto-upload="true"
        :multiple="false"
        :limit="1"
        name="cover"
        :http-request="getFile"
        ref="uploader"
        :on-remove="handleCoverRemove"
        accept="image/*"
      >
        <i slot="default" :class="form.cover?'el-icon-close':'el-icon-plus'"></i>
      </el-upload>
    </el-form-item>
    <el-form-item prop="success_note">
      <div slot="label"> 
        报名成功提示
        <el-tooltip content="报名成功后显示给志愿者的提示信息">
          <i class="el-icon-question"></i> 
        </el-tooltip>
      </div>
      <el-input v-model="form.success_note"></el-input>
    </el-form-item>

    <el-form-item ref="upload_qrcode1">
      <div slot='label'>
        <span>
          活动群二维码
          <el-tooltip content="不是必填项，仅报名成功后可见">
            <i class="el-icon-question"></i>
          </el-tooltip>
        </span>
      </div>
      <el-upload
        action="#"
        list-type="picture-card"
        :auto-upload="true"
        :multiple="false"
        :limit="1"
        name="cover"
        :http-request="getQrcode1"
        ref="uploader1"
        :on-remove="handleQrcode1Remove"
        accept="image/*"
      >
        <i slot="default" :class="form.qrcode1?'el-icon-close':'el-icon-plus'"></i>
      </el-upload>
    </el-form-item>

    <el-form-item ref="upload_qrcode2">
      <div slot='label'>
        <span>
          负责人二维码
          <el-tooltip content="不是必填项，仅报名成功后可见">
            <i class="el-icon-question"></i>
          </el-tooltip>
        </span>
      </div>
      <el-upload
        action="#"
        list-type="picture-card"
        :auto-upload="true"
        :multiple="false"
        :limit="1"
        name="cover"
        :http-request="getQrcode2"
        ref="uploader2"
        :on-remove="handleQrcode2Remove"
        accept="image/*"
      >
        <i slot="default" :class="form.qrcode2?'el-icon-close':'el-icon-plus'"></i>
      </el-upload>
    </el-form-item>

    <el-form-item label="报名截止时间" prop="deadline">
      <el-date-picker v-model="form.deadline" type="datetime" placeholder="选择日期时间"></el-date-picker>
    </el-form-item>
    <el-form-item label="活动起止时间" prop="time_range">
      <el-date-picker
        v-model="form.time_range"
        type="datetimerange"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
      ></el-date-picker>
    </el-form-item>

    <h2>
      <i class="el-icon-document" /> 岗位设置
    </h2>
    <el-card v-for="(job,index) in form.jobs" :key="index" style="margin-bottom:20px;">
      <div slot="header" class="clearfix">
        <span>
          <i class="el-icon-setting"></i>
          岗位{{index + 1}}
        </span>
        <el-button @click="rmjob(job)" style="float: right; padding: 3px 0" type="text">
          <i class="el-icon-delete"></i> 删除岗位
        </el-button>
      </div>
      <el-form-item :prop="'jobs.'+index+'.job_name'" :rules="{required:true,message:'请输入岗位名称',trigger:'blur'}" label="名称">
        <el-input v-model="job.job_name" class="short"></el-input>
      </el-form-item>
      <el-form-item :prop="'jobs.'+index+'.job_worktime'" 
        :rules="[{required:true,message:'请选择岗位工时',trigger:'blur'},
                 {validator:worktimeValidator,trigger:'blur'}]"
        label="工时">
        <el-input v-model="job.job_worktime" class="short"></el-input>
      </el-form-item>
      <el-form-item :prop="'jobs.'+index+'.job_content'" :rules="{required:true,message:'请输入岗位描述',trigger:'blur'}" label="描述">
        <el-input v-model="job.job_content" class="short"></el-input>
      </el-form-item>
      <el-form-item :prop="'jobs.'+index+'.job_require_num'" 
        :rules="[{required:true,message:'请设置岗位人数',trigger:'blur'},
                 {validator:requirenumValidator,trigger:'blur'}]" label="人数">
        <el-input v-model="job.job_require_num" class="short"></el-input>
      </el-form-item>
    </el-card>
    <div style="margin:20px">
      <el-button @click="addJob">
        <i class="el-icon-plus">新增岗位</i>
      </el-button>
    </div>

    <h2>
      <i class="el-icon-edit" /> 报名问卷
    </h2>
    <!-- <el-form-item label="报名表单设计" prop="form">
    </el-form-item>-->
    <el-card v-for="(item,index) in form.form" :key="item.index" style="margin-bottom:20px;">
      <div slot="header" class="clearfix">
        <span>
          <i class="el-icon-setting"></i>
          <span v-if="item.bind=='name'">
            报名表单项{{index+1}}（该选项以姓名为默认值）
            <el-tooltip content="填写时默认填充项为报名者姓名" placement="top">
              <i class="el-icon-info hb"></i>
            </el-tooltip>
          </span>
          <span v-else-if="item.bind=='phone'">
            报名表单项{{index+1}}（该选项以电话为默认值）
            <el-tooltip content="填写时默认填充项为报名者联系电话" placement="top">
              <i class="el-icon-info hb"></i>
            </el-tooltip>
          </span>
          <span v-else-if="item.bind=='department'">
            报名表单项{{index+1}}（该选项以院系为默认值）
            <el-tooltip content="填写时默认填充项为报名者院系" placement="top">
              <i class="el-icon-info hb"></i>
            </el-tooltip>
          </span>
          <span v-else-if="item.type=='text'">报名表单项{{index+1}}（文本）</span>
          <span v-else-if="item.type=='radioBox'">报名表单项{{index+1}}（单选）</span>
          <span v-else-if="item.type=='checkBox'">报名表单项{{index+1}}（多选）</span>
        </span>
              <el-button @click="rmForm(item)" style="float: right; padding: 3px 0" type="text">
        <i class="el-icon-delete"></i> 删除表单项
      </el-button>
      </div>

      <el-form-item
        label="文字描述" :prop="'form.'+index+'.text'"
        :rules="{required:true,message:'请输入表单项名称',trigger:'blur'}"
        style="margin:10px 0px"
      >
        <el-input v-model="item.text" class="short"></el-input>
      </el-form-item>
      <el-form-item label="是否必填">
        <el-switch v-model="item.required"></el-switch>
      </el-form-item>
      <el-form-item label="设置选项" v-if="item.type!='text'">
        <el-button v-if="item.type!='text'" @click="addFormOption(item)">
          <i class="el-icon-plus">添加选项</i>
        </el-button>
      </el-form-item>
      <el-form-item v-for="(option,index2) in item.options" :key="index2" :label="'选项'+(index2+1)"
        :prop="'form.'+index+'.options.'+index2+'.name'" :rules="{required:true,trigger:'blur',message:'选项不能为空'}">
        <el-input v-model="option.name" class="short"></el-input>
        <el-button @click="rmFormOption(item,option)">
          <i class="el-icon-delete"></i>
        </el-button>
      </el-form-item>
    </el-card>
    <div style="margin:25px">
      <el-button @click="addForm(0)">
        <i class="el-icon-plus">新增文本项</i>
      </el-button>
      <el-button @click="addForm(1)">
        <i class="el-icon-plus">新增单选项</i>
      </el-button>
      <el-button @click="addForm(2)">
        <i class="el-icon-plus">新增多选项</i>
      </el-button>
    </div>
    <el-button type="primary" @click="submitform" :loading="loading">发起项目</el-button>
  </el-form>
</template>

<script>
import { startProject } from "@/api/project";
import { Message } from "element-ui";
export default {
  name: "launchform",
  data() {
    return {
      form: {
        title: undefined,
        content: undefined,
        requirements: undefined,
        cover: undefined,
        introduction: undefined,
        type:undefined,
        loc:undefined,
        success_note:"报名成功！",
        form: [
          {
            text: "姓名",
            required: true,
            type: "text",
            bind: "name"
          },
          {
            text: "联系方式",
            required: true,
            type: "text",
            bind: "phone"
          },
          {
            text: "院系",
            required: true,
            type: "text",
            bind: "department"
          }
        ],
        deadline: undefined,
        time_range: undefined,
        jobs: [
          {
            job_name: "",
            job_worktime: "",
            job_content: "",
            job_require_num: ""
          }
        ],
        qrcode1:undefined,
        qrcode2:undefined
      },
      rules: {
        title: [{ required: true, message: "请输入项目标题", trigger: "blur" }],
        content: { required: true, message: "请输入项目详情", trigger: "blur" },
        introduction: [{required: true, message: "请输入项目简介", trigger: "blur" },
                       {max:20,message:"简介不能超过20个中文字符",trigger:'change' }],
        type:{required:true,message:"请选择项目标签",trigger:"blur"},
        requirements: {
          required: true,
          message: "请输入项目需求",
          trigger: "blur"
        },
        deadline: {
          required: true,
          message: "请选择报名截止时间",
          trigger: "blur"
        },
        time_range: {
          required: true,
          message: "请选择活动起止时间",
          trigger: "blur"
        },
        loc: {
          required: true,
          message: "请填写活动地点",
          trigger: "blur"
        },
        jobs: {
          required: true,
          message: "请添加至少一个岗位",
          trigger: "blur"
        },
        form_content: {
          required: true,
          message: "请输入表单项名称",
          trigger: "blur"
        },
        form_option: {
          required: true,
          message: "请输入选项名称",
          trigger: "blur"
        },
        job_name: {
          required: true,
          message: "请输入岗位名称",
          trigger: "blur"
        },
        job_content: {
          required: true,
          message: "请输入岗位描述",
          trigger: "blur"
        },
        cover: { required: true, message: "请上传封面图片", trigger: "blur" }
      },
      loading:false
    };
  },
  computed:{
    worktimeValidator(){
      return function(rule,value,callback){
        var pattern=/^(0|[1-9][0-9]*)?(\.[0-9]*)?$/;
        if(pattern.test(value))
        {
          callback();
        }
        else
        {
          callback(new Error('工时必须是大于零的实数'))
        }
      }
    },
    requirenumValidator(){
      return function(rule,value,callback){
        var pattern=/^[1-9][0-9]*$/;
        if(pattern.test(value))
        {
          callback();
        }
        else
        {
          callback(new Error('人数必须是正整数'))
        }
      }
    }
  },
  methods: {
    rmjob(item) {
      console.log(item);
      var index = this.form.jobs.indexOf(item);
      if (index !== -1) {
        this.form.jobs.splice(index, 1);
      }
    },
    addJob() {
      this.form.jobs.push({});
    },
    clearValidate(type)
    {
      this.$refs.mainform.clearValidate(type)
    },
    addForm(type) {
      if (type == 0) {
        this.form.form.push({ type: "text" });
      } else if (type == 1) {
        this.form.form.push({ type: "radioBox", options: [] });
      } else if (type == 2) {
        this.form.form.push({ type: "checkBox", options: [] });
      }
    },
    rmForm(item) {
      var index = this.form.form.indexOf(item);
      if (index != -1) this.form.form.splice(index, 1);
    },
    addFormOption(item) {
      var index = this.form.form.indexOf(item);
      if (index != -1) {
        this.form.form[index].options.push({ name: "" });
      }
    },
    rmFormOption(item, option) {
      var index = item.options.indexOf(option);
      if (index != -1) {
        item.options.splice(index, 1);
      }
    },
    submitform() {
      var that = this;
      //this.$refs.uploader.submit(); //getfile
      console.log(this.form);
      this.loading=true
      this.$refs.mainform.validate(valid => {
        console.log(valid);
        if (valid) {
          console.log("旧：", this.form);
          var newform = new FormData();
          newform.append("title", this.form.title);
          newform.append("content", this.form.content);
          newform.append("introduction", this.form.introduction);
          newform.append("requirements", this.form.requirements);
          newform.append("loc", this.form.loc);
          newform.append("type", this.form.type);
          newform.append("cover", this.form.cover);
          newform.append("success_note", this.form.success_note);
          newform.append("deadline",new Date(this.form.deadline).toISOString());
          newform.append("begin_datetime",new Date(this.form.time_range[0]).toISOString());
          newform.append("end_datetime",new Date(this.form.time_range[1]).toISOString());
          newform.append("jobs", JSON.stringify(this.form.jobs));
          newform.append("form", JSON.stringify(this.form.form));
          
          if(this.form.qrcode1){newform.append("qrcode_1",this.form.qrcode1);console.log("qrcode1 added")}
          if(this.form.qrcode2){newform.append("qrcode_2",this.form.qrcode2);console.log("qrcode2 added")}
          startProject(newform)
            .then(res => {
              Message({
                message: "成功发起项目",
                type: "success",
                duration: 5000
              });
              that.$router.push({ path: "/dashboard" });
              that.loading=false
            })
            .catch(err => {
              var errcode=err.request.status
              console.log(errcode)
              if(errcode==400){
                Message({
                  message: "表单项不符合规则",
                  type: "error",
                  duration: 5000
                });
              }
              else{
                Message({
                  message: "错误："+err,
                  type: "error",
                  duration: 5000
                });
              }
              that.loading=false
            });
        }
        else
        {
          Message({message:"有项目不符合要求",type:"error",duration:"3000"})
          that.loading=false
        }
      });
    },
    getFile(file) {
      console.log("重置cover！",file);
      this.$refs.mainform.clearValidate("cover");
      var that=this
      new Promise(function(resolve,reject){
        let _URL=window.URL||window.webkitURL
        let img=new Image()
        img.onload=function(){
          let valid=(img.width==2*img.height)
          valid?resolve():reject()
        }
        img.src=_URL.createObjectURL(file.file)
      }).then(()=>{
        that.form.cover = file.file;
      }).catch(()=>{
        Message({
          message:"上传的图片不符合要求（要求宽高比2:1）",
          type:'warning',
          duration:5000
        })
        that.$refs.uploader.clearFiles()
      })
    },
    handleCoverRemove() {
      console.log("清除cover！");
      this.form.cover = undefined;
    },
    getQrcode1(file){
      console.log('重置qrcode1')
      this.form.qrcode1=file.file
    },
    handleQrcode1Remove(){
      console.log('清除qrcode1')
      this.form.qrcode1=undefined
    },
    getQrcode2(file){
      console.log('重置qrcode2')
      this.form.qrcode2=file.file
    },
    handleQrcode2Remove(){
      console.log('清除qrcode2')
      this.form.qrcode2=undefined
    },
  }
};
</script>
<style>
.short {
  width: 40%;
}
i.hb:hover {
  color: blue;
}
</style>