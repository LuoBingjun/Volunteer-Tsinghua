import Vue from 'vue'
import Router from 'vue-router'
import Project from '@/components/Project'
import Info from '@/components/Info'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Project',
      component: Project
    },
    {
      path: '/info',
      name: 'Info',
      component: Info
    }
  ]
})
