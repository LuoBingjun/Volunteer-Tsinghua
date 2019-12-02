<template>
  <el-form :model="form" :rules="rules" label-width="auto" ref="mainform">
    <el-form-item label="项目标题" prop="title" class="short">
      <el-input v-model="form.title"></el-input>
    </el-form-item>
    <el-form-item label="项目详情" prop="content" class="short">
      <el-input v-model="form.content"></el-input>
    </el-form-item>
    <el-form-item label="项目需求" prop="requirements">
      <el-input type="textarea" v-model="form.requirements"></el-input>
    </el-form-item>
    <el-form-item label="封面图片" prop="cover" ref="upload_item">
      <el-upload action="#" 
        list-type="picture-card"
        :auto-upload="true" 
        :multiple="false"
        :limit="1" 
        name="cover"
        :http-request="getFile"
        ref="uploader"
        :on-remove="handleCoverRemove"
      >
      <i slot="default" class="el-icon-plus"></i>
      </el-upload>
    </el-form-item>
    
    <el-form-item label="报名表单设计" prop="form">
    </el-form-item>
    <el-card v-for="(item,index) in form.form" :key="item.index">
      <label>
        <i class="el-icon-setting"></i>
        <span v-if="item.bind=='name'">报名表单项{{index}}（该选项以姓名为默认值）
          <el-tooltip content="报名人填写时，默认填充项为其姓名" placement="top">
            <i class="el-icon-info hb"></i>
          </el-tooltip>
        </span>
        <span v-else-if="item.bind=='phone'">报名表单项{{index}}（该选项以电话为默认值）
          <el-tooltip content="报名人填写时，默认填充项为其联系电话" placement="top">
            <i class="el-icon-info hb"></i>
          </el-tooltip>
        </span>
        <span v-else-if="item.bind=='school'">报名表单项{{index}}（该选项以院系为默认值）
          <el-tooltip content="报名人填写时，默认填充项为其院系" placement="top">
            <i class="el-icon-info hb"></i>
          </el-tooltip>
        </span>
        <span v-else>报名表单项{{index}}</span>
      </label>
      <el-form-item label="文字描述" :rules="{required:true,message:'请输入表单项名称',trigger:'blur'}" style="margin:10px 0px">
        <el-input v-model="item.text" class="short"></el-input>
      </el-form-item>
      <el-form-item label="是否必填">
        <el-switch v-model="item.required"></el-switch>
      </el-form-item>
      <el-form-item label="设置选项" v-if="item.type!='text'" >
        <el-button v-if="item.type!='text'" @click="addFormOption(item)">
          <i class="el-icon-plus">添加选项</i>
        </el-button>
      </el-form-item>
      <el-form-item v-for="(option,index) in item.options" :key="option.index" :label="'选项'+index">
        <el-input v-model="option.name" class="short"></el-input>
        <el-button @click="rmFormOption(item,option)">
          <i class='el-icon-delete'></i> 删除选项
        </el-button>
      </el-form-item>
      <el-button @click="rmForm(item)">
        <i class='el-icon-delete'></i> 删除表单项
      </el-button>
    </el-card>
    <div style="margin:25px">
      <el-button @click="addForm(0)">
        <i class="el-icon-plus"> 新增文本项</i>
      </el-button>
      <el-button @click="addForm(1)">
        <i class="el-icon-plus"> 新增单选项</i>
      </el-button>
      <el-button @click="addForm(2)">
        <i class="el-icon-plus"> 新增多选项</i>
      </el-button>
    </div>
    <el-form-item label="报名截止时间" prop="deadline">
      <el-date-picker
        v-model="form.deadline"
        type="datetime"
        placeholder="选择日期时间">
      </el-date-picker>
    </el-form-item>
    <el-form-item label="活动起止时间" prop="time_range">
      <el-date-picker
        v-model="form.time_range"
        type="datetimerange"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期">
      </el-date-picker>
    </el-form-item>
    <el-form-item label="岗位安排" prop="jobs">

    </el-form-item>
    <el-card v-for="(job,index) in form.jobs" :key="index">
      <label>
        <i class="el-icon-setting"></i>
        岗位{{index}}
      </label>
      <el-form-item :rules="{required:true,message:'请输入岗位名称',trigger:'blur'}" label="名称">
        <el-input v-model="job.job_name" class="short"></el-input>
      </el-form-item>
      <el-form-item :rules="{required:true,message:'请选择岗位工时',trigger:'blur'}" label="工时">
        <el-input v-model="job.job_worktime" class="short"></el-input>
      </el-form-item>
      <el-form-item :rules="{required:true,message:'请输入岗位描述',trigger:'blur'}" label="描述">
        <el-input v-model="job.job_content" class="short"></el-input>
      </el-form-item>
      <el-form-item :rules="{required:true,message:'请设置岗位人数',trigger:'blur'}" label="人数">
        <el-input v-model="job.job_require_num" class="short"></el-input>
      </el-form-item>
      <el-button @click="rmjob(job)"><i class='el-icon-delete'></i> 删除岗位</el-button>
    </el-card>
    <div style="margin:25px">
      <el-button @click="addJob">
        <i class="el-icon-plus"> 新增岗位</i>
      </el-button>
    </div>
    <el-button type="primary" @click="submitform">发起项目</el-button>
  </el-form>
        
</template>

<script>
import {startProject} from "@/api/project"
import {Message} from "element-ui"
export default {
  name: "launchform",
  data(){
    return{
      form:{
        title:undefined,
        content:undefined,
        requirements:undefined,
        cover:undefined,
        form:[
          {
            text:"姓名",
            required:true,
            type:"text",
            bind:"name"
          },{
            text:"联系方式",
            required:true,
            type:"text", 
            bind:"phone"
          },{
            text:"院系",
            required:true,
            type:"text",
            bind:"school"
          }
        ],
        deadline:undefined,
        begin_datetime:undefined,
        end_datetime:undefined,
        time_range:undefined,
        jobs:[{
            "job_name":"job1",
            "job_worktime":2.5,
            "job_content":"job1content1",
            "job_require_num":250
          },
          {
            "job_name":"job2",
            "job_worktime":250.0,
            "job_content":"job2content2",
            "job_require_num":25
          }]
      },
      rules:{
        title:[{required:true,message:'请输入项目标题', trigger:'blur'}],
        content:{required:true,message:'请输入项目详情', trigger:'blur'},
        requirements:{required:true,message:'请输入项目需求', trigger:'blur'},
        deadline:{required:true,message:'请选择报名截止时间', trigger:'blur'},
        time_range:{required:true,message:'请选择活动起止时间',trigger:'blur'},
        jobs:{required:true,message:'请添加至少一个岗位',trigger:'blur'},
        form_content:{required:true,message:'请输入表单项名称',trigger:'blur'},
        form_option:{required:true,message:'请输入选项名称',trigger:'blur'},
        job_name:{required:true,message:'请输入岗位名称',trigger:'blur'},
        job_content:{required:true,message:'请输入岗位描述',trigger:'blur'},
        cover:{required:true,message:'请上传封面图片',trigger:'blur'}
      },
    }
  },
  created(){
    this.form.requirements="需求"
  },
  methods:{
    rmjob(item){
      console.log(item)
      var index = this.form.jobs.indexOf(item)
      if (index !== -1) {
        this.form.jobs.splice(index, 1)
      }
    },
    addJob()
    {
      this.form.jobs.push({})
    },
    addForm(type)
    {
      if(type==0)
      {
        this.form.form.push({type:'text'})
      }
      else if(type==1)
      {
        this.form.form.push({type:'radioBox',options:[]})
      }
      else if(type==2)
      {
        this.form.form.push({type:'checkBox',options:[]})
      }
    },
    rmForm(item)
    {
      var index=this.form.form.indexOf(item)
      if(index!=-1)this.form.form.splice(index,1)
    },
    addFormOption(item)
    {
      var index=this.form.form.indexOf(item)
      if(index!=-1)
      {
        this.form.form[index].options.push({"name":""})
      }
    },
    rmFormOption(item,option)
    {
      var index=item.options.indexOf(option)
      if(index!=-1)
      {
        item.options.splice(index,1)
      }
    },
    submitform(){
      this.$refs.uploader.submit()  //getfile
      console.log(this.form)
      this.$refs.mainform.validate((valid)=>{
        console.log(valid)
        if(valid){
          console.log("旧：",this.form)
          var newform=new FormData()
          newform.append("title",this.form.title)
          newform.append("content",this.form.content)
          newform.append("requirements",this.form.requirements)
          newform.append("cover",this.form.cover)
          newform.append("deadline",new Date(this.form.deadline).toISOString())
          newform.append("begin_datetime",new Date(this.form.time_range[0]).toISOString())
          newform.append("end_datetime",new Date(this.form.time_range[1]).toISOString())
          newform.append("jobs",JSON.stringify(this.form.jobs))
          newform.append("form",JSON.stringify(this.form.form))
          console.log("新：",newform)
          startProject(newform).then(res=>{
            Message({
              message:"成功发起项目",
              type:"success",
              duration: 5000
            })
          }).catch(err=>{
            Message({
              message:"错误："+err,
              type:"error",
              duration:5000
            })
          })
        }
      })
    },
    getFile(file){
      console.log("重置cover！")
      this.$refs.mainform.clearValidate("cover")
      this.form.cover=file.file
    },
    handleCoverRemove(){
      console.log("清除cover！")
      this.form.cover=undefined
    }
  }
}
</script>
<style>
.short{
  width:40%
}
i.hb:hover{
  color:blue
}
</style>