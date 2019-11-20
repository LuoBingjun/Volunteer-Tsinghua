<template>
  <div>
    <h1>{{ msg }}</h1>
    <button @click="changeRouter">点击切换</button>
    <label>{{projectID}}</label>
  </div>
</template>

<script>
export default {
  name: 'Project',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      projectID: undefined,
      projects:[
        {name: 'proj1'},
        {name: 'proj2'},
        {name: 'proj3'},
      ]
    }
  },
  methods:{
    changeRouter(){
      console.log('点击了按钮')
      this.$router.push('Info')
    }
  },
  created(){
    console.log('project页面加载完毕,projectID为',this.$route)
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
