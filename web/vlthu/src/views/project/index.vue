<template>
  <div style='margin:20px'>
    <h1>Project# {{projectID}}: {{title}}</h1> 
    <el-card v-if="ownername">
      <i class="el-icon-user-solid"></i> 发起人：{{ownername}} 
    </el-card>
    <el-card v-if="content"> 
      <i class="el-icon-info"></i> 项目详情：{{content}} 
    </el-card>
    <el-card  v-if="requirements">
      <p>
        <i class="el-icon-star-off"></i> 需求：
      </p>
      <p v-for='item in requirements' :key='item.index'> 
         <i class="el-icon-circle-check"></i> {{item}}
      </p>
    </el-card>
    <el-card v-if="!finished && !started">       <!--  审核  -->
      <p>报名列表：</p>
      <p v-if='applyList && applyList.length == 0'>还没有人报名QAQ</p>
      <checkform v-if='applyList && applyList.length > 0' :applyList="applyList"> </checkform>
    </el-card>
    
    <el-card v-if="started && !finished">    <!--发起签到-->
      <i class="el-icon-circle-plus-outline"></i> 发起签到
      <signform :jobs="jobs" :projectID="projectID"/>
    </el-card>
    <el-card v-if="finished">
      <p> 
        已经结项：查看工时记录
        <el-button @click="exportExcel">
          <i class="el-icon-download"></i>导出工时为excel
        </el-button>
      </p>
      <p v-if='applyList && applyList.length == 0'>没有记录~</p>
      <table v-if='applyList && applyList.length !=0' style="text-align:center">
        <tr>jie
          <td>参加人员</td>
          <td>岗位</td>
        </tr>
        <tr v-for='itemm in applyList' :key='itemm.index'>
          <td>{{ itemm.user.name }}</td>
          <td>{{ itemm.job.job_name }}</td>
        </tr>
      </table>
    </el-card>
  </div>
</template>

<script>
/* eslint-disable */
import {getProjectDetails ,getProjectApplyList ,checkApplyRecord, downloadExcel, startSign} from '@/api/project'
import {Message, Checkbox} from 'element-ui'
import signform from './signform'
import checkform from './checkform'
export default {
  name: 'Project',
  components: {
    signform,checkform
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
    }
  },
  methods:{
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
          message: '获取错误'+'Error request'+err,
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
                message: '获取错误'+'Error request'+err,
                type: 'error',
                duration: 5 * 1000
              })
            })
          }
        }
      }
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
      that.jobs=res.data.job_set

      var start = new Date(res.data.deadline).getTime()
      var now = new Date().getTime()
      if(start>now)that.started=false
      else that.started=true
      
      getProjectApplyList(this.projectID).then(res =>{
        console.log("报名信息：",res.data);
        that.applyList=res.data
      })
      .catch(err=>{
        Message({
        message: '获取错误'+'Error request'+err,
        type: 'error',
        duration: 5 * 1000
        })
      })
    }).catch(err =>{
      Message({
        message: err,
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
