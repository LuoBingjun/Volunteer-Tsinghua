<template>
  <div>
    <h1>登陆界面</h1>
    <p><label>账号</label> <input id='acc' @input ='textChanged' :value="acc"/></p>
    <p><label>密码</label> <input id='pass' @input ='textChanged' :value="pass"/></p>
    <p><button @click="login" > 点击登陆</button></p>
  </div>
</template>

<script>

import request from '@/api/request.js'
export default {
  name: 'Info',
  data () {
    return {
      msg: 'This is personal info!',
      acc: 'admin',
      pass: 'admin'
    }
  },
  methods:{
      login(){
          console.log('点击了登陆按钮')
          console.log(this.$data.acc,this.$data.pass)
          request({
            method:"post",
            url: '/auth/weblogin',
            data:{
                username: this.$data.acc,
                password: this.$data.pass
            }
            }).then(res=>console.log(res))
      },
      textChanged(e){
          console.log('文本发生了变化')
          console.log(this.$data.acc,this.$data.pass)
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
