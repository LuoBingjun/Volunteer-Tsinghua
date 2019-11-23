<template>
  <div>
    <h1>志愿清华团体版主页</h1>
    <h2>发起新项目</h2>
    <div>
        <p><label>项目名称</label> <input type = "text" v-model = "title"/></p>
        <p><label>项目详情</label> <textarea type = "text" v-model = "content"/></p>
        <p><label>封面图片</label> <input type="file" id = "coverFile" @change="uploadCover"/></p>
        <p><label>需求</label> <textarea type = "text" v-model = "requirements"/></p>
        <p><label>截止时间</label> 日期：<textarea type = "text" v-model = "deadlineDate"/> 
                                时刻：<textarea type = "text" v-model = "deadlineTime"/></p>

        <div id = "jobs">
          <div class = "oneJob" v-for = "(job,index) in jobs">
            <h2>岗位{{job.job_name}}</h2>
            <p><button :data-index="index" @click="deleteThisJob" > 删除此岗位</button></p>
            <p><label>岗位名称</label> <input type = "text" v-model = "job.job_name"/></p>
            <p><label>岗位工时</label> <input type = "text" v-model = "job.job_worktime"/></p>
            <p><label>岗位要求描述</label> <textarea type = "text" v-model = "job.job_content"/></p>
            <p><label>岗位需求人数</label> <input type="text" oninput="value=value.replace(/[^\d]/g,'')" v-model = "job.job_require_num"/> </p>
          </div>
        </div>
        

        <p><button @click="addNewJob" > 添加岗位</button></p>
        
        
        
        <p><button @click="submit" > 建立新项目</button></p>
    </div>   
  </div>
</template>

<script>
import {Message} from 'element-ui'
import request from '@/api/request.js'
export default {
  name: 'Project',
  
  data () {
    return {
        submitData: undefined,
        "title": "标题",
        "content": "详情",
        "requirements": "需求" ,
        "form": "json文本",
        "deadlineDate": "2019-12-31",
        "deadlineTime": "23:59:59",
        "jobs":
        [
          {
            "job_name":"job1",
            "job_worktime":3.5,
            "job_content":"job1content1",
            "job_require_num":250
			    }
        ]
    }
  },
  methods:{
    submit(){
        let that = this
        console.log('点击LaunchProject提交按钮, this.&data:', this.$data)
        
        if(!that.submitData)
        {
            Message({
                message: '请上传封面图片！',
                type: 'error',
                duration: 5 * 1000
            })
            return
        }
        that.submitData.append("title", that.title)
        that.submitData.append("content", that.content)
        that.submitData.append("require_num", parseInt(that.require_num))
        that.submitData.append("requirements", that.requirements)
        that.submitData.append("deadline", that.deadlineDate + 'T' + that.deadlineTime)
        that.submitData.append("jobs", that.jobs)
        console.log("that.jobs:", that.jobs)
        console.log('LaunchProject中请求数据:that.submitData', JSON.stringify(that.submitData))
        request({
            method:"post",
            url: '/project/detail',
            headers: {
            'Content-Type': 'multipart/form-data'
            },
            data:that.submitData
        }).then(res=>{
            console.log(res)
            
        }).catch(err =>{
            console.log('LaunchProject发现错误：', err)
            Message({
                message: 'Error request'+err,
                type: 'error',
                duration: 5 * 1000
            })
        })
    },
    uploadCover(event){
        var that = this
        console.log(event);

        let file = event.target.files
        that.submitData = new FormData();
        let formData = that.submitData
        formData.append('category', 'settingPic')
        formData.append('cover', file[0])
        console.log(formData);

    },
    addNewJob(event){
        console.log("addNewJob按钮按下")
        var that = this
        that.$data.jobs.push({
            "job_name":"newJob",
            "job_worktime":5,
            "job_content":"newJobContent",
            "job_require_num":10
        })
        console.log("addNewJob that.jobs:", that.$data.jobs)
    },
    deleteThisJob(event){
        let target = event.target
        console.log("target:",target)
        let jobIndex = target.getAttribute("data-index")
        this.jobs.splice(jobIndex, 1)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
