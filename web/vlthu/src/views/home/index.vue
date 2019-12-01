<template>
  <div>
    <h1>志愿清华团体版主页</h1>
    <div id="dApplyingProjects">
      <h2>正在报名中的项目</h2>
      <p>
        <el-card v-for="project in applyingProjects" :id="project.id" :key="project.index" @click="jumpToDetail">
          <a :id="project.id" @click="jumpToDetail">{{ project.title }}</a>
        </el-card>
      </p>
    </div>
    <div id="dCurrentProjects">
      <h2>正在进行中的项目</h2>
      <p>
        <el-card v-for="project in currentProjects" :id="project.id" :key="project.index" @click="jumpToDetail">
          {{ project.title }}
        </el-card>
      </p>
    </div>
    <div id="dhistoryProjects">
      <h2>历史项目</h2>
      <p>
        <el-card v-for="project in historyProjects" :id="project.id" :key="project.index" @click="jumpToDetail">
          {{ project.title }}
        </el-card>
      </p>
    </div>
    <button @click="startSign">发起项目</button>
    <button @click="exit">退出登陆</button>
  </div>
</template>

<script>
/* eslint-disable */
import {Card} from 'element-ui'
import {getProjectList} from '@/api/project'
export default {
  name: 'Project',
  components:{Card},
  data () {
    return {
      applyingProjects:[],
      currentProjects:[],
      historyProjects:[]
    }
  },
  methods:{
    jumpToDetail(e){
      console.log(e.target.id)
      this.$router.push({path:'/project',query:{projectID:e.target.id}})
    },
    startSign(){
      console.log("start!")
      this.$router.push("LaunchProject");
    },
    exit(){
      this.$router.push("/")
    }
  },
  
  created(){
    console.log("来到了")
    var that=this
    this.applyingProjects=[]
    this.currentProjects=[]
    this.historyProjects=[]
    getProjectList().then(res => {
      console.log("收到了：",res)
      var data=res.data
      for(var item in data)
      {
        if(data[item].finished)
        {
          this.historyProjects.push(data[item])
        }
        else 
        {
          var start = new Date(data[item].deadline).getTime()
          var now = new Date().getTime()
          console.log("(n,s)=",now,start)
          if(now < start)this.applyingProjects.push(data[item])
          else this.currentProjects.push(data[item])
        }
      }
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
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
