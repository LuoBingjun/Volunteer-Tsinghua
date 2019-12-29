<template>
  <div style="margin:40px;">
      <launchform />
  </div>
</template>

<script>
import {Message} from 'element-ui'
import request from '@/utils/request.js'
import {startProject} from '@/api/project'
import launchform from "./launchform"
export default {
  name: 'Project',
  components: {launchform},
  data () {
    return {}
  },
  methods:{
    
  }
}
</script>
