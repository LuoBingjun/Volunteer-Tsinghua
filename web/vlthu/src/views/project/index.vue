<template>
  <div style="margin:40px">
    <h1>{{title}}</h1>
    <el-card v-if="ownername" style="margin-bottom:10px;">
      <i class="el-icon-user-solid"> 发起人：</i>{{ownername}}
    </el-card>
    <el-card style="margin-bottom:10px;">
      <div v-if="type=='WH'"><i class="el-icon-school"> 项目类型：文化教育</i></div>
      <div v-else-if="type=='SH'"><i class="el-icon-medal-1"> 项目类型：赛会服务</i></div>
      <div v-else-if="type=='SQ'"><i class="el-icon-house"> 项目类型：社区服务</i></div>
      <div v-else-if="type=='YL'"><i class="el-icon-first-aid-kit"> 项目类型：医疗卫生</i></div>
      <div v-else-if="type=='JK'"><i class="el-icon-bangzhu"> 项目类型：健康残障</i></div>
      <div v-else-if="type=='XY'"><i class="el-icon-guide"> 项目类型：校园讲解</i></div>
      <div v-else-if="type=='QT'"><i class="el-icon-menu"> 项目类型：其他项目</i></div>
    </el-card>
    <el-card v-if="content" style="margin-bottom:10px;">
      <div slot="header" class="clearfix">
        <span>
          <i class="el-icon-info"></i> 项目详情
        </span>
      </div>
      {{content}}
    </el-card>
    <el-card v-if="requirements" style="margin-bottom:10px;">
      <div slot="header" class="clearfix">
        <span>
          <i class="el-icon-star-off"></i>
          需求
        </span>
      </div>
      {{requirements}}
    </el-card>
    <el-card v-if="!finished && !started" style="margin-bottom:10px;">
      <div slot="header" class="clearfix">
        <span>
          <i class="el-icon-check"></i>
          报名审核
        </span>
      </div>
      <p v-if="applyList && applyList.length == 0">暂时还没有人报名QAQ</p>
      <checkform v-if="applyList && applyList.length > 0" :applyList="applyList" :form="JSON.parse(form)"></checkform>
      
    </el-card>
    <el-card v-if="!finished && started">
      <div slot="header" class="clearfix">
        <span><i class="el-icon-close"> 结项操作</i></span>
      </div>
      <el-button type="danger" plain @click="endProject" v-if="!finished && started">
        <i class="el-icon-close"> 结束项目</i>
      </el-button>
    </el-card>
    <el-card style="margin:10px 0px" v-if="started && !finished">
      <div slot="header" class="clearfix">
        <span>
          <i class="el-icon-tickets"></i> 签到列表
        </span>
      </div>
      <signlist :signlist="signList"/>
    </el-card>
    <el-card v-if="started && !finished" style="Lmargin-bottom:10px;">
      <div slot="header" class="clearfix">
        <span>
          <i class="el-icon-circle-plus-outline"></i> 发起签到
        </span>
      </div>
      <signform :jobs="jobs" :projectID="projectID" />
    </el-card>

    <el-card v-if="finished" style="margin-bottom:10px;">
      <div slot="header" class="clearfix">
        <span>
          <i class="el-icon-setting"></i> 已经结项：查看/修改工时记录
          <el-upload action="#" 
            :http-request="uploadExcel" 
            :auto-upload="true"
            :multiple="false"
            :show-file-list="false"
            accept=".xls,.xlsx"
            style="float: right;"
          >
            <el-button type="primary">
              <i class="el-icon-upload"> 以Excel导入工时</i>
            </el-button>
          </el-upload>
          <el-button style="float: right; margin:0px 10px">
            <el-link  :href="'/api/worktime/Export?project_id='+projectID" type="primary">导出工时为excel</el-link>
          </el-button>
        </span>
      </div>
      <p v-if="applyList && applyList.length == 0">没有记录~</p>
      <el-table v-if="applyList && applyList.length !=0" :data="applyList">
        <el-table-column label="参加人员" prop="user.name"></el-table-column>
        <el-table-column label="岗位" prop="job.job_name"></el-table-column>
      </el-table>
      
      
    </el-card>
  </div>
</template>

<script>
/* eslint-disable */
import {
  getProjectDetails,
  getProjectApplyList,
  checkApplyRecord,
  downloadExcel,
  startSign,
  uploadExcel
} from "@/api/project";
import { Message, Checkbox, MessageBox } from "element-ui";
import signform from "./signform";
import checkform from "./checkform";
import {endProject} from "@/api/project"
import signlist from './signlist'
export default {
  name: "Project",
  components: {
    signform,
    checkform,
    signlist
  },
  data() {
    return {
      ownername: undefined,
      projectID: undefined,
      title: undefined,
      content: undefined,
      cover: undefined,
      require_num: undefined,
      status: undefined,
      requirements: undefined,
      form: undefined,
      time: undefined,
      deadline: undefined,
      applyList: undefined,
      finished: undefined,
      started: undefined,
      jobs: undefined,
      type: undefined, 
      signList:undefined
    };
  },
  methods: {
    handleRecord(e) {
      var id = e.target.id.substr(1, e.target.id.length);
      var flag = e.target.id.substr(0, 1);
      var that = this;
      if (id != "A") {
        checkApplyRecord(parseInt(id), flag == "Y")
          .then(res => {
            Message({
              message: flag == "Y" ? "已审核通过" : "已审核拒绝",
              type: "success",
              duration: 5 * 1000
            });
            for (var item in that.applyList) {
              if (that.applyList[item].id == parseInt(id)) {
                that.applyList[item].status = flag == "Y" ? "P" : "N";
                break;
              }
            }
          })
          .catch(err => {
            Message({
              message: "获取错误" + "Error request" + err,
              type: "error",
              duration: 5 * 1000
            });
          });
      } else {
        for (var item in that.applyList) {
          if (that.applyList.selected) {
            checkApplyRecord(parseInt(id), flag == "Y").catch(err => {
              Message({
                message: "获取错误" + "Error request" + err,
                type: "error",
                duration: 5 * 1000
              });
            });
          }
        }
      }
    },
    endProject(){
      var that=this
      this.$confirm('此操作不可逆转，是否结项？','提示',{
        confirmButtonText: '确定',
        cancelButtonText:'取消',
        type:'warning'
      }).then(()=>{
        endProject(this.projectID).then(res=>{
          Message({
            message:'已成功结项',
            type:'success',
            duration:3000
          })
          setTimeout(function(){that.$router.go(0)},3000) 
        })
      }).catch(()=>{
      })
    },
    uploadExcel(file){
      var newform=new FormData()
      newform.append('project_id',this.projectID)
      newform.append('import_file',file.file)
      uploadExcel(newform).then(res=>{
        Message({
          message:"成功上传",
          type:"success",
          duration:5000
        })
      }).catch(err=>{
        Message({
          message:"Error: ",err,
          type:"error",
          duration: 5000
        })
      })
    }
  },
  created() {
    console.log("project页面加载完毕,route为", this.$route);
    this.$data.projectID = this.$route.query.projectID;
    var that = this;
    getProjectDetails(this.projectID)
      .then(res => {
        console.log("项目详情", res);
        this.ownername = res.data.webuser;
        that.title = res.data.title;
        that.content = res.data.content;
        that.cover = res.data.cover;
        that.require_num = res.data.require_num;
        that.status = res.data.status;
        that.requirements = res.data.requirements;
        that.form = res.data.form;
        that.time = res.data.time;
        that.deadline = res.data.deadline;
        that.finished = res.data.finished;
        that.jobs = res.data.job_set;
        that.type = res.data.type;
        that.signList=res.data.signproject_set;

        var start = new Date(res.data.deadline).getTime();
        var now = new Date().getTime();
        if (start > now) that.started = false;
        else that.started = true;

        getProjectApplyList(this.projectID)
          .then(res => {
            console.log("报名信息：", res.data);
            that.applyList = res.data;
          })
          .catch(err => {
            Message({
              message: "获取错误" + "Error request" + err,
              type: "error",
              duration: 5 * 1000
            });
          });
      })
      .catch(err => {
        Message({
          message: err,
          type: "error",
          duration: 5 * 1000
        });
      });
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1,
h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
a {
  color: #42b983;
}
p {
  text-align: initial;
}
li {
  text-align: initial;
}
</style>
