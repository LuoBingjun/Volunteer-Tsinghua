<template>
  <el-form :model="form" :rules="rules" ref="form">
    <el-form-item label="签到标题" prop="title">
      <el-input v-model="form.title"></el-input>
    </el-form-item>
    <el-form-item label="签到描述" prop="content">
      <el-input v-model="form.content"></el-input>
    </el-form-item>
    <el-form-item label="签到起止时间" prop="time_range">
      <el-date-picker
        v-model="form.time_range"
        type="datetimerange"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        :default-time="['00:00:00']">
      </el-date-picker>
    </el-form-item>
    <el-form-item label="岗位安排" prop="jobs">
      <el-checkbox :indeterminate="isIndeterminate" v-model="checkAll" @change="handleJobsCheckAll">全选</el-checkbox>
      <el-checkbox-group v-model="form.jobs">
        <el-checkbox v-for="job in jobs" :label="job.id" :key="job.id" @change="handleJobsCheck">{{job.job_name}}</el-checkbox>
      </el-checkbox-group>
    </el-form-item>
    <el-form-item label="签到地点" prop="pos">
      <qqmap @input="handleMapInput" />
    </el-form-item>
    <el-button @click="startSign" type="primary" style="margin:10px 0px">发起签到</el-button>
    </el-form>
</template>
<script>
import {startSign} from '@/api/project'
import {Message} from 'element-ui'
import qqmap from '@/components/qqmap'
export default {
  name:'signform',
  props:["jobs","projectID"],
  components:{qqmap},
  created(){
    this.alljobs=[]
    for(var i in this.jobs)
    {
      this.alljobs.push(this.jobs[i].id)
    }
    console.log(this.alljobs)
  },
  data(){
    var validatepos=(rule,value,callback)=>{
      if(!value||!value.text)callback(new Error('请在上方输入框填写活动地址'))
      else callback()
    }
    return {
      form:{
        title: undefined,
        content: undefined,
        time_range:undefined,
        jobs:[],
        pos:{pos:"40.0024431613261,116.3263320",text:undefined}
      },
      alljobs:undefined,
      isIndeterminate:undefined,
      checkAll:undefined,

      rules:{
        title: {required: true, message:'请输入签到标题', trigger:'blur'},
        content: {required: true, message:'请输入签到描述', trigger:'blur'},
        time_range: {required: true, message: '请输入起止时间', trigger:'blur'},
        jobs: {required: true, message: '请至少安排一个岗位', trigger:'blur'},
        pos: {required:true,validator:validatepos,trigger:'blur'}
      }
    }
  },
  methods:{
    handleJobsCheck(value){
      let checkedCount = this.form.jobs.length;
      this.checkAll = (checkedCount === this.jobs.length);
      this.isIndeterminate = checkedCount > 0 && checkedCount < this.jobs.length;
    },
    handleJobsCheckAll(val){
      this.form.jobs = val ? this.alljobs : [];
      this.isIndeterminate = false;
    },
    startSign()
    {
      console.log()
      this.$refs['form'].validate((valid)=>{
        if(valid){
          var newForm={
            title:this.form.title,
            content:this.form.content,
            begin_time:new Date(this.form.time_range[0]).toISOString(),
            end_time:new Date(this.form.time_range[1]).toISOString(),
            jobs:this.form.jobs,
            project:this.projectID,
            longitude:this.form.pos.pos.lng,
            latitude:this.form.pos.pos.lat,
            position:this.form.pos.text
          }
          console.log(newForm)
          startSign(newForm).then(res=>{
            Message({
              message: '成功发起签到',
              type: 'success',
              duration: 5 * 1000
            })
          }).catch(err=>{
            Message({
              message: '发起签到失败：'+err,
              type: 'error',
              duration: 5 * 1000
            })
          })
        }
      })
    },
    handleMapInput(ev){
      this.form.pos.text=ev.text
      if(ev.pos)this.form.pos.pos=ev.pos
      if(ev.text)this.$refs.form.clearValidate("pos")
      console.log("收到了",this.form.pos)
    }
  }
}
</script>

