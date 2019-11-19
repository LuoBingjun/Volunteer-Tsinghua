<template>
  <div>
    <h1>{{ msg }}</h1>
    <button @click="changeRouter">点击切换</button>

  </div>
</template>

<script>
export default {
  name: 'Project',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  },
  methods:{
    changeRouter(){
      console.log('点击了按钮')
      this.$router.push('Info')
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
