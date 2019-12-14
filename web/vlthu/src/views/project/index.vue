<template>
  <div style="margin:40px">
    <h1>{{title}}</h1>
    <el-card v-if="ownername" style="margin-bottom:10px;">
      <div slot="header" class="clearfix">
        <span>
          <i class="el-icon-user-solid"></i> 发起人
        </span>
      </div>
      {{ownername}}
    </el-card>
    <el-card style="margin-bottom:10px;">
      <div slot="header" class="clearfix">
        <span>
          <i class="el-icon-menu">项目类型</i>
        </span>
      </div>
      <div v-if="type=='WH'">文化教育</div>
      <div v-else-if="type=='SH'">赛会服务</div>
      <div v-else-if="type=='SQ'">社区服务</div>
      <div v-else-if="type=='YL'">医疗卫生</div>
      <div v-else-if="type=='JK'">健康残障</div>
      <div v-else-if="type=='XY'">校园讲解</div>
      <div v-else-if="type=='QT'">其他项目</div>
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
    <el-button type="danger" plain @click="endProject" v-if="!finished && !started">
      <i class="el-icon-close"> 结项</i>
    </el-button>

    <el-card v-if="started && !finished" style="margin-bottom:10px;">
      <div slot="header" class="clearfix">
        <span>
          <i class="el-icon-circle-plus-outline"></i> 发起签到
        </span>
      </div>
      <signform :jobs="jobs" :projectID="projectID" />
    </el-card>

    <el-card v-if="finished" style="margin-bottom:10px;">
      <p>
        已经结项：查看工时记录
        <el-button @click="exportExcel">
          <i class="el-icon-download"></i>导出工时为excel
        </el-button>
      </p>
      <p v-if="applyList && applyList.length == 0">没有记录~</p>
      <table v-if="applyList && applyList.length !=0" style="text-align:center">
        <tr>
          <td>参加人员</td>
          <td>岗位</td>
        </tr>
        <tr v-for="itemm in applyList" :key="itemm.index">
          <td>{{ itemm.user.name }}</td>
          <td>{{ itemm.job.job_name }}</td>
        </tr>
      </table>
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
  startSign
} from "@/api/project";
import { Message, Checkbox, MessageBox } from "element-ui";
import signform from "./signform";
import checkform from "./checkform";
import {endProject} from "@/api/project"
export default {
  name: "Project",
  components: {
    signform,
    checkform
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
    exportExcel() {
      downloadExcel(this.projectID)
        .then(res => {
          const url = window.URL.createObjectURL(new Blob([res.data]));
          const link = document.createElement("a");
          link.href = url;
          let fileName = res.headers["content-disposition"].split("filename=");
          link.setAttribute("download", fileName[1]);
          document.body.appendChild(link);
          link.click();
        })
        .catch(err => {
          Message({
            message: "Error request" + err,
            type: "error",
            duration: 5 * 1000
          });
        });
    },
    endProject(){
      this.$confirm('此操作不可逆转，是否结项？','提示',{
        confirmButtonText: '确定',
        cancelButtonText:'取消',
        type:'warning'
      }).then(()=>{
        endProject(this.projectID).then(res=>{
          Message({
            message:'已成功结项',
            type:'success',
            duration:5000
          })
          this.$router.push(-1)
        })
      }).catch(()=>{
        Message({
          message:'已取消',
          type:'info',
          duration:5000
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
