<template>
  <div style='margin:20px'>
    <h1>Project# {{projectID}}: {{title}}</h1>
    <div> 
      <p v-if="ownername"> 发起人：{{ownername}} </p>
      <p v-if="content"> 项目详情：{{content}} </p>
      <div  v-if="requirements">
        <p> 需求：</p>
        <p v-for='item in requirements' :key='item.index'> 
            {{item}}
        </p>
      </div>
    </div>
    <div v-if="!finished && !started">       <!--  审核  -->
      <p>报名列表：</p>
      <p v-if='applyList && applyList.length == 0'>还没有人报名QAQ</p>
      <table v-if='applyList && applyList.length !=0'>
        <tr>
          <!--<td><Checkbox id="CA" @input="handleSelect"/></td>-->
          <td>报名人</td>
          <td>申请岗位</td>
          <!--<td> 
            <button @click="handleRecord" id="YA">统统通过</button>
          </td>
          <td>
            <button @click="handleRecord" id="NA">统统拒绝</button>
          </td>-->
        </tr>
        <tr v-for='itemm in applyList' :key='itemm.index'>
          <!--<td><Checkbox type='checkBox' :id="'C'+itemm.id" @input="handleSelect" :ref="'C'+itemm.id"/></td>-->
          <td>{{itemm.user.name}}</td>
          <td>{{itemm.job.job_name}}</td>
          <td> 
            <button v-if="itemm.status!='P'" @click="handleRecord" :id="'Y'+itemm.id">通过</button>
            <button v-if="itemm.status=='P' " disabled='true'>已通过</button>
          </td> 
          <td>
            <button v-if="itemm.status!='N'" @click="handleRecord" :id="'N'+itemm.id">拒绝</button>
            <button v-if="itemm.status=='N' " disabled='true'>已拒绝</button>
          </td>
        </tr>
      </table>
    </div>
    <div v-if="started && !finished">    <!--发起签到-->
      发起签到
      <table>
        <tr>
          <td> 签到标题 </td>
          <td> <input v-model="sign_opt.title" value="签到"/></td>
        </tr>
        <tr>
          <td> 签到描述 </td>
          <td> <input v-model="sign_opt.content" value="签到"/></td>
        </tr>
        <tr>
          <td>签到开始时间</td>
          <td><input type = "text" v-model = "sign_opt.begin_time"/></td>
        </tr>
        <tr>
          <td>签到结束时间</td>
          <td><input type = "text" v-model = "sign_opt.end_time" /></td>
        </tr>
        <tr>
          <td>岗位</td>
          <td>权限</td>
        </tr>
        <tr v-for="item in jobs" :key="item.index">
          <td>{{item.job_name}}</td>
          <td><input type="checkbox" :value="item.id" v-model="sign_opt.jobs"/></td>
        </tr>
      </table>
      <button @click="startSign">发起签到</button>
    </div>
    <div v-if="finished">          <!--导出工时-->
      已经结项：<button @click="exportExcel">导出为excel</button>
      <p v-if='applyList && applyList.length == 0'>没有记录~</p>
      <table v-if='applyList && applyList.length !=0' style="text-align:center">
        <tr>
          <td>参加人员</td>
          <td>岗位</td>
        </tr>
        <tr v-for='itemm in applyList' :key='itemm.index'>
          <td>{{itemm.user.name}}</td>
          <td>{{itemm.job.job_name}}</td>
        </tr>
      </table>
    </div>
    <button @click="changeRouter">点击返回</button>
    <label></label>
  </div>
</template>

<script>
import {getProjectDetails ,getProjectApplyList ,checkApplyRecord, downloadExcel, startSign} from '@/api/project'
import {Message, Checkbox} from 'element-ui'
export default {
  name: 'Project',
  components: {
    Checkbox
  },
  data () {
    return {
      ownername: undefined,
      projectID: undefined,
      title: undefined,
      content:undefined,
      cover: undefined,
      require_num:undefined,
      status:undefined,
      requirements:undefined,
      form:undefined,
      time:undefined,
      deadline:undefined,
      applyList:undefined,
      finished:undefined,
      started:undefined,
      jobs:undefined,
      sign_opt:{
        "title": undefined,
        "content": undefined,
        "begin_time": undefined,
        "end_time":undefined,
        "project": undefined,     //对应的项目ID
        "jobs": []
      }
    }
  },
  methods:{
    changeRouter(){
      console.log('点击了按钮')
      this.$router.go(-1)
    },
    handleRecord(e){
      var id=e.target.id.substr(1,e.target.id.length)
      var flag=e.target.id.substr(0,1)
      var that=this
      if(id!='A')
      {
        checkApplyRecord(parseInt(id),flag=='Y').then(res=>{
          Message({
            message: (flag=='Y'?'已审核通过':'已审核拒绝'),
            type: 'success',
            duration: 5 * 1000
          })
          for (var item in that.applyList)
          {
            if(that.applyList[item].id==parseInt(id))
            {
              that.applyList[item].status=(flag=='Y'?'P':'N')
              break
            }
          }
        }).catch(err=>{
          Message({
          message: 'Error request'+err,
          type: 'error',
          duration: 5 * 1000
          })
        })
      }
      else
      {
        for(var item in that.applyList)
        {
          if(that.applyList.selected)
          {
            checkApplyRecord(parseInt(id),flag=='Y').catch(err=>{
              Message({
                message: 'Error request'+err,
                type: 'error',
                duration: 5 * 1000
              })
            })
          }
        }
      }
    },
    startSign()
    {
      startSign(this.sign_opt).then(res=>{
        Message({
          message: '成功发起签到',
          type: 'success',
          duration: 5 * 1000
        })
      }).catch(err=>{
        Message({
          message: 'Error request'+err,
          type: 'error',
          duration: 5 * 1000
        })
      })
    },
    exportExcel()
    {
      downloadExcel(this.projectID).then(res=>{
        const url = window.URL.createObjectURL(new Blob([res.data]));
        const link = document.createElement('a');
        link.href = url;
        let fileName = res.headers['content-disposition'].split('filename=');
        link.setAttribute('download', fileName[1]);
        document.body.appendChild(link);
        link.click();
      }).catch(err=>{
        Message({
          message: 'Error request'+err,
          type: 'error',
          duration: 5 * 1000
        })
      })
    }
    /*
    handleSelect(e)
    {
      var id=e.target.id.substr(1,e.target.id.length)
      var flag=e.target.id.substr(0,1)
      if(id=='A')
      {
        for(var item in this.applyList)
        {
          this.applyList[item].selected=true;
          console.log(this.$refs['C'+this.applyList[item].id])
        }
      }
    }*/
  },
  created(){
    console.log('project页面加载完毕,route为',this.$route)
    this.$data.projectID=this.$route.query.projectID
    var that=this;
    getProjectDetails(this.projectID).then(res =>{
      console.log('项目详情',res)
      this.ownername=res.data.webuser.username
      that.title=res.data.title
      that.content=res.data.content
      that.cover=res.data.cover
      that.require_num=res.data.require_num
      that.status=res.data.status
      that.requirements=JSON.parse(res.data.requirements)
      that.form=res.data.form
      that.time=res.data.time
      that.deadline=res.data.deadline
      that.finished=res.data.finished
      that.sign_opt.project=this.projectID
      that.jobs=res.data.job_set
      console.log(that.job_set)

      console.log("得到的需求们：",this.requirements)
      var start = new Date(res.deadline).getTime()
      var now = new Date().getTime()
      if(start>now)this.started=false
      else this.started=true
      getProjectApplyList(this.projectID).then(res =>{
        console.log("报名信息：",res.data);
        that.applyList=res.data
      })
      .catch(err=>{
        Message({
        message: 'Error request'+err,
        type: 'error',
        duration: 5 * 1000
        })
      })

    }).catch(err =>{
      Message({
        message: 'Error request'+err,
        type: 'error',
        duration: 5 * 1000
      })
    })
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
a {
  color: #42b983;
}
p{
  text-align:initial;
}
li{
  text-align:initial;
}
</style>
