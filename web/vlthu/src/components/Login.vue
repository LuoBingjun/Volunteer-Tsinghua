<template>
  <div>
    <h1>登陆界面</h1>
    <p><label>账号</label> <input ref='acc'  @input ='textChanged' :value="acc" /></p>
    <p><label>密码</label> <input ref='pass' @input ='textChanged' :value="pass"/></p>
    <p><button @click="login" > 点击登陆</button></p>
  </div>
</template>

<script>
import {login} from '@/api/login'
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
          login(this.$data.acc,this.$data.pass).then(res=>{
              console.log(res)
              this.$router.push({name:'Project',query:{projectID:4}})
            })
      },
      textChanged(e){
          console.log('文本发生了变化')
          this.acc=this.$refs.acc.value
          this.pass=this.$refs.pass.value
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
