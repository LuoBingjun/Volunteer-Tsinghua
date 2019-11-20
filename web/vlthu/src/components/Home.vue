<template>
  <div>
    <h1>志愿清华团体版主页</h1>
    <div id="dApplyingProjects"> 
        <h2>正在报名中的项目</h2>     
        <li v-for="project in applyingProjects">
          {{ project.name }}
        </li>
    </div>
    <div id="dCurrentProjects">
        <h2>正在进行中的项目</h2>       
        <li v-for="project in currentProjects">
          {{ project.name }}
        </li>
    </div>
    <div id="dhistoryProjects">
        <h2>历史项目</h2>       
        <li v-for="project in historyProjects">
          {{ project.name }}
        </li>
    </div>


    
  </div>
</template>

<script>
export default {
  name: 'Project',
  data () {
    return {
      applyingProjects:[
        {name: 'proj1'},
        {name: 'proj2'},
        {name: 'proj3'},
      ],
      currentProjects:[
        {name: 'cproj1'},
        {name: 'cproj2'},
        {name: 'cproj3'},
      ],
      historyProjects:[
        {name: 'hproj1'},
        {name: 'hproj2'},
        {name: 'hproj3'},
      ],
    }
  },
  methods:{
    
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
