<template>
  <div id="app">
    <div style='height:100px;bgcolor:#888888'>
      <h1> 志愿清华小程序 </h1>
    </div>
    <router-view/>
    <div style='height:100px;bgcolor:#888888'>
      <p> 志愿清华小程序</p>
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
</style>
