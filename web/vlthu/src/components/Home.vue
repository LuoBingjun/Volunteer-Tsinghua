<template>
  <div>
    <h1>志愿清华团体版主页</h1>
    <div id="dApplyingProjects"> 
        <h2>正在报名中的项目</h2>     
        <p>
          <button v-for="project in applyingProjects" :key="project.index" @click="jumpToDetail" :id="project.id"> 
            {{ project.title }}
          </button>
        </p>
    </div>
    <div id="dCurrentProjects">
        <h2>正在进行中的项目</h2>       
        <p>
          <button v-for="project in currentProjects" :key="project.index" @click="jumpToDetail" :id="project.id"> 
            {{ project.title }}
          </button>
        </p>
    </div>
    <div id="dhistoryProjects">
        <h2>历史项目</h2>     
        <p>
          <button v-for="project in historyProjects" :key="project.index" @click="jumpToDetail" :id="project.id"> 
            {{ project.title }}
          </button>
        </p>
    </div>
    <button @click="startSign">发起项目</button>
  </div>
</template>

<script>
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
      this.$router.push({name:'Project',query:{projectID:e.target.id}})
    },
    startSign(){
      console.log("start!")
      this.$router.push("LaunchProject");
    }
  },
  
  created(){
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
