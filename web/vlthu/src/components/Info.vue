<template>
  <div>
    <h1>{{ msg }}</h1>
    <h2>Essential Links</h2>
  </div>
</template>

<script>
import request from '@/api/request'
export default {
  name: 'Info',
  data () {
    return {
      msg: 'This is personal info!'
    }
  },
  created(){
    request({
      url:'/auth/user',
      method:'get',
    }).then(res =>{
      console.log('This page is created!',this.$data,res)
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
