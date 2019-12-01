<template>
  <div>
    <el-card>
      <h1>
        <i class="el-icon-circle-plus"> 发起新项目</i>
      </h1>
    </el-card>
    
    <div>
        <p><label>项目名称</label> <input type = "text" v-model = "title"/></p>
        <p><label>项目详情</label> <textarea type = "text" v-model = "content"/></p>
        <p><label>封面图片</label> <input type="file" id = "coverFile" @change="uploadCover"/></p>
        <p><label>需求</label> <textarea type = "text" v-model = "requirements"/></p>
        <p><label>截止时间</label> 日期：<textarea type = "text" v-model = "deadlineDate"/> 
                                时刻：<textarea type = "text" v-model = "deadlineTime"/></p>

        <div id = "jobs">
          <div class = "oneJob" v-for = "(job,index) in jobs" :key="(job,index)">
            <h2>岗位{{job.job_name}}</h2>
            <p><button :data-index="index" @click="deleteThisJob" > 删除此岗位</button></p>
            <p><label>岗位名称</label> <input type = "text" v-model = "job.job_name"/></p>
            <p><label>岗位工时</label> <input type = "text" v-model = "job.job_worktime"/></p>
            <p><label>岗位要求描述</label> <textarea type = "text" v-model = "job.job_content"/></p>
            <p><label>岗位需求人数</label> <input type="text" oninput="value=value.replace(/[^\d]/g,'')" v-model = "job.job_require_num"/> </p>
          </div>
        </div>
        

        <p><button @click="addNewJob" > 添加岗位</button></p>
        
        <div id = "form">
          <div class = "oneQuestion" v-for = "(question,index) in form"  :key= "(question,index)">
            <h2>问题：{{question.text}}</h2>
            <p><button :data-index="index" @click="deleteThisQuestion" > 删除此问题</button></p>

            <input type='radio' id='bitian' value='true' v-model="question.required"/>
		        <label for='bitian'>此问题必填</label>
		
            <input type='radio' id='feibi' value="" v-model="question.required"/>
            <label for='feibi'>此问题非必填</label>

            <p><label>问题：</label> <input type = "text" v-model = "question.text"/></p>





            <div v-if="question.type === 'text'">  
              文本题         
              <p><label>默认答案：</label> <input type = "text" v-model = "question.value"/></p>              
            </div>

            <div v-if="question.type === 'radioBox'">
              <div class = "oneOption" v-for = "(option,optionIndex) in question.options" :key="(option,optionIndex)">
                <p><label>单选题选项：</label> <input type = "text" v-model = "option.name"/></p>
                <p><button :data-index="index" data-optionIndex="optionIndex" @click="deleteThisOption" > 删除此选项</button></p>
              </div>
              <p><button :data-index="index" @click="addNewOption" > 添加新选项</button></p>
            </div>

            <div v-if="question.type === 'checkBox'">
              <div class = "oneOption" v-for = "(option,optionIndex) in question.options" :key="(option,optionIndex)">
                <p><label>多选题选项：</label> <input type = "text" v-model = "option.name"/></p>
                <p><button :data-index="index" data-optionIndex="optionIndex" @click="deleteThisOption" > 删除此选项</button></p>
              </div>
              <p><button :data-index="index" @click="addNewOption" > 添加新选项</button></p>
            </div>


            

          </div>
        </div>

        <input type='radio' id='wenben' value='text' v-model="addNewQuestionType"/>
        <label for='wenben'>文本问题</label>

        <input type='radio' id='danxuan' value="radioBox" v-model="addNewQuestionType"/>
        <label for='danxuan'>单选题</label>
        <input type='radio' id='duoxuan' value="checkBox" v-model="addNewQuestionType"/>
        <label for='duoxuan'>多选题</label>
        <p><button @click="addNewQuestion" > 添加新问题</button></p>
        
        
        <p><button @click="submit" > 建立新项目</button></p>
        <p><button @click="back" > 返回主页</button></p>
    </div>   
  </div>
</template>

<script>
import {Message} from 'element-ui'
import request from '@/utils/request.js'
import {startProject} from '@/api/project'
export default {
  name: 'Project',
  
  data () {
    return {
        submitData: undefined,
        addNewQuestionType: "text",
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
        ],
        "form":[
          {
              "text":"姓名",
              "required":"true",
              "type":"text",
              "value":""
          },{
              "text":"献血量",
              "required":"true",
              "type":"radioBox",
              "options":[
                  {"name": "100"},
                  {"name": "200"}
              ],
              "value":""
          },{
              "text":"献血量",
              "required":"true",
              "type":"checkBox",
              "options":[
                  {"name": "100"},
                  {"name": "200"}
              ],
              "value":""
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
        that.submitData.append("requirements", that.requirements)
        that.submitData.append("deadline", that.deadlineDate + ' ' + that.deadlineTime)
        that.submitData.append("jobs", JSON.stringify(that.jobs))
        that.submitData.append("form", JSON.stringify(that.form))
        console.log("that.jobs:", that.jobs)
        console.log('LaunchProject中请求数据:that.submitData', JSON.stringify(that.submitData))
        startProject(that.submitData).then(res=>{
            Message({
                message: '成功发起项目！',
                type: 'success',
                duration: 5 * 1000
            })
            setTimeout(function(){that.$router.push('Home')},5000)
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
        let jobIndex = target.getAttribute("data-index")
        this.jobs.splice(jobIndex, 1)
    },
    deleteThisQuestion(event){
        let target = event.target
        let questionIndex = target.getAttribute("data-index")
        this.form.splice(questionIndex, 1)
    },
    deleteThisOption(event){
        let target = event.target
        console.log("target:",target)
        let questionIndex = target.getAttribute("data-index")
        let optionIndex = target.getAttribute("data-optionIndex")
        this.form[questionIndex].options.splice(optionIndex, 1)
    },
    addNewQuestion(){
        if(this.addNewQuestionType == 'text')
        {
            this.$data.form.push({
            "text":"姓名",
            "required":"true",
            "type":"text",
            "value":""
            })
        }
        if(this.addNewQuestionType == 'radioBox')
        {
            this.$data.form.push({
              "text":"献血量",
              "required":"true",
              "type":"radioBox",
              "options":[
                  {"name": "100"},
                  {"name": "200"}
              ],
              "value":""
            })
        }
        if(this.addNewQuestionType == 'checkBox')
        {
            this.$data.form.push({
              "text":"献血量",
              "required":"true",
              "type":"checkBox",
              "options":[
                  {"name": "100"},
                  {"name": "200"}
              ],
              "value":""
            })
        }
    },
    addNewOption(event){
        let target = event.target
        let questionIndex = target.getAttribute("data-index")
        this.form[questionIndex].options.push({
            "name": "1000"
        })
    },
    back(){
      this.$router.push('Home')
    }
  }
}
</script>
