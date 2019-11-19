<template>
  <div id="app">
    <div style='height:100px;background-color: blueviolet;'>
      <h1> 志愿清华小程序 </h1>
    </div>
    <router-view/>
    <div style='height:100px;background-color: blueviolet;'>
      <p> @志愿清华小程序</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

body{
  margin:0px
}
</style>
