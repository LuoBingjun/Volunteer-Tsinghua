<!-- 展示模板 -->
<template>
  <div id="app">
    <img src="./assets/logo.png">
    <hellouiui></hellouiui>
    <helloorigin/>
  </div>
</template>
 
<script>
// 导入组件
import hellouiui from './components/Hello'
import helloorigin from './components/HelloWorld'
export default {
  name: 'app',
  components: {
    hellouiui,
    helloorigin
  }
}
</script>
<!-- 样式代码 -->
<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>